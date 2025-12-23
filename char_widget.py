##
##    This file is part of Fontedit.
##    Copyright 2010-2020 Nathan Dumont
##
##    Fontedit is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    Fontedit is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Fontedit.  If not, see <http://www.gnu.org/licenses/>.
##

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk

class CharacterWidget(Gtk.EventBox):
    def __init__(self, font):
        GObject.GObject.__init__(self)
        self.set_size_request(100, 100)
        self.drawing = Gtk.DrawingArea()
        self.drawing.connect("draw", self.expose)
        # event signals
        self.drawing.connect('motion-notify-event', self.draw_motion_notify_event)
        self.drawing.connect('button-press-event', self.draw_button_press_event)

        # Ask to receive events the drawing area doesn't normally
        # subscribe to
        self.drawing.set_events(self.drawing.get_events()
                      | Gdk.EventMask.LEAVE_NOTIFY_MASK
                      | Gdk.EventMask.BUTTON_PRESS_MASK
                      | Gdk.EventMask.POINTER_MOTION_MASK
                      | Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.add(self.drawing)

        self.fg = (font.fg['r'] / 65535, font.fg['g'] / 65535, font.fg['b'] / 65535)
        self.bg = (font.bg['r'] / 65535, font.bg['g'] / 65535, font.bg['b'] / 65535)
        self.rows = font.rows
        self.cols = font.cols

        self.pixels = []
        for y in range(font.rows):
            self.pixels.append([])
            for x in range(font.cols):
                self.pixels[-1].append(0)

        self._modified = False
        self.drag_value = 0
        self.show_all()
    
    def expose(self, area, context):
        context.scale(area.get_allocated_width(), area.get_allocated_height())

        xstep = 1.0 / self.cols
        ystep = 1.0 / self.rows

        for i in range(self.rows):
            for j in range(self.cols):
                if self.pixels[i][j]:
                    context.set_source_rgb(*self.fg)
                else:
                    context.set_source_rgb(*self.bg)
                context.rectangle(j*xstep, i*ystep, xstep*0.95, ystep*0.95)
                context.fill()
        
        return True

    def draw_pixel(self, x, y, start=False):
        width = self.drawing.get_allocated_width()
        height = self.drawing.get_allocated_height()
        ystep = 1.0 / self.rows
        xstep = 1.0 / self.cols
        x = x / width
        y = y / height

        pixel_row = int(y / ystep)
        pixel_col = int(x / xstep)

        if (0 <= pixel_row < self.rows) and (0 <= pixel_col < self.cols):
            if start:
                old_val = self.pixels[pixel_row][pixel_col]
                self.drag_value = old_val ^ 1
            self.pixels[pixel_row][pixel_col] = self.drag_value
            self.drawing.queue_draw_area(pixel_col * xstep * width,
                                        pixel_row * ystep * height,
                                        xstep * width,
                                        ystep * height)

    def draw_motion_notify_event(self, area, event):
        (window, x, y, state) = event.window.get_pointer()

        if state & Gdk.ModifierType.BUTTON1_MASK:
            self.draw_pixel(x, y)
    
    def draw_button_press_event(self, area, event):
        if event.button == 1:
            self.draw_pixel(event.x, event.y, start=True)
            self._modified = True

    def get_pixels(self):
        return self.pixels
    
    def set_pixels(self, vals):
        self.pixels = vals
        self.drawing.queue_draw()

    def set_fg(self, r, g, b):
        self.fg = (r / 65535, g / 65535, b / 65535)
        self.drawing.queue_draw()
    
    def set_bg(self, r, g, b):
        self.bg = (r / 65535, g / 65535, b / 65535)
        self.drawing.queue_draw()

    def clear_modified(self):
        self._modified = False

    @property
    def modified(self):
        return self._modified
