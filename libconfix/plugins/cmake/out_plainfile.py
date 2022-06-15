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

from .out_cmake import find_cmake_output_builder

from libconfix.plugins.plainfile.builder import PlainFileBuilder
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup
from libconfix.core.filesys.file import FileState

class PlainfileOutputSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(PlainfileOutputBuilder())
        pass
    pass

class PlainfileOutputBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)

    def output(self):
        super(PlainfileOutputBuilder, self).output()

        output_builder = None
        
        for b in self.parentbuilder().iter_builders():
            if isinstance(b, PlainFileBuilder):

                if output_builder is None:
                    output_builder = find_cmake_output_builder(self.parentbuilder())
                    assert output_builder is not None
                    pass

                # cmake makes a difference between files that have
                # been generated in the build directory and regular
                # ones from the source directory. we use the
                # FileState.VIRTUAL as a heuristic, until we find a
                # better way.
                if b.file().state() is FileState.VIRTUAL:
                    path = '${CMAKE_CURRENT_BINARY_DIR}/'+b.file().name()
                else:
                    path = b.file().name()
                    pass

                if b.datadir() is not None:
                    output_builder.local_cmakelists().add_install__files(
                        files=[path],
                        destination='share/'+'/'.join(b.datadir()))
                elif b.prefixdir() is not None:
                    output_builder.local_cmakelists().add_install__files(
                        files=[path],
                        destination='/'.join(b.prefixdir()))
                else:
                    assert 0
                    pass

                pass
            pass
        pass

    pass
