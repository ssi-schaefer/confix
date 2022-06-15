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

import unittest

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

class IgnoredEntriesTest(unittest.TestCase):

    # a regression I had one day. turned out that IGNORE_FILE() passed
    # a string to DirectoryBuilder's add_ignored_entries() which
    # expects a list.
    
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('IgnoredEntriesTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["IGNORE_FILE('x.cc')"]))
        fs.rootdirectory().add(
            name='x.cc',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        self.assertFalse(package.rootbuilder().find_entry_builder(['x.cc']) is not None)
        pass
    pass

class NoInternalRequiresTest(unittest.TestCase):

    # a node must eliminate require objects that can be resolved
    # internally, before it gets to dependency calculation.
    
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('NoInternalRequiresTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='file1.h',
            entry=File(lines=["#include <file2.h>"]))
        fs.rootdirectory().add(
            name='file2.h',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        self.assertFalse(len(package.rootbuilder().requires()) != 0)
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(IgnoredEntriesTest))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NoInternalRequiresTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

