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

from . import makefile_utils
from . import makefile_am
from . import configure_ac
from . import output
from . import iface
from . import file_installer_suite
from . import c
from . import exe
from . import exename.suite_inmem
from . import readonly_prefixes.suite_inmem
from . import libtool
from . import buildinfo
from . import ac_config_srcdir_suite
from . import inter_package_inmem
from . import check.suite_inmem

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
