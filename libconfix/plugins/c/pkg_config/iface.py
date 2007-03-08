# Copyright (C) 2007 Joerg Faschingbauer

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

from libconfix.plugins.c.buildinfo import \
     BuildInfo_CFLAGS, \
     BuildInfo_CLibrary_External

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.automake.buildinfo import \
     BuildInfo_ACInclude_m4, \
     BuildInfo_Configure_in
from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core.automake import helper_automake

from libconfix.core.utils.error import Error

class PKG_CONFIG_LIBRARY_InterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.__object = object
        self.add_global('PKG_CONFIG_LIBRARY', getattr(self, 'PKG_CONFIG_LIBRARY'))
        pass

    def PKG_CONFIG_LIBRARY(self, package):
        if type(package) is not str:
            raise Error("PKG_CONFIG_LIBRARY(): argument 'package' must be a string")
        self.__object.add_buildinfo(BuildInfo_ACInclude_m4(
            lines=[pkg_config_check]))
        self.__object.add_buildinfo(BuildInfo_Configure_in(
            lines=['CONFIX_PKG_CONFIG_LIBRARY('+package+')'],
            order=Configure_ac.LIBRARIES))
        self.__object.add_buildinfo(BuildInfo_CFLAGS(
            cflags=['$('+helper_automake.automake_name(package)+'_PKG_CONFIG_CFLAGS)']))
        self.__object.add_buildinfo(BuildInfo_CLibrary_External(
            libpath=[],
            libs=['$('+helper_automake.automake_name(package)+'_PKG_CONFIG_LIBS)']))
        pass
    pass

pkg_config_check = """

AC_DEFUN([CONFIX_PKG_CONFIG_LIBRARY],
[
AC_REQUIRE(PKG_PROG_PKG_CONFIG)
$1_PKG_CONFIG_CFLAGS=`${PKG_CONFIG} --cflags`
$1_PKG_CONFIG_LIBS=`${PKG_CONFIG} --libs`
])

"""
