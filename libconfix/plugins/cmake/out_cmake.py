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
from modules_dir_builder import ModulesDirectoryBuilder
from external_library import BuildInfo_Toplevel_CMakeLists_Include
from external_library import BuildInfo_Toplevel_CMakeLists_FindCall

from libconfix.core.machinery.builder import Builder
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.hierarchy import confix_admin
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

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
        self.__modules_builder = None
        self.__bursted = False
        pass

    def local_cmakelists(self):
        return self.__local_cmakelists

    def top_cmakelists(self):
        return self.__top_cmakelists

    def add_module_file(self, name, lines):
        self.__modules_builder.add_module_file(name, lines)
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def initialize(self, package):
        super(CMakeBackendOutputBuilder, self).initialize(package)

        # CMakeLists.txt files all over
        self.__local_cmakelists = CMakeLists()
        if self.parentbuilder() is package.rootbuilder():
            self.__top_cmakelists = self.__local_cmakelists
            pass
        else:
            top_cmake_builder = find_cmake_output_builder(package.rootbuilder())
            self.__top_cmakelists = top_cmake_builder.local_cmakelists()
            pass
        pass

        # if in the top directory, add the CMake admin section to
        # confix-admin. if not in the top directory, steal it from
        # there.
        if self.parentbuilder() is self.package().rootbuilder():
            # create the directory hierarchy if necessary.
            admin_dir_builder = confix_admin.add_confix_admin(self.package())
            cmake_dir = admin_dir_builder.directory().get('cmake')
            if cmake_dir is None:
                cmake_dir = admin_dir_builder.directory().add(name='cmake', entry=Directory())
                pass
            modules_dir = cmake_dir.get('Modules')
            if modules_dir is None:
                modules_dir = cmake_dir.add(name='Modules', entry=Directory())
                pass

            # wrap builder hierarchy around directory hierarchy. NOTE
            # that the modules directory builder is a backend builder.
            cmake_dir_builder = admin_dir_builder.add_builder(DirectoryBuilder(directory=cmake_dir))
            self.__modules_builder = cmake_dir_builder.add_backend_dirbuilder(ModulesDirectoryBuilder(directory=modules_dir))
        else:
            self.__modules_builder = find_cmake_output_builder(self.package().rootbuilder()).__modules_builder
            pass
        pass

    def relate(self, node, digraph, topolist):
        super(CMakeBackendOutputBuilder, self).relate(node, digraph, topolist)

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_Toplevel_CMakeLists_Include):
                    self.__top_cmakelists.add_include(bi.include())
                    continue
                if isinstance(bi, BuildInfo_Toplevel_CMakeLists_FindCall):
                    self.__top_cmakelists.add_find_call(bi.find_call())
                    continue
                pass
            pass
        pass
                    
    def output(self):
        # if in the top directory, our CMakeLists.txt file needs to
        # contain a lot of boilerplate things, in addition to its
        # regular module content.
        if self.parentbuilder() is self.package().rootbuilder():
            self.__output_top_cmakelists()
            pass

        # write the CMakeLists.txt file.
        cmakelists_file = self.parentbuilder().directory().find(['CMakeLists.txt'])
        if cmakelists_file is None:
            cmakelists_file = File()
            self.parentbuilder().directory().add(name='CMakeLists.txt', entry=cmakelists_file)
        else:
            cmakelists_file.truncate()
            pass
        cmakelists_file.add_lines(self.__local_cmakelists.lines())

        # NOTE: this has to come last because we add stuff to the
        # ModulesDirectoryBuilder, and he has to come after us.
        super(CMakeBackendOutputBuilder, self).output()
        pass

    def __output_top_cmakelists(self):
        top_cmakelists = find_cmake_output_builder(self.parentbuilder()).top_cmakelists()

        # project name and version. extract as much from confix's
        # package properties as we can.
        # FIXME: rest of the package's properties.
        top_cmakelists.set_project(self.package().name())
        top_cmakelists.add_set('VERSION', self.package().version())

        # CMake requires us to write something like that.
        top_cmakelists.add_cmake_minimum_required('VERSION', '2.6')

        # in case we add our own modules, point the include path
        # there.
        top_cmakelists.add_set(
            'CMAKE_MODULE_PATH',
            '${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/%s/cmake/Modules"' % const.ADMIN_DIR)

        # rpath wizardry
        self.__apply_rpath_settings(top_cmakelists)

        # CPack wizardry
        self.__apply_cpack_settings(top_cmakelists)

        # piggy-back repo install
        top_cmakelists.add_install__files(
            files=[self.package().repofilename()],
            destination='share/confix2/repo')
        
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

        # version information.
        version_parts = self.package().version().split('.')
        if (len(version_parts) >= 1):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_MAJOR', version_parts[0])
            pass
        if (len(version_parts) >= 2):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_MINOR', version_parts[1])
            pass
        if (len(version_parts) >= 3):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_PATCH', version_parts[2])
            pass
        
        pass

    def __apply_cpack_settings(self, top_cmakelists):
        top_cmakelists.add_include('CPack')
        top_cmakelists.add_set('CPACK_SOURCE_PACKAGE_FILE_NAME', '"${PROJECT_NAME}-${VERSION}"')
        top_cmakelists.add_set('CPACK_SOURCE_IGNORE_FILES', "${CPACK_SOURCE_IGNORE_FILES};~\$")
        pass
    
    pass
