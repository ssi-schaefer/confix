# Copyright (C) 2008-2013 Joerg Faschingbauer

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
from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage

import unittest

class AC_CONFIG_SRCDIR_Suite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(NoFiles('test'))
        self.addTest(NonTrivialFiles('test'))
        pass
    pass

class AC_CONFIG_SRCDIR_Test(unittest.TestCase):
    def test__no_files(self):
        fs = FileSystem(path=['dont', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_automake_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_automake_builder is None)

        self.failIf(rootdir_automake_builder.configure_ac().unique_file_in_srcdir() is None)
        self.failUnless(rootdir_automake_builder.configure_ac().unique_file_in_srcdir() in ('Confix2.dir', 'Confix2.pkg'))

        pass
        
    def test__nontrivial_files(self):
        fs = FileSystem(path=['dont', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['H("file.h")']))
        fs.rootdirectory().add(
            name='file.h',
            entry=File())
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_automake_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_automake_builder is None)

        self.failIf(rootdir_automake_builder.configure_ac().unique_file_in_srcdir() is None)
        self.failUnless(rootdir_automake_builder.configure_ac().unique_file_in_srcdir() == 'file.h')

        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(AC_CONFIG_SRCDIR_Test)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
