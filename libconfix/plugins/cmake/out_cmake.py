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

from cmakelists import CMakeLists

from libconfix.core.machinery.builder import Builder
from libconfix.core.filesys.file import File

def find_cmake_output_builder(dirbuilder):
    """
    Find the directory's dedicated automake output builder.
    """
    for b in dirbuilder.iter_builders():
        if isinstance(b, CMakeBackendOutputBuilder):
            return b
        pass
    else:
        assert False
        pass
    pass

class CMakeBackendOutputBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__local_cmakelists = None
        self.__top_cmakelists = None
        pass

    def local_cmakelists(self):
        return self.__local_cmakelists

    def locally_unique_id(self):
        return str(self.__class__)

    def initialize(self, package):
        super(CMakeBackendOutputBuilder, self).initialize(package)
        self.__local_cmakelists = CMakeLists()
        if self.parentbuilder() == package.rootbuilder():
            self.__top_cmakelists = self.__local_cmakelists
            pass
        else:
            top_cmake_builder = find_cmake_output_builder(package.rootbuilder())
            self.__top_cmakelists = top_cmake_builder.cmakelists()
            pass
        pass

    def output(self):
        super(CMakeBackendOutputBuilder, self).output()
        
        cmakelists_file = self.parentbuilder().directory().find(['CMakeLists.txt'])
        if cmakelists_file is None:
            cmakelists_file = File()
            self.parentbuilder().directory().add(name='CMakeLists.txt', entry=cmakelists_file)
        else:
            cmakelists_file.truncate()
            pass
        cmakelists_file.add_lines(self.__local_cmakelists.lines())
        pass
    
    pass
