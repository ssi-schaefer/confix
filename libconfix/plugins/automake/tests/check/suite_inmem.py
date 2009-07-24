# Copyright (C) 2002-2006 Salomon Automation
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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class CheckProgramInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CheckProgramInMemory('test_with_implicit_setup'))
        self.addTest(CheckProgramInMemory('test_with_explicit_setup'))
        pass
    pass

class CheckProgramInMemory(unittest.TestCase):
    def test_with_implicit_setup(self):
        filesys = FileSystem(path=[])
        filesys.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest")',
                              'PACKAGE_VERSION("1.2.3")']))
        filesys.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')"]))
        filesys.rootdirectory().add(
            name='_check_proggy.c',
            entry=File(lines=['int main(void) {}']))
        
        package = LocalPackage(rootdirectory=filesys.rootdirectory(),
                               setups=ConfixSetup(use_libtool=False, short_libnames=False))
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)
        
        self.failUnless('CheckProgramTest__check_proggy' in rootdir_output_builder.makefile_am().check_programs())
        self.failUnlessEqual(len(rootdir_output_builder.makefile_am().tests_environment()), 1)
        self.failUnlessEqual(rootdir_output_builder.makefile_am().tests_environment()['name'], 'value')
        pass

    def test_with_explicit_setup(self):
        filesys = FileSystem(path=[])
        filesys.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest")',
                              'PACKAGE_VERSION("1.2.3")']))
        filesys.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')",
                              "EXECUTABLE(center=C(filename='main.c'),",
                              "           exename='the-test-program',",
                              "           what=EXECUTABLE_CHECK)"]))
        filesys.rootdirectory().add(
            name='main.c',
            entry=File(lines=['int main(void) {}']))

        package = LocalPackage(rootdirectory=filesys.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)
        
        self.failUnless('the-test-program' in rootdir_output_builder.makefile_am().check_programs())
        self.failUnlessEqual(len(rootdir_output_builder.makefile_am().tests_environment()), 1)
        self.failUnlessEqual(rootdir_output_builder.makefile_am().tests_environment()['name'], 'value')
    
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CheckProgramInMemorySuite())
    pass

