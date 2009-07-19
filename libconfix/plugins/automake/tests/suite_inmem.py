# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from makefile_utils import MakefileUtilsSuite
from makefile_am import MakefileAmSuite
from configure_ac import ConfigureACSuite
from output import AutomakeOutputSuite
from iface import InterfaceSuite
from file_installer_suite import FileInstallerSuite
from c import CSuite
from exe import ExecutableSuite
from exename.suite_inmem import ExecutableNameInMemorySuite
import readonly_prefixes.suite_inmem
from libtool_linking import LibtoolLinkingSuite
from buildinfo import BuildInfoSuite
from ac_config_srcdir_suite import AC_CONFIG_SRCDIR_Suite
from inter_package_inmem import InterPackageInMemorySuite
from check.suite_inmem import CheckProgramInMemorySuite

from libconfix.plugins.automake.pkg_config.tests.suite_inmem import PkgConfigInMemorySuite
from libconfix.plugins.automake.c.tests.suite_inmem import AutomakeCInMemorySuite

import unittest

class AutomakeInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(MakefileUtilsSuite())
        self.addTest(MakefileAmSuite())
        self.addTest(ConfigureACSuite())
        self.addTest(AutomakeOutputSuite())
        self.addTest(InterfaceSuite())
        self.addTest(FileInstallerSuite())
        self.addTest(CSuite())
        self.addTest(ExecutableSuite())
        self.addTest(ExecutableNameInMemorySuite())
        self.addTest(readonly_prefixes.suite_inmem.InMemorySuite())
        self.addTest(LibtoolLinkingSuite())
        self.addTest(BuildInfoSuite())
        self.addTest(PkgConfigInMemorySuite())
        self.addTest(AutomakeCInMemorySuite())
        self.addTest(AC_CONFIG_SRCDIR_Suite())
        self.addTest(InterPackageInMemorySuite())
        self.addTest(CheckProgramInMemorySuite())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeInMemorySuite())
    pass
