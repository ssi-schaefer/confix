# Copyright (C) 2009-2013 Joerg Faschingbauer

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

from intra_package_build import IntraPackageBuildSuite
from local_install_build import LocalInstallBuildSuite
from public_install_build import PublicInstallBuildSuite
from inter_package_build import InterPackageBuildSuite
from library_dependencies_build import LibraryDependenciesBuildSuite
from readonly_prefixes_build import ReadonlyPrefixesBuildSuite
from external_library_build import ExternalLibraryBuildSuite
from plainfile_build import PlainfileBuildSuite
from idl_build import IDLBuildSuite
from script_build import ScriptBuildSuite
from repo_install_build import RepoInstallBuildSuite
from generator_build import GeneratorBuildSuite
from cmake_bug_10082_build import CMakeBug10082BuildSuite
from custom_command_build import CustomCommandBuildSuite

import unittest

class CMakeBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageBuildSuite())
        self.addTest(LocalInstallBuildSuite())
        self.addTest(PublicInstallBuildSuite())
        self.addTest(InterPackageBuildSuite())
        self.addTest(LibraryDependenciesBuildSuite())
        self.addTest(ReadonlyPrefixesBuildSuite())
        self.addTest(ExternalLibraryBuildSuite())
        self.addTest(PlainfileBuildSuite())
        self.addTest(IDLBuildSuite())
        self.addTest(ScriptBuildSuite())
        self.addTest(RepoInstallBuildSuite())

        self.addTest(GeneratorBuildSuite())
        self.addTest(CMakeBug10082BuildSuite())
        self.addTest(CustomCommandBuildSuite())

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
