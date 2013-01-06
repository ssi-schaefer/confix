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

from libconfix.plugins.automake.pkg_config.tests.suite_inmem import PkgConfigInMemorySuite
from libconfix.plugins.automake.c.tests.suite_inmem import AutomakeCInMemorySuite
from libconfix.plugins.automake.script.tests.suite_inmem import AutomakeScriptInMemorySuite

import unittest

class AutomakeInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(makefile_utils.suite)
        self.addTest(makefile_am.suite)
        self.addTest(configure_ac.suite)
        self.addTest(output.suite)
        self.addTest(iface.suite)
        self.addTest(file_installer_suite.suite)
        self.addTest(c.suite)
        self.addTest(exe.suite)
        self.addTest(exename.suite_inmem.suite)
        self.addTest(readonly_prefixes.suite_inmem.suite)
        self.addTest(libtool.suite)
        self.addTest(buildinfo.suite)
        self.addTest(PkgConfigInMemorySuite())
        self.addTest(AutomakeCInMemorySuite())
        self.addTest(ac_config_srcdir_suite.suite)
        self.addTest(inter_package_inmem.suite)
        self.addTest(check.suite_inmem.suite)
        self.addTest(AutomakeScriptInMemorySuite())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeInMemorySuite())
    pass
