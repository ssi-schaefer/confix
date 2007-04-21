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

import os
import shutil
import sys
import unittest

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils.error import Error

from libconfix.plugins.c.setups.default_setup import DefaultCSetup

from libconfix.testutils import packages, find

class IntraPackageInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageInMemoryTest('test_includepath'))
        pass
    pass

class IntraPackageInMemoryTest(unittest.TestCase):
    def setUp(self):
        self.fs_ = FileSystem(path=['x'],
                              rootdirectory=packages.lo_hi1_hi2_highest_exe(name='self.__class__.__name__',
                                                                            version='1.2.3'))
        
        self.package_ = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                                     setups=[DefaultDirectorySetup(),
                                             DefaultCSetup(short_libnames=False,
                                                    use_libtool=False)])
        self.package_.boil(external_nodes=[])
        self.package_.output()
        pass

    def test_includepath(self):
        hi1 = find.find_entrybuilder(rootbuilder=self.package_.rootbuilder(), path=['hi1'])
        self.failUnless('-I$(top_builddir)/confix_include' in hi1.makefile_am().includepath())
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageInMemorySuite())
    pass

