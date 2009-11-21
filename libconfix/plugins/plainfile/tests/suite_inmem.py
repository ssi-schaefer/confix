# Copyright (C) 2002-2006 Salomon Automation
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

from package import make_package

from libconfix.plugins.plainfile.builder import PlainFileBuilder
from libconfix.plugins.plainfile.setup import PlainFileInterfaceSetup

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class PlainFileSuiteInMemory(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(PlainFileInMemoryTest('test'))
        self.addTest(PlainFileCreatorParamTest('test'))
        pass
    pass

class PlainFileInMemoryTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'], rootdirectory=make_package())
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        
        plainfile_data = package.rootbuilder().find_entry_builder(['plainfile_data'])
        plainfile_prefix = package.rootbuilder().find_entry_builder(['plainfile_prefix'])
        self.failIf(plainfile_data is None)
        self.failIf(plainfile_prefix is None)
        self.failUnless(isinstance(plainfile_data, PlainFileBuilder))
        self.failUnless(isinstance(plainfile_prefix, PlainFileBuilder))
        pass
    pass

class PlainFileCreatorParamTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["from libconfix.plugins.plainfile.setup import PlainFileCreatorSetup",

                              "PACKAGE_NAME('PlainFileCreatorTest')",
                              "PACKAGE_VERSION('1.2.3')",

                              "SETUP([PlainFileCreatorSetup(",
                              "           regex=r'\.data$',",
                              "           datadir=['the', 'data', 'dir']),",
                              "       PlainFileCreatorSetup(",
                              "           regex=r'\.prefix$',",
                              "           prefixdir=['the', 'prefix', 'dir'])])"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='file.data',
            entry=File())
        fs.rootdirectory().add(
            name='file.prefix',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=None)
        package.boil(external_nodes=[])

        databuilder = package.rootbuilder().find_entry_builder(['file.data'])
        prefixbuilder = package.rootbuilder().find_entry_builder(['file.prefix'])
        self.failIf(databuilder is None)
        self.failIf(prefixbuilder is None)

        self.failUnless(databuilder.datadir() == ['the', 'data', 'dir'])
        self.failUnless(databuilder.prefixdir() is None)
        self.failUnless(prefixbuilder.prefixdir() == ['the', 'prefix', 'dir'])
        self.failUnless(prefixbuilder.datadir() is None)
        pass
    pass
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(PlainFileSuiteInMemory())
    pass
