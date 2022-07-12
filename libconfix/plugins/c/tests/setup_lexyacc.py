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

from libconfix.plugins.c.lex import LexBuilder
from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.yacc import YaccBuilder
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class LexYaccSetupTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LexYaccSetupTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        fs.rootdirectory().add(
            name='clexfile.l',
            entry=File())
        fs.rootdirectory().add(
            name='cxxlexfile.ll',
            entry=File())
        fs.rootdirectory().add(
            name='cyaccfile.y',
            entry=File())
        fs.rootdirectory().add(
            name='cxxyaccfile.yy',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        clex = cxxlex = cyacc = cxxyacc = lib = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, LexBuilder):
                if b.file().name() == 'clexfile.l':
                    clex = b
                    continue
                if b.file().name() == 'cxxlexfile.ll':
                    cxxlex = b
                    continue
                self.fail()
                pass
            if isinstance(b, YaccBuilder):
                if b.file().name() == 'cyaccfile.y':
                    cyacc = b
                    continue
                if b.file().name() == 'cxxyaccfile.yy':
                    cxxyacc = b
                    continue
                self.fail()
                pass
            if isinstance(b, LibraryBuilder):
                lib = b
                continue
            pass

        self.assertFalse(clex is None)
        self.assertFalse(cxxlex is None)
        self.assertFalse(cyacc is None)
        self.assertFalse(cxxyacc is None)
        self.assertFalse(lib is None)
        pass
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(LexYaccSetupTest))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

