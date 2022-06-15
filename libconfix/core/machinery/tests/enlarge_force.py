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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.setup import NullSetup
from libconfix.core.utils import const

import unittest

class EnlargeForceDummy(Builder):
    def locally_unique_id(self):
        return str(self.__class__)
    def enlarge(self):
        super(EnlargeForceDummy, self).enlarge()
        self.force_enlarge()
        pass
    pass        

class EnlargeForceTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+".once')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[NullSetup()])
        package.rootbuilder().add_builder(EnlargeForceDummy())
        self.assertRaises(LocalPackage.InfiniteLoopError, package.boil, external_nodes=[])
        pass
        
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(EnlargeForceTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass



        

