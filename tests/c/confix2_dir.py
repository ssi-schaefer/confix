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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.setup import DirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils import find

from libconfix.plugins.c.setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder

class Confix2_dir_Suite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ProvideRequireInclude('test'))
        pass
    pass

class ProvideRequireInclude(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['', 'path', 'to', 'it'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ProvideRequireInclude')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_H('lo.h')"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_H('lo.h', URGENCY_ERROR)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DirectorySetup(),
                                       DefaultCSetup(use_libtool=False,
                                                     short_libnames=False)])
        package.boil(external_nodes=[])

        lo_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(),
                                            path=['lo'])
        hi_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(),
                                            path=['hi'])

        self.failUnless(lo_builder in package.digraph().successors(hi_builder))
        pass
    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(Confix2_dir_Suite())
    pass

