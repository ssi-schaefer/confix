# Copyright (C) 2007-2013 Joerg Faschingbauer

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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.overlay_filesys import OverlayFileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.automake import bootstrap
from libconfix.plugins.automake import configure
from libconfix.plugins.automake import make

import unittest
import sys
import os

class OverlayBasicTest(PersistentTestCase):
    def test(self):
        source = self.rootpath() + ['source']
        build = self.rootpath() + ['build']
        install = self.rootpath() + ['install']
        overlay = self.rootpath() + ['overlay']

        # compose the source tree,

        # source
        # |-- exe
        # |   `-- main.c
        # `-- library
        #     |-- library.c
        #     `-- library.h

        source_fs = FileSystem(path=source)
        source_library = source_fs.rootdirectory().add(
            name='library',
            entry=Directory())
        source_library.add(
            name='library.h',
            entry=File(lines=['#ifndef LIBRARY_H',
                              '#define LIBRARY_H',
                              'extern void f(void);',
                              '#endif']))
        source_library.add(
            name='library.c',
            entry=File(lines=['#include "library.h"',
                              'void f(void) {}']))
        source_exe = source_fs.rootdirectory().add(
            name='exe',
            entry=Directory())
        source_exe.add(
            name='main.c',
            entry=File(lines=['// CONFIX:EXENAME("the_exe")',
                              '#include <library.h>',
                              'int main(void) {',
                              '    f();',
                              '    return 0;',
                              '}']))

        # compose the build instructions, separate from the source
        # tree,

        # overlay
        # |-- Confix2.dir
        # |-- Confix2.pkg
        # |-- exe
        # |   `-- Confix2.dir
        # `-- library
        #     `-- Confix2.dir

        overlay_fs = FileSystem(path=overlay)
        overlay_fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("'+self.__class__.__name__+'")',
                              'PACKAGE_VERSION("1.2.3")']))
        overlay_fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        overlay_library = overlay_fs.rootdirectory().add(
            name='library',
            entry=Directory())
        overlay_library.add(
            name=const.CONFIX2_DIR,
            entry=File())
        overlay_exe = overlay_fs.rootdirectory().add(
            name='exe',
            entry=Directory())
        overlay_exe.add(
            name=const.CONFIX2_DIR,
            entry=File())

        # union of both, and boil-build-install
        
        overlay_fs = OverlayFileSystem(original=source_fs, overlay=overlay_fs)
        
        package = LocalPackage(rootdirectory=overlay_fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        # should have checked such thing elsewhwere, but it won't hurt
        # repeating.
        self.failUnless(source_fs.rootdirectory().find([const.CONFIX2_PKG]) is None)
        self.failUnless(source_fs.rootdirectory().find([const.CONFIX2_DIR]) is None)
        self.failUnless(source_fs.rootdirectory().find(['exe', const.CONFIX2_DIR]) is None)
        self.failUnless(source_fs.rootdirectory().find(['library', const.CONFIX2_DIR]) is None)

        overlay_fs.sync()

        os.makedirs(os.sep.join(build))
        bootstrap.bootstrap(packageroot=overlay_fs.rootdirectory().abspath(),
                            use_kde_hack=False,
                            argv0=sys.argv[0])
        configure.configure(packageroot=overlay_fs.rootdirectory().abspath(),
                            builddir=build,
                            prefix=install)
        make.make(builddir=build,
                  args=['install'])

        self.failUnless(os.path.exists(os.sep.join(install+['bin', 'the_exe'])))

        make.make(builddir=build,
                  args=['dist'])

        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(OverlayBasicTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass

