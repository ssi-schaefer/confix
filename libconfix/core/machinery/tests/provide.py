# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

class ProvideSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ProvideStringUpdateTest('test'))
        pass
    pass

class ProvideStringUpdateTest(unittest.TestCase):

    # one day I tried to eliminate Provide_String.update() and didn't
    # see from the tests that it was needed. now I see.
    
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ProvideStringUpdateTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('aaa')",
                              "PROVIDE_SYMBOL('aaa')"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[])
        package.boil(external_nodes=[])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ProvideSuite())
    pass

