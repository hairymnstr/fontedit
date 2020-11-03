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

if gtk.pygtk_version < (2,6):
  print "PyGTK 2.6 or later required for this widget"
  sys.exit(-1)

class CharacterWidget(gtk.EventBox):
  def __init__(self, font):
    gtk.EventBox.__init__(self)
    self.table = gtk.Table(font.rows, font.cols, True)
    self.add(self.table)

    self._colour_frame = gtk.gdk.Color(0, 0, 0)
    self._colour_bg = gtk.gdk.Color(font.bg['r'], 
                                    font.bg['g'],
                                    font.bg['b'])
    self._colour_fg = gtk.gdk.Color(font.fg['r'],
                                    font.fg['g'],
                                    font.fg['b'])

    self.modify_bg(gtk.STATE_NORMAL, self._colour_frame)

    self.pixels = []
    for i in range(font.rows):
      self.pixels.append([])
      for j in range(font.cols):
        self.pixels[i].append(gtk.EventBox())
        self.pixels[i][j].modify_bg(gtk.STATE_ACTIVE, self._colour_fg)
        self.pixels[i][j].modify_bg(gtk.STATE_NORMAL, self._colour_bg)
        self.pixels[i][j].connect("button-press-event", self.pixel_click)
        self.pixels[i][j].set_size_request(28, 28)
        self.table.attach(self.pixels[i][j], j, j+1, i, i+1, 
                          xpadding=1, ypadding=1)

    self._modified = False
    self.show_all()

  def pixel_click(self, widget, *kw):
    if widget.state == gtk.STATE_NORMAL:
      widget.set_state(gtk.STATE_ACTIVE)
    else:
      widget.set_state(gtk.STATE_NORMAL)
    self._modified = True

  def get_pixels(self):
    ret = []
    for i in range(len(self.pixels)):
      ret.append([])
      for j in range(len(self.pixels[0])):
        if self.pixels[i][j].state == gtk.STATE_NORMAL:
          ret[i].append(0)
        else:
          ret[i].append(1)
    return ret;

  def set_pixels(self, vals):
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        if vals[i][j] == 0:
          self.pixels[i][j].set_state(gtk.STATE_NORMAL)
        else:
          self.pixels[i][j].set_state(gtk.STATE_ACTIVE)
    self._modified = False

  def clear_modified(self):
    self._modified = False

  def set_fg(self, r, g, b):
    self._colour_fg = gtk.gdk.Color(r, g, b)
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        self.pixels[i][j].modify_bg(gtk.STATE_ACTIVE, self._colour_fg)

  def set_bg(self, r, g, b):
    self._colour_bg = gtk.gdk.Color(r, g, b)
    for i in range(len(self.pixels)):
      for j in range(len(self.pixels[0])):
        self.pixels[i][j].modify_bg(gtk.STATE_NORMAL, self._colour_bg)

  @property
  def modified(self):
    return self._modified

if __name__ == "__main__":
  win = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
  win.connect("destroy", lambda obj, *kw: gtk.main_quit())
  char = CharacterWidget(12, 8)
  win.add(char)
  win.show_all()
  gtk.main()

