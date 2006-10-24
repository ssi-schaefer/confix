# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import os

from builder import Builder

class EntryBuilder(Builder):
    def __init__(self, entry):
        Builder.__init__(self)
        self.__entry = entry
        self.__unique_id = None
        pass

    def __str__(self):
        return str(self.__class__)+'('+os.sep.join(self.__entry.abspath())+')'
        
    def unique_id(self):
        if self.__unique_id is None:
            self.__unique_id = str(self.__class__)+\
                               '('+'/'.join(self.__entry.relpath(self.package().rootbuilder().directory()))+')'
            pass
        return self.__unique_id
    def entry(self):
        return self.__entry
    pass

