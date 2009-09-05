# Copyright (C) 2009 Joerg Faschingbauer

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

import unittest

class CMakeCBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageBuildSuite())
        self.addTest(LocalInstallBuildSuite())
        self.addTest(PublicInstallBuildSuite())
        self.addTest(InterPackageBuildSuite())
        self.addTest(LibraryDependenciesBuildSuite())
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CMakeCBuildSuite())
    pass
