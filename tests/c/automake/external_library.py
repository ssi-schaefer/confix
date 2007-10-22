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
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.plugins.c.library import LibraryBuilder
from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class ExternalLibraryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExternalLibraryTest('test'))
        pass
    pass

class ExternalLibraryTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['', 'path', 'to', 'it'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExternalLibraryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lolo = fs.rootdirectory().add(
            name='lolo',
            entry=Directory())
        lolo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('lolo')",
                              "EXTERNAL_LIBRARY(",
                              "    incpath=['-I/the/include/path/of/lolo'],",
                              "    libpath=['-L/the/first/library/path/of/lolo', '-L/the/second/library/path/of/lolo'],",
                              "    cflags=['some_cflag'],",
                              "    cmdlinemacros={'key': 'value'},",
                              "    libs=['-llolo'])"]))

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('lolo', URGENCY_ERROR)",
                              "PROVIDE_SYMBOL('lo')",
                              "EXTERNAL_LIBRARY(",
                              "    incpath=['-I/the/include/path/of/lo'],",
                              "    libpath=['-L/the/first/library/path/of/lo', '-L/the/second/library/path/of/lo'],",
                              "    libs=['-llo'])"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi.add(
            name='hi_c.c',
            entry=File(lines=["// CONFIX:REQUIRE_SYMBOL('lo', URGENCY_ERROR)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[DefaultDirectorySetup(),
                                       DefaultCSetup(use_libtool=True, short_libnames=False)])
        package.boil(external_nodes=[])
        package.output()
        
        hidir_builder = package.rootbuilder().find_entry_builder(['hi'])
        hi_c_builder = package.rootbuilder().find_entry_builder(['hi', 'hi_c.c'])
        self.failIf(hidir_builder is None)
        self.failIf(hi_c_builder is None)

        for b in hidir_builder.builders():
            if isinstance(b, LibraryBuilder):
                hi_lib_builder = b
                break
            pass
        else:
            self.fail()
            pass

        self.failUnless(hi_c_builder.external_include_path()[0] == ['-I/the/include/path/of/lo'])
        self.failUnless(hi_c_builder.external_include_path()[1] == ['-I/the/include/path/of/lolo'])
        self.failUnless('some_cflag' in hi_c_builder.cflags())
        self.failUnless(hi_c_builder.cmdlinemacros().get('key') is not None)

        self.failUnless(hi_lib_builder.external_libpath()[0] == \
                        ['-L/the/first/library/path/of/lo', '-L/the/second/library/path/of/lo'])
        self.failUnless(hi_lib_builder.external_libpath()[1] == \
                        ['-L/the/first/library/path/of/lolo', '-L/the/second/library/path/of/lolo'])
        self.failUnlessEqual(hi_lib_builder.external_libraries()[0], ['-llo'])
        self.failUnlessEqual(hi_lib_builder.external_libraries()[1], ['-llolo'])

        self.failUnless('-llolo' in hidir_builder.makefile_am().compound_libadd('libExternalLibraryTest_hi_la'))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExternalLibraryInMemorySuite())
    pass

