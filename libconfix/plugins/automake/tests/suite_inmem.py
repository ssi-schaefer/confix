# Copyright (C) 2006-2013 Joerg Faschingbauer

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

import makefile_utils
import makefile_am
import configure_ac
import output
import iface
import file_installer_suite
import c
import exe
import exename.suite_inmem
import readonly_prefixes.suite_inmem
import libtool
import buildinfo
import ac_config_srcdir_suite
import inter_package_inmem
import check.suite_inmem

import libconfix.plugins.automake.pkg_config.tests.suite_inmem
import libconfix.plugins.automake.c.tests.suite_inmem
import libconfix.plugins.automake.script.tests.suite_inmem

import unittest

suite = unittest.TestSuite()
suite.addTest(makefile_utils.suite)
suite.addTest(makefile_am.suite)
suite.addTest(configure_ac.suite)
suite.addTest(output.suite)
suite.addTest(iface.suite)
suite.addTest(file_installer_suite.suite)
suite.addTest(c.suite)
suite.addTest(exe.suite)
suite.addTest(exename.suite_inmem.suite)
suite.addTest(readonly_prefixes.suite_inmem.suite)
suite.addTest(libtool.suite)
suite.addTest(buildinfo.suite)
suite.addTest(libconfix.plugins.automake.pkg_config.tests.suite_inmem.suite)
suite.addTest(libconfix.plugins.automake.c.tests.suite_inmem.suite)
suite.addTest(ac_config_srcdir_suite.suite)
suite.addTest(inter_package_inmem.suite)
suite.addTest(check.suite_inmem.suite)
suite.addTest(libconfix.plugins.automake.script.tests.suite_inmem.suite)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
