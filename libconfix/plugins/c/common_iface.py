# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from dependency import \
     Provide_CInclude, \
     Require_CInclude

from buildinfo import \
    BuildInfo_CFLAGS, \
    BuildInfo_CXXFLAGS, \
    BuildInfo_CommandlineMacros

# jjj remove automake dependency
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.require import Require
from libconfix.core.machinery.setup import Setup
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.utils.error import Error

import os, types

class REQUIRE_H(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)
        self.__builder = builder
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
        self.__builder.add_require(Require_CInclude(
            filename=filename,
            found_in=str(self.__builder),
            urgency=urgency))
        pass
    pass

class PROVIDE_H(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)
        self.__builder = builder
        self.add_global('PROVIDE_H', getattr(self, 'PROVIDE_H'))
        pass
    def PROVIDE_H(self, filename, match=Provide.AUTO_MATCH):
        if not filename or len(filename)==0:
            raise Error('PROVIDE_H(): need a non-zero filename parameter')
        if match not in [Provide.EXACT_MATCH,
                         Provide.GLOB_MATCH,
                         Provide.AUTO_MATCH]:
            raise Error('PROVIDE_H(): match parameter must be one of EXACT_MATCH, GLOB_MATCH, AUTO_MATCH')
        self.__builder.add_provide(Provide_CInclude(filename, match))
        pass
    pass

class TESTS_ENVIRONMENT(InterfaceProxy):
    def __init__(self, dirbuilder):
        assert isinstance(dirbuilder, DirectoryBuilder)
        InterfaceProxy.__init__(self)
        self.__dirbuilder = dirbuilder
        self.add_global('TESTS_ENVIRONMENT', getattr(self, 'TESTS_ENVIRONMENT'))
        pass
    def TESTS_ENVIRONMENT(self, name, value):
        if type(name) is not types.StringType:
            raise Error('TESTS_ENVIRONMENT(): key must be a string')
        if type(value) is not types.StringType:
            raise Error('TESTS_ENVIRONMENT(): value must be a string')

        # jjj this is coupled to automake, but should rather be
        # anonymous. CMake as well may have the functionality of
        # providing tests with an enviroment.

        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        automake_output_builder.makefile_am().add_tests_environment(name, value)
        pass
    pass
