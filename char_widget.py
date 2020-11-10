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

import sys
import os
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gdk
from gi.repository import GdkPixbuf

class CharacterWidget(Gtk.EventBox):
  def __init__(self, font):
    GObject.GObject.__init__(self)
    self.table = Gtk.Table(font.rows, font.cols, True)
    self.add(self.table)

    self._colour_frame = Gdk.Color(0, 0, 0)
    self._colour_bg = Gdk.Color(font.bg['r'], 
                                    font.bg['g'],
                                    font.bg['b'])
    self._colour_fg = Gdk.Color(font.fg['r'],
                                    font.fg['g'],
                                    font.fg['b'])
    d = bytes([font.fg['r']//256, font.fg['g']//256, font.fg['b']//256] * (32*32))
    self.drag_active = GdkPixbuf.Pixbuf.new_from_data(d, GdkPixbuf.Colorspace.RGB,
                                                      False, 8, 32, 32, 32*3)
    d = bytes([font.bg['r']//256, font.bg['g']//256, font.bg['b']//256] * (32*32))
    self.drag_normal = GdkPixbuf.Pixbuf.new_from_data(d, GdkPixbuf.Colorspace.RGB,
                                                      False, 8, 32, 32, 32*3)
    
    self.modify_bg(Gtk.StateType.NORMAL, self._colour_frame)

    self.pixels = []
    for i in range(font.rows):
      self.pixels.append([])
      for j in range(font.cols):
        self.pixels[i].append(Gtk.EventBox())
        self.pixels[i][j].modify_bg(Gtk.StateType.ACTIVE, self._colour_fg)
        self.pixels[i][j].modify_bg(Gtk.StateType.NORMAL, self._colour_bg)
        self.pixels[i][j].set_events(self.pixels[i][j].get_events() | Gdk.EventMask.POINTER_MOTION_MASK)
        self.pixels[i][j].connect("button-press-event", self.pixel_click)
        self.pixels[i][j].connect("drag-motion", self.pixel_drag2)
        self.pixels[i][j].drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [Gtk.TargetEntry.new(f"pix", Gtk.TargetFlags.SAME_APP, i*font.cols+j)], Gdk.DragAction.PRIVATE)
        self.pixels[i][j].drag_dest_set(Gtk.DestDefaults.ALL, [Gtk.TargetEntry.new(f"pix", Gtk.TargetFlags.SAME_APP, i*font.cols+j)], Gdk.DragAction.PRIVATE)
        self.pixels[i][j].set_size_request(28, 28)
        self.table.attach(self.pixels[i][j], j, j+1, i, i+1, 
                          xpadding=1, ypadding=1)

    self._modified = False
    self.show_all()

  def pixel_click(self, widget, *kw):
    if widget.get_state() == Gtk.StateType.NORMAL:
      widget.set_state(Gtk.StateType.ACTIVE)
      self._drag_state = Gtk.StateType.ACTIVE
      widget.drag_source_set_icon_pixbuf(self.drag_active)
    else:
      widget.set_state(Gtk.StateType.NORMAL)
      self._drag_state = Gtk.StateType.NORMAL
      widget.drag_source_set_icon_pixbuf(self.drag_normal)
    self._modified = True

  def pixel_drag2(self, widget, content, x, y, time):
    widget.set_state(self._drag_state)

  def get_pixels(self):
    ret = []
    for i in range(len(self.pixels)):
      ret.append([])
      for j in range(len(self.pixels[0])):
        if self.pixels[i][j].get_state() == Gtk.StateType.NORMAL:
          ret[i].append(0)
        else:
          ret[i].append(1)
    return ret;

  def set_pixels(self, vals):
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        if vals[i][j] == 0:
          self.pixels[i][j].set_state(Gtk.StateType.NORMAL)
        else:
          self.pixels[i][j].set_state(Gtk.StateType.ACTIVE)
    self._modified = False

  def clear_modified(self):
    self._modified = False

  def set_fg(self, r, g, b):
    self._colour_fg = Gdk.Color(r, g, b)
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        self.pixels[i][j].modify_bg(Gtk.StateType.ACTIVE, self._colour_fg)
    d = bytes([r//256, g//256, b//256] * (32*32))
    self.drag_active = GdkPixbuf.Pixbuf.new_from_data(d, GdkPixbuf.Colorspace.RGB,
                                                      False, 8, 32, 32, 32*3)

  def set_bg(self, r, g, b):
    self._colour_bg = Gdk.Color(r, g, b)
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        self.pixels[i][j].modify_bg(Gtk.StateType.NORMAL, self._colour_bg)
    d = bytes([r//256, g//256, b//256] * (32*32))
    self.drag_normal = GdkPixbuf.Pixbuf.new_from_data(d, GdkPixbuf.Colorspace.RGB,
                                                      False, 8, 32, 32, 32*3)

  @property
  def modified(self):
    return self._modified

if __name__ == "__main__":
  win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
  win.connect("destroy", lambda obj, *kw: Gtk.main_quit())
  char = CharacterWidget(12, 8)
  win.add(char)
  win.show_all()
  Gtk.main()

