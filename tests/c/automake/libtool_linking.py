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

from libconfix.plugins.c.setup import DefaultCSetup

from libconfix.testutils import find

class LibtoolLinkingSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(LibtoolLinklineSeeThroughHeaders('test'))
        pass
    pass

class LibtoolLinklineSeeThroughHeaders(unittest.TestCase):
    def test(self):
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
                               setups=[DefaultCSetup(use_libtool=True, short_libnames=False),
                                       DirectorySetup()])
        package.boil(external_nodes=[])
        package.output()

        userlib_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(),
                                                 path=['userlib'])

        # if we foolishly didn't see through the seethrough1 and
        # seethrough2 nodes until we see a real library, the we'd not
        # have anything to link in.
        self.failIf(userlib_builder.makefile_am().compound_libadd(
            'libLibtoolLinklineSeeThroughHeaders_userlib_la') is None)

        # when we see through both seethrough1 and seethrough2, then
        # we see the 'lo' library. we see it twice because we have two
        # paths, and we're expected to sort this out.
        self.failUnlessEqual(
            userlib_builder.makefile_am().compound_libadd('libLibtoolLinklineSeeThroughHeaders_userlib_la'),
            ['-L$(top_builddir)/lib', '-lLibtoolLinklineSeeThroughHeaders_lib'])

        userexe_builder = find.find_entrybuilder(rootbuilder=package.rootbuilder(),
                                                 path=['userexe'])

        # for the executables holds the same as for libraries, so this
        # is basically a copy of above, with a few things exchanged.
        self.failIf(userexe_builder.makefile_am().compound_ldadd(
            'LibtoolLinklineSeeThroughHeaders_userexe_main') is None)

        self.failUnlessEqual(
            userexe_builder.makefile_am().compound_ldadd('LibtoolLinklineSeeThroughHeaders_userexe_main'),
            ['-L$(top_builddir)/lib', '-lLibtoolLinklineSeeThroughHeaders_lib'])

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(LibtoolLinkingSuite())
    pass
