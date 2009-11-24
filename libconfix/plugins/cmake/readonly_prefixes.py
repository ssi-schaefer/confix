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

from out_cmake import find_cmake_output_builder

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import Setup

class ReadonlyPrefixesSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_builder(ReadonlyPrefixesBuilder())
        pass
    pass

class ReadonlyPrefixesBuilder(Builder):
    """
    Installs the module file in confix-admin.
    """
    def locally_unique_id(self):
        return self.__class__.__name__
    def output(self):
        super(ReadonlyPrefixesBuilder, self).output()

        if self.parentbuilder() is not self.package().rootbuilder():
            return

        cmake_output_builder = find_cmake_output_builder(self.parentbuilder())

        cmake_output_builder.add_module_file(
            name='ConfixReadonlyPrefixes.cmake',
            lines=['FUNCTION(ConfixFindNativeInstalledLibrary basename exename)',
                   '    SET(prefixlib_list ${CMAKE_INSTALL_PREFIX}/lib)',
                   '    FOREACH(prefix ${READONLY_PREFIXES})',
                   '        LIST(APPEND prefixlib_list ${prefix}/lib)',
                   '    ENDFOREACH(prefix)',
                   '    FIND_LIBRARY(${basename}_LIBRARY ${basename} ${prefixlib_list})',
                   '    IF (${basename}_LIBRARY)',
                   '        MESSAGE(STATUS "add dependency ${exename} -> ${${basename}_LIBRARY}")',
                   '    ELSE (${basename}_LIBRARY)',
                   '        MESSAGE(FATAL_ERROR "cannot find confix native installed library \'${basename}\'")',
                   '    ENDIF (${basename}_LIBRARY)',
                   'ENDFUNCTION(ConfixFindNativeInstalledLibrary)'])
        pass
    pass
