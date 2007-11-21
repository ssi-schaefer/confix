# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

import os
import sys
import unittest

from libconfix.core.automake import bootstrap, configure, make
from libconfix.core.automake.repo_automake import AutomakeCascadedPackageRepository
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.plugins.c.setups.default_setup import DefaultCSetup

from libconfix.testutils.persistent import PersistentTestCase

class ReadonlyPrefixesBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ReadonlyPrefixesBuildWithoutLibtool('test'))
        self.addTest(ReadonlyPrefixesBuildWithLibtool('test'))
        pass
    pass

class ReadonlyPrefixesBuildBase(PersistentTestCase):
    def __init__(self, str):
        PersistentTestCase.__init__(self, str)
        pass

    def use_libtool(self): assert 0
    
    def test(self):
        sourcedir = self.rootpath() + ['source']
        builddir = self.rootpath() + ['build']
        installdir = self.rootpath() + ['install']

        lo_sourcedir = sourcedir + ['lo']
        lo_builddir = builddir + ['lo']
        lo_installdir = installdir + ['lo']

        hi_sourcedir = sourcedir + ['hi']
        hi_builddir = builddir + ['hi']
        hi_installdir = installdir + ['hi']

        # create, sync, build, install package lo
        # ---------------------------------------
        lo_fs = FileSystem(path=lo_sourcedir)

        lo_fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("lo")',
                              'PACKAGE_VERSION("1.2.3")']))
        lo_fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=[]))
        lo_fs.rootdirectory().add(
            name='lo.h',
            entry=File(lines=['#ifndef lo_lo_h',
                              '#define lo_lo_h',
                              'void lo();',
                              '#endif',
                              ]))
        lo_fs.rootdirectory().add(
            name='lo.c',
            entry=File(lines=['#include "lo.h"',
                              'void lo() {}']))

        lo_package = LocalPackage(rootdirectory=lo_fs.rootdirectory(),
                                  setups=[DefaultCSetup(short_libnames=False,
                                                 use_libtool=self.use_libtool())])
        lo_package.boil(external_nodes=[])
        lo_package.output()
        lo_fs.sync()

        bootstrap.bootstrap(
            packageroot=lo_sourcedir,
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        os.makedirs(os.sep.join(lo_builddir))
        configure.configure(
            packageroot=lo_sourcedir,
            builddir=lo_builddir,
            prefix=lo_installdir,
            readonly_prefixes=[])
        make.make(
            builddir=lo_builddir,
            args=['install'])


        # get external view (repo-packages from prefix and readonly-prefixes)
        # -------------------------------------------------------------------

        repo = AutomakeCascadedPackageRepository(
            prefix=hi_installdir, # we don't actually read aything
                                  # from there because we have nothing
                                  # installed there (yet)
            readonly_prefixes=[lo_installdir])

        # create, sync, build package lo
        # ------------------------------

        hi_fs = FileSystem(path=hi_sourcedir)
        
        hi_fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("hi")',
                              'PACKAGE_VERSION("4.5.6")']))
        hi_fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib = hi_fs.rootdirectory().add(
            name='lib',
            entry=Directory())
        lib.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lib.add(
            name='hilib.h',
            entry=File(lines=['#ifndef hi_hilib_h',
                              '#define hi_hilib_h',
                              'void hilib();',
                              '#endif']))
        lib.add(
            name='hilib.c',
            entry=File(lines=['#include "hilib.h"',
                              '#include <stdio.h>',
                              'void hilib() {',
                              r'    printf("hilib();\n");',
                              '}']))
        bin = hi_fs.rootdirectory().add(
            name='bin',
            entry=Directory())
        bin.add(
            name=const.CONFIX2_DIR,
            entry=File())
        bin.add(
            name='main.c',
            entry=File(lines=['#include <lo.h>',
                              '#include <hilib.h>',
                              '// URGENCY_ERROR: detect errors as early as possible ',
                              '// (keeping test-and-fix cycles low)',
                              '// CONFIX:REQUIRE_H("lo.h", URGENCY_ERROR)',
                              '// CONFIX:REQUIRE_H("hilib.h", URGENCY_ERROR)',
                              '',
                              'int main() {',
                              '  lo();',
                              '  hilib();',
                              '  return 0;',
                              '}']))

        hi_package = LocalPackage(rootdirectory=hi_fs.rootdirectory(),
                                  setups=[DefaultDirectorySetup(),
                                          DefaultCSetup(short_libnames=False,
                                                 use_libtool=self.use_libtool())])
        hi_package.boil(external_nodes=repo.nodes())
        hi_package.output()
        hi_fs.sync()

        bootstrap.bootstrap(
            packageroot=hi_sourcedir,
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        os.makedirs(os.sep.join(hi_builddir))
        configure.configure(
            packageroot=hi_sourcedir,
            builddir=hi_builddir,
            prefix=hi_installdir,
            readonly_prefixes=[lo_installdir])
        make.make(
            builddir=hi_builddir,
            args=['install'])

        
        pass

    pass

class ReadonlyPrefixesBuildWithLibtool(ReadonlyPrefixesBuildBase):
    def __init__(self, str):
        ReadonlyPrefixesBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return True
    pass
    
class ReadonlyPrefixesBuildWithoutLibtool(ReadonlyPrefixesBuildBase):
    def __init__(self, str):
        ReadonlyPrefixesBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return False
    pass
        


if __name__ == '__main__':
    unittest.TextTestRunner().run(ReadonlyPrefixesBuildSuite())
    pass

