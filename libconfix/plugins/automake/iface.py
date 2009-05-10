# Copyright (C) 2008 Joerg Faschingbauer

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

from configure_ac import Configure_ac
from buildinfo import BuildInfo_Configure_in, BuildInfo_ACInclude_m4

from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.machinery.setup import Setup
from libconfix.core.iface.proxy import InterfaceProxy

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

        pass

    AC_BUILDINFO_TRANSPORT_LOCAL = 0
    AC_BUILDINFO_TRANSPORT_PROPAGATE = 1
    def CONFIGURE_AC(self, lines, order, flags=None):
        if type(order) not in [types.IntType or types.LongType]:
            raise Error('CONFIGURE_AC(): "order" parameter must be an integer')
        if flags is None or self.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.__dirbuilder.package().configure_ac().add_paragraph(
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
            self.__dirbuilder.package().acinclude_m4().add_paragraph(
                paragraph=Paragraph(lines=lines))
            pass
        if flags is None or self.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.__dirbuilder.add_buildinfo(BuildInfo_ACInclude_m4(
                lines=lines))
            pass
        pass

    def ADD_EXTRA_DIST(self, filename):
        self.__dirbuilder.makefile_am().add_extra_dist(filename)
        pass

    def MAKEFILE_AM(self, line):
        self.__dirbuilder.makefile_am().add_line(line)
        pass
        
    pass