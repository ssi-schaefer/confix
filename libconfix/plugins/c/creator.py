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

from libconfix.core.builder import Builder
from libconfix.core.setup import Setup
from libconfix.core.filesys.file import File

from h import HeaderBuilder
from c import CBuilder
from cxx import CXXBuilder
from lex import LexBuilder
from yacc import YaccBuilder

class Creator(Builder):
    def __init__(self, parentbuilder, package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.handled_entries_ = set()
        pass
    
    def enlarge(self):
        super(Creator, self).enlarge()
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, File):
                continue
            if name in self.handled_entries_:
                continue
            builder = do_create_builder(name=name,
                                        entry=entry,
                                        parentbuilder=self.parentbuilder(),
                                        package=self.package())
            if builder is None:
                continue
            self.handled_entries_.add(name)
            self.parentbuilder().add_builder(builder)
            pass
        pass
    pass

def do_create_builder(name, entry, parentbuilder, package):
    root, ext = os.path.splitext(name)
    if ext in ['.h', '.hh', '.hpp']:
        return HeaderBuilder(file=entry,
                             parentbuilder=parentbuilder,
                             package=package)
    if ext in ['.c']:
        return CBuilder(file=entry,
                        parentbuilder=parentbuilder,
                        package=package)
    if ext in ['.cpp', '.cc', '.cxx']:
        return CXXBuilder(file=entry,
                          parentbuilder=parentbuilder,
                          package=package)
    if ext in ['.l', '.ll']:
        return LexBuilder(file=entry,
                          parentbuilder=parentbuilder,
                          package=package)
    if ext in ['.y', '.yy']:
        return YaccBuilder(file=entry,
                           parentbuilder=parentbuilder,
                           package=package)
    return None

class CreatorSetup(Setup):
    def setup_directory(self, directory_builder):
        super(CreatorSetup, self).setup_directory(directory_builder)

        directory_builder.add_builder(Creator(parentbuilder=directory_builder,
                                              package=directory_builder.package()))
        pass
    pass
