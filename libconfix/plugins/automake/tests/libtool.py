# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2013 Joerg Faschingbauer

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

from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.c.setups.default_setup import DefaultCSetup
from libconfix.plugins.c.library import LibraryBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.setups.explicit_setup import ExplicitSetup

import unittest

class LibtoolTest(unittest.TestCase):
    def test__library(self):
        rootdir = Directory()
        rootdir.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibtoolInMemoryTest.testLibrary')",
                              "PACKAGE_VERSION('1.2.3')"]))
        rootdir.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["LIBRARY(members=[C(filename='file.c')])"]))
        rootdir.add(
            name='file.c',
            entry=File())

        package = LocalPackage(rootdirectory=rootdir,
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])
        package.output()

        library_builder = None
        for b in package.rootbuilder().iter_builders():
            if isinstance(b, LibraryBuilder):
                self.assertTrue(library_builder is None)
                library_builder = b
                pass
            pass
        self.assertFalse(library_builder is None)

        automake_output_builder = find_automake_output_builder(package.rootbuilder())
        self.assertTrue('lib'+library_builder.basename()+'.la' in automake_output_builder.makefile_am().ltlibraries())
        pass
    
    def test__see_through_headers(self):
        fs = FileSystem(path=['don\'t', 'care'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LibtoolLinklineSeeThroughHeaders')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lib = fs.rootdirectory().add(
            name='lib',
            entry=Directory())
        lib.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib.add(
            name='lib.h',
            entry=File())
        lib.add(
            name='lib.c',
            entry=File())

        seethrough1 = fs.rootdirectory().add(
            name='seethrough1',
            entry=Directory())
        seethrough1.add(
            name=const.CONFIX2_DIR,
            entry=File())
        seethrough1.add(
            name='seethrough1.h',
            entry=File(lines=["#include <lib.h>"]))

        seethrough2 = fs.rootdirectory().add(
            name='seethrough2',
            entry=Directory())
        seethrough2.add(
            name=const.CONFIX2_DIR,
            entry=File())
        seethrough2.add(
            name='seethrough2.h',
            entry=File(lines=["#include <lib.h>"]))

        userlib = fs.rootdirectory().add(
            name='userlib',
            entry=Directory())
        userlib.add(
            name=const.CONFIX2_DIR,
            entry=File())
        userlib.add(
            name='userlib.c',
            entry=File(lines=['#include <seethrough1.h>',
                              '#include <seethrough2.h>']))

        userexe = fs.rootdirectory().add(
            name='userexe',
            entry=Directory())
        userexe.add(
            name=const.CONFIX2_DIR,
            entry=File())
        userexe.add(
            name='main.c',
            entry=File(lines=['#include <seethrough1.h>',
                              '#include <seethrough2.h>',
                              'int main() {}']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=True)])
        package.boil(external_nodes=[])
        package.output()

        userlib_builder = package.rootbuilder().find_entry_builder(['userlib'])
        self.assertFalse(userlib_builder is None)
        userlib_automake_builder = find_automake_output_builder(userlib_builder)

        # if we foolishly didn't see through the seethrough1 and
        # seethrough2 nodes until we see a real library, the we'd not
        # have anything to link in.
        self.assertFalse(userlib_automake_builder.makefile_am().compound_libadd(
            'libLibtoolLinklineSeeThroughHeaders_userlib_la') is None)

        # when we see through both seethrough1 and seethrough2, then
        # we see the 'lo' library. we see it twice because we have two
        # paths, and we're expected to sort this out.
        self.assertEqual(
            userlib_automake_builder.makefile_am().compound_libadd('libLibtoolLinklineSeeThroughHeaders_userlib_la'),
            ['-L$(top_builddir)/lib', '-lLibtoolLinklineSeeThroughHeaders_lib'])

        userexe_builder = package.rootbuilder().find_entry_builder(['userexe'])
        self.assertFalse(userexe_builder is None)
        userexe_automake_builder = find_automake_output_builder(userexe_builder)

        # for the executables holds the same as for libraries, so this
        # is basically a copy of above, with a few things exchanged.
        self.assertFalse(userexe_automake_builder.makefile_am().compound_ldadd(
            'LibtoolLinklineSeeThroughHeaders_userexe_main') is None)

        self.assertEqual(
            userexe_automake_builder.makefile_am().compound_ldadd('LibtoolLinklineSeeThroughHeaders_userexe_main'),
            ['-L$(top_builddir)/lib', '-lLibtoolLinklineSeeThroughHeaders_lib'])

        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibtoolTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
