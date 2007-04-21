# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import os, types

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.provide_string import Provide_String
from libconfix.core.machinery.require import Require
from libconfix.core.machinery.setup import Setup
from libconfix.core.utils.error import Error

from dependency import \
     Provide_CInclude, \
     Require_CInclude

from buildinfo import \
    BuildInfo_CIncludePath_External, \
    BuildInfo_CFLAGS, \
    BuildInfo_CXXFLAGS, \
    BuildInfo_CommandlineMacros, \
    BuildInfo_CLibrary_External

class EXTERNAL_LIBRARY_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('EXTERNAL_LIBRARY', getattr(self, 'EXTERNAL_LIBRARY'))
        pass

    def EXTERNAL_LIBRARY(
        self,
        incpath=[],
        cflags=[],
        cxxflags=[],
        cmdlinemacros={},
        libpath=[],
        libs=[]):

        if type(incpath) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'incpath' argument must be a list")
        if type(cflags) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'cflags' argument must be a list")
        if type(cxxflags) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'cxxflags' argument must be a list")
        if type(cmdlinemacros) is not types.DictionaryType:
            raise Error("EXTERNAL_LIBRARY(): 'cmdlinemacros' argument must be a dictionary")
        if type(libpath) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'libpath' argument must be a list")
        if type(libs) is not types.ListType:
            raise Error("EXTERNAL_LIBRARY(): 'libs' argument must be a list")

        if len(incpath) > 0:
            self.__object.add_buildinfo(
                BuildInfo_CIncludePath_External(incpath=incpath))
            pass
        if len(cflags) > 0:
            self.__object.add_buildinfo(
                BuildInfo_CFLAGS(cflags=cflags))
            pass
        if len(cxxflags) > 0:
            self.__object.add_buildinfo(
                BuildInfo_CXXFLAGS(cxxflags=cxxflags))
            pass
        if len(cmdlinemacros) > 0:
            self.__object.add_buildinfo(
                BuildInfo_CommandlineMacros(macros=cmdlinemacros))
            pass
        if len(libpath) > 0 or len(libs) > 0:
            self.__object.add_buildinfo(
                BuildInfo_CLibrary_External(libpath=libpath, libs=libs))
            pass
        pass
    pass

class REQUIRE_H_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object

        self.add_global('REQUIRE_H', getattr(self, 'REQUIRE_H'))
        pass
    def REQUIRE_H(self, filename, urgency=Require.URGENCY_IGNORE):
        if not filename:
            raise Error("REQUIRE_H(): need a non-null 'filename' parameter")
        if type(filename) is not types.StringType:
            raise Error("REQUIRE_H(): 'filename' parameter must be a string")
        if len(filename)==0:
            raise Error("REQUIRE_H(): need a non-zero 'filename' parameter")
        if not urgency in [Require.URGENCY_IGNORE, Require.URGENCY_WARN, Require.URGENCY_ERROR]:
            raise Error('REQUIRE_H(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
        self.__object.add_require(Require_CInclude(
            filename=filename,
            found_in=str(self.__object),
            urgency=urgency))
        pass
    
    pass

class PROVIDE_H_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('PROVIDE_H', getattr(self, 'PROVIDE_H'))
        pass
    def PROVIDE_H(self, filename, match=Provide_String.AUTO_MATCH):
        if not filename or len(filename)==0:
            raise Error('PROVIDE_H(): need a non-zero filename parameter')
        if match not in [Provide_String.EXACT_MATCH,
                         Provide_String.PREFIX_MATCH,
                         Provide_String.GLOB_MATCH,
                         Provide_String.AUTO_MATCH]:
            raise Error('PROVIDE_H(): match parameter must be one of EXACT_MATCH, PREFIX_MATCH, GLOB_MATCH, AUTO_MATCH')
        self.__object.add_provide(Provide_CInclude(filename, match))
        pass
    pass

class TESTS_ENVIRONMENT_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('TESTS_ENVIRONMENT', getattr(self, 'TESTS_ENVIRONMENT'))
        pass
    def TESTS_ENVIRONMENT(self, name, value):
        if type(name) is not types.StringType:
            raise Error('TESTS_ENVIRONMENT(): key must be a string')
        if type(value) is not types.StringType:
            raise Error('TESTS_ENVIRONMENT(): value must be a string')
        self.__object.parentbuilder().makefile_am().add_tests_environment(name, value)
        pass
    pass
