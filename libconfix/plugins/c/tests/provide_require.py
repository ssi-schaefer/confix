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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.machinery.require import Require
from libconfix.core.utils import const
from libconfix.setups.explicit_setup import ExplicitSetup

from libconfix.plugins.c.dependency import \
     Require_CInclude, \
     Provide_CInclude
from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class Provide_CInclude_and_Require_CInclude(unittest.TestCase):
    def testBasic(self):
        r = Require_CInclude(filename='file.h', found_in=[], urgency=Require.URGENCY_DEFAULT)
        p = Provide_CInclude(filename='file.h')
        self.failUnless(p.resolve(r))

        p = Provide_CInclude(filename='file1.h')
        self.failIf(p.resolve(r))

        p = Provide_CInclude(filename='file*', match=Provide_CInclude.GLOB_MATCH)
        self.failUnless(p.resolve(r))

        p = Provide_CInclude(filename='file*', match=Provide_CInclude.AUTO_MATCH)
        self.failUnless(p.resolve(r))
        p = Provide_CInclude(filename='file[a]', match=Provide_CInclude.AUTO_MATCH)
        self.failIf(p.resolve(r))
        p = Provide_CInclude(filename='file.[hc]', match=Provide_CInclude.AUTO_MATCH)
        self.failUnless(p.resolve(r))
        p = Provide_CInclude(filename='file.?', match=Provide_CInclude.AUTO_MATCH)
        self.failUnless(p.resolve(r))
        
        pass

    def testIface(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(['PACKAGE_NAME("Provide_CInclude_and_Require_CInclude.testIface")',
                        'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_H(filename='file*')",
                              "PROVIDE_H(filename='file')",
                              "PROVIDE_H(filename='file?')",
                              "PROVIDE_H(filename='fileblah', match=AUTO_MATCH)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=False)])
        package.boil(external_nodes=[])

        found = 0
        for p in package.rootbuilder().provides():
            self.failUnless(isinstance(p, Provide_CInclude))
            if p.string() == 'file*':
                self.failUnless(p.match() == Provide_CInclude.GLOB_MATCH)
                found += 1
                continue
            if p.string() == 'file':
                self.failUnless(p.match() == Provide_CInclude.EXACT_MATCH)
                found += 1
                continue
            if p.string() == 'file?':
                self.failUnless(p.match() == Provide_CInclude.GLOB_MATCH)
                found += 1
                continue
            if p.string() == 'fileblah':
                self.failUnless(p.match() == Provide_CInclude.EXACT_MATCH)
                found += 1
                continue
            pass
        self.failUnlessEqual(found, 4)
        pass

    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Provide_CInclude_and_Require_CInclude))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
