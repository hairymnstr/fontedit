##
##    This file is part of Fontedit.
##    Copyright 2010 Nathan Dumont
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

import sys, os
import pygtk
import gtk, gobject
from math import floor, ceil, sqrt

if gtk.pygtk_version < (2,6):
  print "PyGTK 2.6 or later required for this widget"
  sys.exit(-1)

class FontViewWidget(gtk.ScrolledWindow):
  def __init__(self, font):
    gtk.ScrolledWindow.__init__(self)

    self.fg = ("%c%c%c" % (font.fg['r'] >> 8, font.fg['g'] >> 8,
                           font.fg['b'] >> 8))
    self.bg = ("%c%c%c" % (font.bg['r'] >> 8, font.bg['g'] >> 8,
                           font.bg['b'] >> 8))

    self.highlight_colour = gtk.gdk.Color(65535, 0, 0)
    tc = self.get_style()
    tc = tc.bg[gtk.STATE_NORMAL]
    self.normal_colour = gtk.gdk.Color(tc.red, tc.green, tc.blue)

    self.font = font
    self.chars_per_line = int(floor(sqrt(font.chars)))
    self.lines = int(ceil(font.chars / self.chars_per_line))

    self.table = gtk.Table(self.lines, self.chars_per_line, True)

    self.add_with_viewport(self.table)

    self.pbf = []
    self.img = []
    self.img_border = []
    for c in range(font.chars):
      # generate a pixmap of the character and display it in the table
      # first make a string from the font entry
      d = ""
      for i in range(font.rows):
        for j in range(font.cols):
          if font.get_character(c)[i][j]:
            d += self.fg
          else:
            d += self.bg
      # now make a new pixbuf from this
      self.pbf.append(gtk.gdk.pixbuf_new_from_data(d, gtk.gdk.COLORSPACE_RGB,
                      False, 8, font.cols, font.rows, font.cols * 3))

      row = c / self.chars_per_line
      col = c % self.chars_per_line
      self.img.append(gtk.image_new_from_pixbuf(self.pbf[c]))
      self.img_border.append(gtk.EventBox())
      self.img_border[c].add(self.img[c])
      self.img_border[c].connect("button-press-event", self.char_click, c)
      self.img[c].set_padding(1,1)
      self.table.attach(self.img_border[c], col, col+1, row, row+1)

    self.show_all()

  def update(self, c):
    self.img_border[c].remove(self.img[c])
    # generate a pixmap of the character and display it in the table
    # first make a string from the font entry
    d = ""
    for i in range(self.font.rows):
      for j in range(self.font.cols):
        if self.font.get_character(c)[i][j]:
          d += self.fg
        else:
          d += self.bg
    # now make a new pixbuf from this
    self.pbf[c] = gtk.gdk.pixbuf_new_from_data(d, gtk.gdk.COLORSPACE_RGB,
                  False, 8, self.font.cols, self.font.rows, self.font.cols * 3)
    self.img[c] = gtk.image_new_from_pixbuf(self.pbf[c])
    self.img[c].set_padding(1, 1)

    row = c / self.chars_per_line
    col = c % self.chars_per_line

    self.img_border[c].add(self.img[c])
 
  def select(self, c):
    for i in range(self.font.chars):
      if i == c:
        self.img_border[c].modify_bg(gtk.STATE_NORMAL, self.highlight_colour)
      else:
        self.img_border[i].modify_bg(gtk.STATE_NORMAL, self.normal_colour)
    
  def char_click(self, widget, event, ind):
    self.emit("select-char", ind)
 
  def set_colours(self, fr, fg, fb, br, bg, bb):
    self.fg = "%c%c%c" % (fr >> 8, fg >> 8, fb >> 8)
    self.bg = "%c%c%c" % (br >> 8, bg >> 8, bb >> 8)
    for c in range(self.font.chars):
      self.update(c)

# make the new signal select-char generated when a character image is clicked
gobject.signal_new("select-char", FontViewWidget,
                   gobject.SIGNAL_ACTION,
                   gobject.TYPE_NONE,
                   (gobject.TYPE_PYOBJECT,))

