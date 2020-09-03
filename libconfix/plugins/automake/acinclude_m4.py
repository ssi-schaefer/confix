# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.core.utils.paragraph import ParagraphSet
from libconfix.core.utils import const

class ACInclude_m4:

    """ Straightforward encapsulation of acinclude.m4, containing
    "paragraphs". """

    def __init__(self):
        self.paragraphs_ = ParagraphSet()
        pass

    def add_paragraph(self, paragraph):
        self.paragraphs_.add(paragraph)
        
    def add_paragraphs(self, paragraphset):
        self.paragraphs_ += paragraphset
        
    def lines(self):
        lines = []
        lines.append('# DO NOT EDIT! This file was automatically generated')
        lines.append('# by Confix version '+const.CONFIX_VERSION)
        lines.extend(self.paragraphs_.lines())
        return lines
        
