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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

def includefile(packagename):
    return '${%s_SOURCE_DIR}/confix-admin/cmake/Modules/ConfixReadonlyPrefixes.cmake' % packagename    

class ReadonlyPrefixesSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(ReadonlyPrefixesBuilder())
        pass
    pass

class ReadonlyPrefixesBuilder(Builder):
    """
    Installs a confix helper module file in the root/confix-admin
    directory, and includes that file early in the toplevel
    CMakeLists.txt file of the package.
    """
    def locally_unique_id(self):
        return self.__class__.__name__
    def output(self):
        super(ReadonlyPrefixesBuilder, self).output()

        if self.parentbuilder() is not self.package().rootbuilder():
            return

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        cmake_output_builder.top_cmakelists().add_include(
            includefile(self.package().name()))            

        cmake_output_builder.add_module_file(
            name='ConfixReadonlyPrefixes.cmake',
            lines=[
                '# Find subdir/filename along the prefix and readonly-prefixes.',
                '# The directory where the file has been found is stored ',
                '# in the output variable "directory"',
                'FUNCTION(ConfixFindNativeInstalledFile directory filename subdir)',
                '    SET(my_path ${CMAKE_INSTALL_PREFIX}/${subdir})',
                '    FOREACH(dir ${READONLY_PREFIXES})',
                '        LIST(APPEND my_path ${dir}/${subdir})',
                '    ENDFOREACH(dir)',
                '    FIND_PATH(${directory} ${filename} PATH ${my_path} NO_DEFAULT_PATH)',
                'ENDFUNCTION(ConfixFindNativeInstalledFile)',
                '',
                'FUNCTION(ConfixFindNativeInstalledLibrary basename exename)',
                '    SET(prefixlib_list ${CMAKE_INSTALL_PREFIX}/lib)',
                '    FOREACH(prefix ${READONLY_PREFIXES})',
                '        LIST(APPEND prefixlib_list ${prefix}/lib)',
                '    ENDFOREACH(prefix)',
                '    FIND_LIBRARY(${basename}_LIBRARY ${basename} ${prefixlib_list})',
                '    IF (NOT ${basename}_LIBRARY)',
                '        MESSAGE(FATAL_ERROR "cannot find confix native installed library \'${basename}\'")',
                '    ENDIF (NOT ${basename}_LIBRARY)',
                'ENDFUNCTION(ConfixFindNativeInstalledLibrary)',
                ])
        pass
    pass
