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
     BuildInfo_CXXFLAGS, \
     BuildInfo_CLibrary_External

from libconfix.core.automake.buildinfo import \
     BuildInfo_ACInclude_m4, \
     BuildInfo_Configure_in
from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core.automake import helper_automake

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.buildinfoset import BuildInformationSet

class PkgConfigLibraryAdapter(Builder):
    """
    Adapter to an external library which is found using pkg-config.
    """
    def __init__(self, packagename):
        Builder.__init__(self)
        self.__packagename = packagename
        pass

    def locally_unique_id(self):
        return str(self.__class__)+':'+self.__packagename
        
    def buildinfos(self):
        ret = BuildInformationSet()
        ret.merge(super(PkgConfigLibraryAdapter, self).buildinfos())

        package_shell_name = helper_automake.automake_name(self.__packagename)

        ret.add(BuildInfo_ACInclude_m4(
            lines=[pkg_config_check]))
        ret.add(BuildInfo_Configure_in(
            lines=['CONFIX_PKG_CONFIG_LIBRARY(['+self.__packagename+'], ['+package_shell_name+'])'],
            order=Configure_ac.LIBRARIES))
        ret.add(BuildInfo_CFLAGS(
            cflags=['$('+package_shell_name+'_PKG_CONFIG_CFLAGS)']))
        ret.add(BuildInfo_CXXFLAGS(
            cxxflags=['$('+package_shell_name+'_PKG_CONFIG_CFLAGS)']))
        ret.add(BuildInfo_CLibrary_External(
            libpath=[],
            libs=['$('+package_shell_name+'_PKG_CONFIG_LIBS)']))

        return ret
    pass

pkg_config_check = """

dnl Use pkg-config to extract information out of <package-name>.pc. Output
dnl variables are ${<package-shell-name>_CFLAGS} and
dnl ${<package-shell-name>_LIBS}, which are AC_SUBST'ed
dnl 
dnl $1 ... <package-name>; package name as understood by pkg-config.
dnl 
dnl $2 ... <package-shell-name>; prefix used in output shell variable
dnl        names; be careful to craft it carefully.

AC_DEFUN([CONFIX_PKG_CONFIG_LIBRARY],
[
AC_REQUIRE([PKG_PROG_PKG_CONFIG])
AC_MSG_CHECKING([pkg-config $1 parameters])
$2_PKG_CONFIG_CFLAGS=`${PKG_CONFIG} --cflags $1`
$2_PKG_CONFIG_LIBS=`${PKG_CONFIG} --libs $1`
AC_MSG_RESULT([cflags="${$2_PKG_CONFIG_CFLAGS}"; libs="${$2_PKG_CONFIG_LIBS}"])
AC_SUBST([$2_PKG_CONFIG_CFLAGS])
AC_SUBST([$2_PKG_CONFIG_LIBS])
])

"""
