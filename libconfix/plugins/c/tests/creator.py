# Copyright (C) 2008 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.core.utils import const

import unittest

class CreatorSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CreatorTest('test'))
        pass
    pass

class CreatorTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['a'])
        fs.rootdirectory().add(name=const.CONFIX2_PKG,
                               entry=File(lines=["PACKAGE_NAME('ignore-entries-c')",
                                                 "PACKAGE_VERSION('6.6.6')"]))
        fs.rootdirectory().add(name=const.CONFIX2_DIR,
                               entry=File(lines=['IGNORE_ENTRIES(["ignored.h"])',
                                                 'IGNORE_FILE("ignored.c")']))
        fs.rootdirectory().add(name='ignored.h',
                               entry=File())
        fs.rootdirectory().add(name='ignored.c',
                               entry=File())
        fs.rootdirectory().add(name='not-ignored.h',
                               entry=File())
        
        package = LocalPackage(
            rootdirectory=fs.rootdirectory(),
            setups=[ConfixSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])

        self.failIf(package.rootbuilder().find_entry_builder(path=['ignored.h']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['ignored.c']))
        self.failUnless(package.rootbuilder().find_entry_builder(path=['not-ignored.h']))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CreatorSuite())
    pass
