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
from external_library import ExternalLibraryBuilder
from external_library import BuildInfo_Toplevel_CMakeLists_Include
from external_library import BuildInfo_Toplevel_CMakeLists_FindCall

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

import types

class CMakeInterfaceSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(CMakeInterfaceProxy(dirbuilder=dirbuilder))
        pass
    pass

class CMakeInterfaceProxy(InterfaceProxy):

    CMAKE_BUILDINFO_PROPAGATE = 0
    CMAKE_BUILDINFO_LOCAL = 1

    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)

        self.__dirbuilder = dirbuilder

        self.add_global('CMAKE_BUILDINFO_PROPAGATE', getattr(self, 'CMAKE_BUILDINFO_PROPAGATE'))
        self.add_global('CMAKE_BUILDINFO_LOCAL', getattr(self, 'CMAKE_BUILDINFO_LOCAL'))

        self.add_global('CMAKE_CMAKELISTS_ADD_INCLUDE', getattr(self, 'CMAKE_CMAKELISTS_ADD_INCLUDE'))
        self.add_global('CMAKE_ADD_CONFIX_MODULE', getattr(self, 'CMAKE_ADD_CONFIX_MODULE'))
        self.add_global('CMAKE_CMAKELISTS_ADD_FIND_CALL', getattr(self, 'CMAKE_CMAKELISTS_ADD_FIND_CALL'))
        self.add_global('CMAKE_EXTERNAL_LIBRARY', getattr(self, 'CMAKE_EXTERNAL_LIBRARY'))
        pass

    def CMAKE_CMAKELISTS_ADD_INCLUDE(self, include, flags):
        if type(include) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE(): "include" parameter must be a string')
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_INCLUDE(): "flags" parameter must be list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).top_cmakelists().add_include(include)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_Toplevel_CMakeLists_Include(include=include))
            pass
        pass

    def CMAKE_ADD_CONFIX_MODULE(self, name, lines):
        find_cmake_output_builder(self.__dirbuilder).add_module_file(name, lines)
        pass

    def CMAKE_CMAKELISTS_ADD_FIND_CALL(self, find_call, flags):
        if type(find_call) is not str:
            raise Error('CMAKE_CMAKELISTS_ADD_FIND_CALL(): "find_call" parameter must be a string')
        if type(flags) is int:
            flags = (flags,)
            pass
        if type(flags) not in (tuple, list):
            raise Error('CMAKE_CMAKELISTS_ADD_FIND_CALL(): "flags" parameter must be list or tuple')
        if self.CMAKE_BUILDINFO_LOCAL in flags:
            find_cmake_output_builder(self.__dirbuilder).top_cmakelists().add_find_call(find_call)
            pass
        if self.CMAKE_BUILDINFO_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_Toplevel_CMakeLists_FindCall(find_call=find_call))
            pass
        pass

    def CMAKE_EXTERNAL_LIBRARY(self, incpath=[], libpath=[], libs=[], cmdlinemacros={}):
        if type(incpath) is not types.ListType:
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'incpath' argument must be a list")
        if type(libpath) is not types.ListType:
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'libpath' argument must be a list")
        if type(libs) is not types.ListType:
            raise Error("CMAKE_EXTERNAL_LIBRARY(): 'libs' argument must be a list")
        if type(cmdlinemacros) is not types.DictionaryType:
            raise Error("EXTERNAL_LIBRARY(): 'cmdlinemacros' argument must be a dictionary")

        self.__dirbuilder.add_builder(
            ExternalLibraryBuilder(incpath=incpath, libpath=libpath, libs=libs, cmdlinemacros=cmdlinemacros))
        pass

    pass
