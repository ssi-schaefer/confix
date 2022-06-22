# Copyright (C) 2008-2009 Joerg Faschingbauer

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

from .configure_ac import Configure_ac
from .buildinfo import BuildInfo_Configure_in, BuildInfo_ACInclude_m4
from .out_automake import find_automake_output_builder

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.interface import InterfaceProxy

import types

class AutomakeInterfaceSetup(Setup):
    def setup(self, dirbuilder):
        dirbuilder.add_interface(AutomakeInterfaceProxy(dirbuilder=dirbuilder))
        pass
    pass

class AutomakeInterfaceProxy(InterfaceProxy):
    def __init__(self, dirbuilder):
        InterfaceProxy.__init__(self)

        self.__dirbuilder = dirbuilder

        self.add_global('LOCAL', self.AC_BUILDINFO_TRANSPORT_LOCAL)
        self.add_global('PROPAGATE', self.AC_BUILDINFO_TRANSPORT_PROPAGATE)
        self.add_global('AC_BOILERPLATE', Configure_ac.BOILERPLATE)
        self.add_global('AC_OPTIONS', Configure_ac.OPTIONS)
        self.add_global('AC_PROGRAMS', Configure_ac.PROGRAMS)
        self.add_global('AC_LIBRARIES', Configure_ac.LIBRARIES)
        self.add_global('AC_HEADERS', Configure_ac.HEADERS)
        self.add_global('AC_TYPEDEFS_AND_STRUCTURES', Configure_ac.TYPEDEFS_AND_STRUCTURES)
        self.add_global('AC_FUNCTIONS', Configure_ac.FUNCTIONS)
        self.add_global('AC_OUTPUT', Configure_ac.OUTPUT)

        self.add_global('CONFIGURE_AC', getattr(self, 'CONFIGURE_AC'))
        self.add_global('ACINCLUDE_M4', getattr(self, 'ACINCLUDE_M4'))
        self.add_global('ADD_EXTRA_DIST', getattr(self, 'ADD_EXTRA_DIST'))
        self.add_global('MAKEFILE_AM', getattr(self, 'MAKEFILE_AM'))
        self.add_global('ADD_AM_CFLAGS', getattr(self, 'ADD_AM_CFLAGS'))
        self.add_global('ADD_AM_CXXFLAGS', getattr(self, 'ADD_AM_CXXFLAGS'))
        self.add_global('TESTS_ENVIRONMENT', getattr(self, 'TESTS_ENVIRONMENT'))

        pass

    AC_BUILDINFO_TRANSPORT_LOCAL = 0
    AC_BUILDINFO_TRANSPORT_PROPAGATE = 1
    def CONFIGURE_AC(self, lines, order, flags=None):
        if type(order) not in [int or int]:
            raise Error('CONFIGURE_AC(): "order" parameter must be an integer')
        if flags is None or self.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            automake_output_builder = find_automake_output_builder(self.__dirbuilder)
            assert automake_output_builder
            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(lines=lines),
                order=order)
            pass
        if flags is None or self.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_Configure_in(
                lines=lines,
                order=order))
            pass
        pass

    def ACINCLUDE_M4(self, lines, flags=None):
        if flags is None or self.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            automake_output_builder = find_automake_output_builder(self.__dirbuilder)
            assert automake_output_builder
            automake_output_builder.acinclude_m4().add_paragraph(
                paragraph=Paragraph(lines=lines))
            pass
        if flags is None or self.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_ACInclude_m4(
                lines=lines))
            pass
        pass

    def ADD_EXTRA_DIST(self, filename):
        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        assert automake_output_builder
        automake_output_builder.makefile_am().add_extra_dist(filename)
        pass

    def MAKEFILE_AM(self, line):
        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        assert automake_output_builder
        automake_output_builder.makefile_am().add_line(line)
        pass

    def ADD_AM_CFLAGS(self, str):
        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        assert automake_output_builder
        automake_output_builder.makefile_am().add_am_cflags(str)
        pass

    def ADD_AM_CXXFLAGS(self, str):
        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        assert automake_output_builder
        automake_output_builder.makefile_am().add_am_cxxflags(str)
        pass

    def TESTS_ENVIRONMENT(self, name, value):
        if type(name) is not str:
            raise Error('TESTS_ENVIRONMENT(): key must be a string')
        if type(value) is not str:
            raise Error('TESTS_ENVIRONMENT(): value must be a string')

        automake_output_builder = find_automake_output_builder(self.__dirbuilder)
        automake_output_builder.makefile_am().add_tests_environment(name, value)
        pass
        
    pass
