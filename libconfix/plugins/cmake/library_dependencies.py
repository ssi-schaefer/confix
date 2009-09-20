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
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeInstalled

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder

class LibraryDependenciesSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(LibraryDependenciesBuilder())
        pass
    pass

class LibraryDependenciesBuilder(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def output(self):
        super(LibraryDependenciesBuilder, self).output()

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())
        found_exe = False

        for exe in self.parentbuilder().iter_builders():
            if not isinstance(exe, ExecutableBuilder):
                continue
            found_exe = True
            for bi in exe.topo_libraries():
                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    cmake_output_builder.top_cmakelists().add_include(
                        '${'+self.package().name()+'_SOURCE_DIR}/'
                        'confix-admin/cmake/Modules/ConfixFindNativeInstalledLibrary.cmake')
                    cmake_output_builder.top_cmakelists().add_find_call(
                        'ConfixFindNativeInstalledLibrary('+bi.basename()+')')
                    cmake_output_builder.local_cmakelists().tighten_target_link_library(
                        target=exe.exename(),
                        basename=bi.basename(),
                        tightened='${'+bi.basename()+'_LIBRARY}')
                    pass
                pass
            pass

        if found_exe:
            cmake_output_builder.add_module_file(
                name='ConfixFindNativeInstalledLibrary.cmake',
                lines=['FUNCTION(ConfixFindNativeInstalledLibrary basename)',
                       '    SET(prefixlib_list ${CMAKE_INSTALL_PREFIX}/lib)',
                       '    FOREACH(prefix ${READONLY_PREFIXES})',
                       '        LIST(APPEND prefixlib_list ${prefix}/lib)',
                       '    ENDFOREACH(prefix)',
                       '    FIND_LIBRARY(${basename}_LIBRARY ${basename} ${prefixlib_list})',
                       '    IF (${basename}_LIBRARY)',
                       '        MESSAGE(STATUS "found confix native installed library \'${${basename}_LIBRARY}\'")',
                       '    ELSE (${basename}_LIBRARY)',
                       '        MESSAGE(FATAL_ERROR "cannot find confix native installed library \'${basename}\'")',
                       '    ENDIF (${basename}_LIBRARY)',
                       'ENDFUNCTION(ConfixFindNativeInstalledLibrary)'])
            pass
        pass
    pass

