# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import unittest

from automake.suite_inmem import AutomakeCSuiteInMemory

from provide_require import Provide_CInclude_and_Require_CInclude_Suite
from setup_library import LibrarySetupSuite
from setup_exe import ExecutableSetupSuite
from setup_cxx import CXXSetupSuite
from setup_lexyacc import LexYaccSetupSuite
from main_search import MainSearchSuite
from name_mangling import NameManglingSuite
from requires import RequireTestSuite
from default_installer import DefaultInstallerSuite
from graph_installer import GraphInstallerSuite
from relate import RelateSuite
from buildinfo import BuildInfoSuite
from confix2_dir import Confix2_dir_Suite
from inter_package_inmem import InterPackageInMemorySuite
from misc import MiscellaneousSuite

class CTestSuiteInMemory(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        self.addTest(Provide_CInclude_and_Require_CInclude_Suite())
        self.addTest(LibrarySetupSuite())
        self.addTest(ExecutableSetupSuite())
        self.addTest(CXXSetupSuite())
        self.addTest(LexYaccSetupSuite())
        self.addTest(MainSearchSuite())
        self.addTest(NameManglingSuite())
        self.addTest(RequireTestSuite())
        self.addTest(DefaultInstallerSuite())
        self.addTest(GraphInstallerSuite())
        self.addTest(RelateSuite())
        self.addTest(BuildInfoSuite())
        self.addTest(Confix2_dir_Suite())
        self.addTest(InterPackageInMemorySuite())
        self.addTest(MiscellaneousSuite())

        self.addTest(AutomakeCSuiteInMemory())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CTestSuiteInMemory())
    pass
