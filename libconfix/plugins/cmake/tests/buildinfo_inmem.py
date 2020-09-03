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

from libconfix.plugins.cmake.buildinfo import BuildInfo_CMakeModule
from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder
from libconfix.plugins.c.setups.explicit_setup import ExplicitCSetup
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

import unittest

class BuildInformationTest(unittest.TestCase):
    def test__confix_module_propagate(self):
        fs = FileSystem(path=[])
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())

        distributor = source.add(
            name='distributor',
            entry=Directory())
        distributor.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('distributor')",
                              "PACKAGE_VERSION('1.2.3')"]))
        distributor.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('distributor')",
                              "CMAKE_ADD_MODULE_FILE(",
                              "    name='TestModule.cmake',"
                              "    lines=['The-TestModule-Content'],",
                              "    flags=CMAKE_BUILDINFO_PROPAGATE)"]))

        distributor_package = LocalPackage(rootdirectory=distributor,
                                           setups=[ExplicitDirectorySetup(), CMakeSetup()])
        distributor_package.boil(external_nodes=[])


        receiver = source.add(
            name='receiver',
            entry=Directory())
        receiver.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('receiver')",
                              "PACKAGE_VERSION('1.2.3')"]))
        receiver.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('distributor', URGENCY_ERROR)"]))

        receiver_package = LocalPackage(rootdirectory=receiver,
                                        setups=[ExplicitDirectorySetup(), CMakeSetup()])
        receiver_package.boil(external_nodes=distributor_package.install().nodes())
        receiver_package.output()

        modfile = receiver.find(['confix-admin', 'cmake', 'Modules', 'TestModule.cmake'])
        self.failUnless(modfile)
        self.failUnlessEqual(modfile.lines()[0], 'The-TestModule-Content')
        
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(BuildInformationTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
