# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder

from libconfix.plugins.c.library import LibraryBuilder

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder

class COutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(LibraryOutputBuilder())
        pass
    pass

class LibraryOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    
    def output(self):
        super(LibraryOutputBuilder, self).output()
        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())
        for library in self.parentbuilder().iter_builders():
            if not isinstance(library, LibraryBuilder):
                continue
            cmake_output_builder.local_cmakelists().add_library_definition(
                library.basename(),
                [member.file().name() for member in library.members()])
            pass
        pass

    pass
