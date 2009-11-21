# Copyright (C) 2002-2006 Salomon Automation
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

import sys
import unittest

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.plugins.automake import bootstrap, configure, make

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils.persistent import PersistentTestCase

class InterixLinkSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterixLink('test'))
        pass
    pass

class InterixLink(PersistentTestCase):

    # one day, on interix, we saw libtool behave strange with the
    # following constellation

    # libhi.la -> liblo.la -> liblolo.la

    # when using libtool to link libhi, we only pass -llo on the
    # commandline, and not -llolo. libtool seems to fail to toposort
    # and calculate -llo -llolo by itself.

    # (we did not find out anything about this so far: this test works
    # well on interix.)
    
    def test(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('InterixLink')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())

        lolo = source.add(
            name='lolo',
            entry=Directory())
        lolo.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lolo.add(
            name='lolo.h',
            entry=File(lines=["void lolo(void);"]))
        lolo.add(
            name='lolo.c',
            entry=File(lines=["void lolo(void) {}"]))

        lo = source.add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo.add(
            name='lo.h',
            entry=File(lines=["void lo(void);"]))
        lo.add(
            name='lo.c',
            entry=File(lines=["#include <lolo.h>",
                              "void lo(void) {lolo();}"]))

        hi = source.add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi.add(
            name='hi.c',
            entry=File(lines=["#include <lo.h>",
                              "void hi(void) {lo();}"]))

        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        package = LocalPackage(rootdirectory=source,
                               setups=[ConfixSetup(use_libtool=True)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix=None,
            readonly_prefixes=None)
        make.make(
            builddir=build.abspath(),
            args=[])

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterixLinkSuite())
    pass

