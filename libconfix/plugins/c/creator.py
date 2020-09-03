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

from c import CBuilder
from cxx import CXXBuilder
from h import HeaderBuilder
from lex import LexBuilder
from yacc import YaccBuilder

from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

import os

class CCreator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__handled_entries = set()
        pass

    def shortname(self):
        return 'CCreator'

    def locally_unique_id(self):
        # I am supposed to be the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)
    
    def enlarge(self):
        super(CCreator, self).enlarge()
        for name, entry in self.parentbuilder().directory().entries():
            if not isinstance(entry, VFSFile):
                continue
            if name in self.__handled_entries:
                continue
            builder = do_create_builder(name=name, entry=entry)
            if builder is None:
                continue
            self.__handled_entries.add(name)
            self.parentbuilder().add_builder(builder)
            pass
        pass
    pass

def do_create_builder(name, entry):
    root, ext = os.path.splitext(name)
    if ext in ['.h', '.hh', '.hpp']:
        return HeaderBuilder(file=entry)
    if ext in ['.c']:
        return CBuilder(file=entry)
    if ext in ['.cpp', '.cc', '.cxx']:
        return CXXBuilder(file=entry)
    if ext in ['.l', '.ll']:
        return LexBuilder(file=entry)
    if ext in ['.y', '.yy']:
        return YaccBuilder(file=entry)
    return None

class CCreatorSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(CCreator())
        pass
    pass
