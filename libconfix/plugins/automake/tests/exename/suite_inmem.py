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

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class ExecutableNameInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExplicitExecutableNameInMemoryTest('test'))
        pass
    pass

class ExplicitExecutableNameInMemoryTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='main.cc',
            entry=File(lines=['// CONFIX:EXENAME("explicit-name")',
                              'int main() { return 0; }']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False, use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        for b in package.rootbuilder().iter_builders():
            if isinstance(b, ExecutableBuilder) and b.exename() == 'explicit-name':
                break
            pass
        else:
            self.fail()
            pass
        pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(ExecutableNameInMemorySuite())
    pass

