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

from simple_build import SimpleBuildSuite
from kde_hack import KDEHackTestSuiteBuild
from autoconf_archive import AutoConfArchiveSuite
from exename.suite_build import ExecutableNameBuildSuite
from readonly_prefixes.suite_build import ReadonlyPrefixesBuildSuite
from interix_link import InterixLinkSuite
from inter_package_build import InterPackageBuildSuite
from intra_package_build import IntraPackageBuildSuite
from check.suite_build import CheckProgramBuildSuite
from relocated_headers.suite_build import RelocatedHeadersBuildSuite
from explicit_package_build import ExplicitPackageBuildSuite

from libconfix.plugins.automake.c.tests.suite_build import AutomakeCBuildSuite
from libconfix.plugins.automake.plainfile.tests.suite_build import AutomakePlainfileBuildSuite
from libconfix.plugins.automake.tests.idl_build import AutomakeIDLBuildSuite

import unittest

class AutomakeBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(SimpleBuildSuite())
        self.addTest(KDEHackTestSuiteBuild())
        self.addTest(AutoConfArchiveSuite())
        self.addTest(ExecutableNameBuildSuite())
        self.addTest(ReadonlyPrefixesBuildSuite())
        self.addTest(InterixLinkSuite())
        self.addTest(AutomakeCBuildSuite())
        self.addTest(InterPackageBuildSuite())
        self.addTest(IntraPackageBuildSuite())
        self.addTest(CheckProgramBuildSuite())
        self.addTest(RelocatedHeadersBuildSuite())
        self.addTest(ExplicitPackageBuildSuite())
        self.addTest(AutomakePlainfileBuildSuite())
        self.addTest(AutomakeIDLBuildSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(AutomakeBuildSuite())
    pass
