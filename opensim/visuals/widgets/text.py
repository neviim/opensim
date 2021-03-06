#===--- text.py - OpenSim text manager ------------------------------------===#
#
# Copyright 2008 Bobby Powers
#
# This file is part of OpenSim.
# 
# OpenSim is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# OpenSim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with OpenSim.  If not, see <http://www.gnu.org/licenses/>.
#
#===-----------------------------------------------------------------------===#
#
# This file contains the implementation of TextInfo, the class designed
# to store text labels and provide information about the size of them.
#
#===-----------------------------------------------------------------------===#

import cairo, pango, pangocairo


class TextInfo():

  def __init__(self, string, font_face='Arial,sans', wrap_width=180,
               font_size=14, align=pango.ALIGN_CENTER, 
               placeholder_text=False, cr=None):
    self.string = string
    self.font_face = font_face
    self.font_size = font_size
    self.width = wrap_width
    self.text_width = self.width
    self.placeholder = placeholder_text
    self.align = align

    self.font_description = "%s normal %d" % (self.font_face, self.font_size)


  def update_extents(self, cr):
    cr.save()

    layout = self.create_layout(cr)
    self.text_width, self.height = layout.get_pixel_size()

    cr.restore()


  def create_layout(self, cr):
    pcctx = pangocairo.CairoContext(cr)
    font_map = pangocairo.cairo_font_map_get_default()
    pcr = font_map.create_context()
    p_layout = pango.Layout(pcr)
    p_layout.set_wrap(pango.WRAP_WORD)
    p_layout.set_width(int(self.width*pango.SCALE))
    font = pango.FontDescription(self.font_description)
    p_layout.set_font_description(font)
    p_layout.set_alignment(self.align)
    p_layout.set_text(self.string)
    return p_layout


  def show_text(self, cr):
    cr.save()
    layout = self.create_layout(cr)

    self.text_width, self.height = layout.get_pixel_size()
    cr.translate(-int(self.width/2), -int(self.height/2))
    pc = pangocairo.CairoContext(cr)
    pc.show_layout(layout)

    cr.restore()


  def add(self, string):
    if self.placeholder:
      self.string = ''
      self.placeholder = False
    self.string = self.string + string

  def backspace(self):
    if len(self.string) > 0:
      self.string = self.string[0:-1]


  def new_width(self, requested_width):
    self.width = requested_width

