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

import unittest

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage

from libconfix.plugins.script.setup import ScriptSetup

from libconfix.testutils import find

from package import make_package

class ScriptSuiteInMemory(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ScriptInMemoryTest('test'))
        pass
    pass

class ScriptInMemoryTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'], rootdirectory=make_package())
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ScriptSetup()])
        package.boil(external_nodes=[])
        package.output()

        script = find.find_entrybuilder(rootbuilder=package.rootbuilder(), path=['script'])
        self.failIf(script is None)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ScriptSuiteInMemory())
    pass
