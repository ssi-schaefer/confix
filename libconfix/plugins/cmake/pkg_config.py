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

from external_library import ExternalLibraryBuilder
from buildinfo import BuildInfo_Toplevel_CMakeLists_FindCall

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.buildinfo import BuildInformationSet

class PkgConfigLibraryBuilder(Builder):
    def __init__(self, packagename):
        Builder.__init__(self)
        self.__packagename = packagename
        self.__bursted = False
        pass

    def locally_unique_id(self):
        return str(self.__class__)+':'+self.__packagename
    
    def enlarge(self):
        super(PkgConfigLibraryBuilder, self).enlarge()

        if self.__bursted:
            return
        self.__bursted = True

        self.parentbuilder().add_builder(
            ExternalLibraryBuilder(
                name='PkgConfig-Helper',
                incpath=['${CONFIX_CMAKE_PKG_CONFIG__%s_INCLUDE_DIRS}' % self.__packagename],
                libpath=['${CONFIX_CMAKE_PKG_CONFIG__%s_LIBRARY_DIRS}' % self.__packagename],
                libs=['${CONFIX_CMAKE_PKG_CONFIG__%s_LIBRARIES}' % self.__packagename],
                cflags=['${CONFIX_CMAKE_PKG_CONFIG__%s_CFLAGS}' % self.__packagename,
                        '${CONFIX_CMAKE_PKG_CONFIG__%s_CFLAGS_OTHER}' % self.__packagename]))
        pass

    def buildinfos(self):
        ret = BuildInformationSet()
        ret.merge(super(PkgConfigLibraryBuilder, self).buildinfos())

        ret.add(BuildInfo_Toplevel_CMakeLists_FindCall(
            find_call=['FIND_PACKAGE(PkgConfig)',
                       'PKG_CHECK_MODULES(CONFIX_CMAKE_PKG_CONFIG__%s REQUIRED %s)' % (self.__packagename, self.__packagename)]))
        return ret
    pass
    
    
