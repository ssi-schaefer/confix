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

from buildinfo import BuildInfo_IncludePath_External_CMake
from buildinfo import BuildInfo_LibraryPath_External_CMake
from buildinfo import BuildInfo_Library_External_CMake
from buildinfo import BuildInfo_CommandlineMacros_CMake
from buildinfo import BuildInfo_CFLAGS_CMake
from buildinfo import BuildInfo_CXXFLAGS_CMake

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.buildinfo import BuildInformationSet

class ExternalLibraryBuilder(Builder):
    def __init__(self,
                 name=None,
                 incpath=[],
                 libpath=[],
                 libs=[],
                 cflags=[],
                 cxxflags=[],
                 cmdlinemacros={}):
        Builder.__init__(self)

        self.__name = name
        self.__incpath = incpath
        self.__libpath = libpath
        self.__libs = libs
        self.__cflags = cflags
        self.__cxxflags = cxxflags
        self.__cmdlinemacros = cmdlinemacros
        pass

    def locally_unique_id(self):
        id = str(self.__class__)
        if self.__name is not None:
            id += ':'+self.__name
            pass
        return id

    def buildinfos(self):
        ret = BuildInformationSet()
        ret.merge(super(ExternalLibraryBuilder, self).buildinfos())
        
        if len(self.__incpath) > 0:
            ret.add(BuildInfo_IncludePath_External_CMake(incpath=self.__incpath))
            pass
        if len(self.__libpath) > 0:
            ret.add(BuildInfo_LibraryPath_External_CMake(libpath=self.__libpath))
            pass
        if len(self.__libs) > 0:
            ret.add(BuildInfo_Library_External_CMake(libs=self.__libs))
            pass
        if len(self.__cmdlinemacros) > 0:
            ret.add(BuildInfo_CommandlineMacros_CMake(macros=self.__cmdlinemacros))
            pass
        if len(self.__cflags) > 0:
            ret.add(BuildInfo_CFLAGS_CMake(cflags=self.__cflags))
            pass
        if len(self.__cxxflags) > 0:
            ret.add(BuildInfo_CXXFLAGS_CMake(cxxflags=self.__cxxflags))
            pass
        return ret

    pass
