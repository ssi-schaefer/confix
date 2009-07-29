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
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
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

    def top_cmakelists(self):
        return self.__top_cmakelists

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
            self.__top_cmakelists = top_cmake_builder.local_cmakelists()
            pass
        pass

    def output(self):
        super(CMakeBackendOutputBuilder, self).output()

        if self.parentbuilder() is self.package().rootbuilder():
            self.__output_top_cmakelists()
            pass
        
        cmakelists_file = self.parentbuilder().directory().find(['CMakeLists.txt'])
        if cmakelists_file is None:
            cmakelists_file = File()
            self.parentbuilder().directory().add(name='CMakeLists.txt', entry=cmakelists_file)
        else:
            cmakelists_file.truncate()
            pass
        cmakelists_file.add_lines(self.__local_cmakelists.lines())
        pass

    def __output_top_cmakelists(self):
        top_cmakelists = find_cmake_output_builder(self.parentbuilder()).top_cmakelists()

        # project name and version. extract as much from confix's
        # package properties as we can.
        # FIXME: rest of the package's properties.
        top_cmakelists.set_project(self.package().name())
        top_cmakelists.add_set('VERSION', self.package().version())

        # rpath wizardry
        self.__apply_rpath_settings(top_cmakelists)

        # CPack wizardry
        self.__apply_cpack_settings(top_cmakelists)
        
        # register subdirectories with our toplevel CMakeLists.txt
        for dirnode in self.package().topo_directories():
            assert isinstance(dirnode, DirectoryBuilder)
            relpath = dirnode.directory().relpath(self.package().rootdirectory())
            if len(relpath) == 0:
                continue # don't add package root
            self.local_cmakelists().add_subdirectory('/'.join(relpath))
            pass
        pass

    def __apply_rpath_settings(self, top_cmakelists):
        # RPATH settings, according to
        # http://www.vtk.org/Wiki/CMake_RPATH_handling. this ought to
        # be the way that we know from automake/libtool.

        # use, i.e. don't skip the full RPATH for the build tree
        top_cmakelists.add_set('CMAKE_SKIP_BUILD_RPATH', 'FALSE')

        # when building, don't use the install RPATH already (but
        # later on when installing)
        top_cmakelists.add_set('CMAKE_BUILD_WITH_INSTALL_RPATH', 'FALSE')

        # the RPATH to be used when installing
        top_cmakelists.add_set('CMAKE_INSTALL_RPATH', "${CMAKE_INSTALL_PREFIX}/lib")

        # add the automatically determined parts of the RPATH which
        # point to directories outside the build tree to the install
        # RPATH
        top_cmakelists.add_set('CMAKE_INSTALL_RPATH_USE_LINK_PATH', 'TRUE')
        pass

    def __apply_cpack_settings(self, top_cmakelists):
        top_cmakelists.add_include('CPack')
        top_cmakelists.add_set('CPACK_SOURCE_PACKAGE_FILE_NAME', '"${PROJECT_NAME}-${VERSION}"')
        top_cmakelists.add_set('CPACK_SOURCE_IGNORE_FILES', "${CPACK_SOURCE_IGNORE_FILES};~\$")
        pass
    
    pass
