# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2012 Joerg Faschingbauer

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

from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.testutils import dirhier

import unittest
import types

class BasicDirectorySetup(unittest.TestCase):

    def test(self):
        fs = dirhier.packageroot()
        subdir = dirhier.subdir(parent=fs.rootdirectory(), name='a')
        subsubdir = dirhier.subdir(parent=subdir, name='a')
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ImplicitDirectorySetup()])
        package.boil(external_nodes=[])

        self.assertEqual(package.rootbuilder().directory().find(['a']), subdir)
        self.assertEqual(package.rootbuilder().directory().find(['a', 'a']), subsubdir)
        
        subdir_builder = package.rootbuilder().find_entry_builder(['a'])
        self.failIf(subdir_builder is None)
        
        subsubdir_builder = package.rootbuilder().find_entry_builder(['a','a'])
        self.failIf(subsubdir_builder is None)

        self.assertEqual(subdir_builder.directory(), subdir)
        self.assertEqual(subsubdir_builder.directory(), subsubdir)

        pass

    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(BasicDirectorySetup))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
