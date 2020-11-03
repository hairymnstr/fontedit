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

class Font:
  """ Base class for all fonts.  Each new font created generates a Font object
      saving and loading are achieved by pickling/unpickling this object. """
  def __init__(self, rows, cols, chars):
    self._rows = rows
    self._cols = cols
    self._chars = []
    for i in range(chars):
      self._chars.append([])
      for j in range(rows):
        self._chars[i].append([])
        for k in range(cols):
          self._chars[i][j].append(0)
    self.current = 0
    self.changed = False
    self.fg = {'r': 65535, 'g': 65535, 'b': 65535}
    self.bg = {'r': 0, 'g': 0, 'b': 0}

  def get_rows(self):
    """ Number of rows of pixels in the character """
    return self._rows

  def set_rows(self, val):
    if isinstance(val, [int, long]) and (val < 33) and (val > 0):
      self._rows = val

  def get_cols(self):
    """ Number of columns of pixels in the character """
    return self._cols

  def set_cols(self, val):
    if isinstance(val, [int, long]) and (val < 33) and (val > 0):
      self._cols = val

  @property
  def chars(self):
    """ Number of characters in this object """
    return len(self._chars)

  def get_character(self, ind):
    return self._chars[ind]

  def set_character(self, ind, val):
    for i in range(self._rows):
      for j in range(self._cols):
        if self._chars[ind][i][j] != val[i][j]:
          self.changed = True
        self._chars[ind][i][j] = val[i][j]

  rows = property(get_rows, set_rows)
  cols = property(get_cols, set_cols)

