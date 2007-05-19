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

import unittest, os, sys, shutil

from libconfix.core.automake import bootstrap, configure, make
from libconfix.core.automake.repo_automake import AutomakeCascadedPackageRepository
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class InterPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterPackageBuildWithLibtool('test'))
        self.addTest(InterPackageBuildWithoutLibtool('test'))
        self.addTest(InstalledIncludeDirTest('test'))
        pass
    pass

class InterPackageBuildBase(PersistentTestCase):
    def __init__(self, str):
        PersistentTestCase.__init__(self, str)
        pass

    def use_libtool(self): assert 0
    
    def setUp(self):
        PersistentTestCase.setUp(self)
        self.sourcedir_ = self.rootpath() + ['source']
        self.builddir_ = self.rootpath() + ['build']
        self.installdir_ = self.rootpath() + ['install']
        self.lo_sourcedir_ = self.sourcedir_ + ['lo']
        self.lo_builddir_ = self.builddir_ + ['lo']
        self.hi_sourcedir_ = self.sourcedir_ + ['hi']
        self.hi_builddir_ = self.builddir_ + ['hi']

        lo_root = Directory()
        lo_root.add(name=const.CONFIX2_PKG,
                    entry=File(lines=['PACKAGE_NAME("lo")',
                                      'PACKAGE_VERSION("1.2.3")']))
        lo_root.add(name=const.CONFIX2_DIR,
                    # we actually do nothing intelligent here but to
                    # test the marshalling of buildinfo (which is not
                    # strictly the target of this particular test, but
                    # I'm too lazy to make an extra test of it)
                    entry=File(lines=['CONFIGURE_AC(lines=["  "],',
                                      '             order=AC_PROGRAMS)',
                                      'ACINCLUDE_M4(lines=["  "])'
                                      ]))
        lo_h = lo_root.add(name='lo.h',
                           entry=File(lines=['#ifndef lo_lo_h',
                                             '#define lo_lo_h',
                                             'void lo();',
                                             '#endif',
                                             ]))
        lo_h.set_property(name='INSTALLPATH_CINCLUDE', value=['lo'])
        lo_root.add(name='lo.c',
                    entry=File(lines=['#include "lo.h"',
                                      'void lo() {}']))
        self.lo_fs_ = FileSystem(path=self.lo_sourcedir_, rootdirectory=lo_root)

        self.lo_package_ = LocalPackage(rootdirectory=self.lo_fs_.rootdirectory(),
                                        setups=[DefaultCSetup(short_libnames=False,
                                                              use_libtool=self.use_libtool())])
        
        
        hi_root = Directory()
        hi_root.add(name=const.CONFIX2_PKG,
                    entry=File(lines=['PACKAGE_NAME("hi")',
                                      'PACKAGE_VERSION("4.5.6")']))
        hi_root.add(name=const.CONFIX2_DIR,
                    entry=File())
        lib = hi_root.add(name='lib',
                          entry=Directory())
        lib.add(name=const.CONFIX2_DIR,
                entry=File())
        lib.add(name='hilib.h',
                entry=File(lines=['#ifndef hi_hilib_h',
                                  '#define hi_hilib_h',
                                  'void hilib();',
                                  '#endif']))
        lib.add(name='hilib.c',
                entry=File(lines=['#include "hilib.h"',
                                  '#include <stdio.h>',
                                  'void hilib() {',
                                  r'    printf("hilib();\n");',
                                  '}']))
        bin = hi_root.add(name='bin',
                          entry=Directory())
        bin.add(name=const.CONFIX2_DIR,
                entry=File())
        bin.add(name='main.c',
                entry=File(lines=['#include <lo/lo.h>',
                                  '#include <hilib.h>',
                                  '// URGENCY_ERROR: detect errors as early as possible ',
                                  '// (keeping test-and-fix cycles low)',
                                  '// CONFIX:REQUIRE_H("lo/lo.h", URGENCY_ERROR)',
                                  '// CONFIX:REQUIRE_H("hilib.h", URGENCY_ERROR)',
                                  '',
                                  'int main() {',
                                  '  lo();',
                                  '  hilib();',
                                  '  return 0;',
                                  '}']))

        self.hi_fs_ = FileSystem(path=self.hi_sourcedir_, rootdirectory=hi_root)
        self.hi_package_ = LocalPackage(rootdirectory=self.hi_fs_.rootdirectory(),
                                        setups=[DefaultDirectorySetup(),
                                                DefaultCSetup(short_libnames=False,
                                                       use_libtool=self.use_libtool())])
        
        pass

    def test(self):
        try:
            # confixize, bootstrap, and install package 'lo'

            self.lo_package_.boil(external_nodes=[])
            self.lo_package_.output()
            self.lo_fs_.sync()

            bootstrap.bootstrap(
                packageroot=self.lo_sourcedir_,
                use_libtool=self.use_libtool(),
                use_kde_hack=False,
                path=None,
                argv0=sys.argv[0])
            os.makedirs(os.sep.join(self.lo_builddir_))
            configure.configure(
                packageroot=self.lo_sourcedir_,
                builddir=self.lo_builddir_,
                prefix=self.installdir_,
                readonly_prefixes=[])
            make.make(
                builddir=self.lo_builddir_,
                args=['install'])

            # read repo from prefix

            repo = AutomakeCascadedPackageRepository(
                prefix=self.installdir_,
                readonly_prefixes=[])

            # confixize, bootstrap, and install package 'hi'

            self.hi_package_.boil(external_nodes=repo.nodes())
            self.hi_package_.output()
            self.hi_fs_.sync()

            bootstrap.bootstrap(
                packageroot=self.hi_sourcedir_,
                use_libtool=self.use_libtool(),
                use_kde_hack=False,
                path=None,
                argv0=sys.argv[0])
            os.makedirs(os.sep.join(self.hi_builddir_))
            configure.configure(
                packageroot=self.hi_sourcedir_,
                builddir=self.hi_builddir_,
                prefix=self.installdir_,
                readonly_prefixes=[])
            make.make(
                builddir=self.hi_builddir_,
                args=['install'])
            
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise

        pass
    pass

class InterPackageBuildWithLibtool(InterPackageBuildBase):
    def __init__(self, str):
        InterPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return True
    pass
    
class InterPackageBuildWithoutLibtool(InterPackageBuildBase):
    def __init__(self, str):
        InterPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return False
    pass

class InstalledIncludeDirTest(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        lo_build = build.add(
            name='lo',
            entry=Directory())
        hi_build = build.add(
            name='hi',
            entry=Directory())
        prefix = fs.rootdirectory().add(
            name='prefix',
            entry=Directory())
            
        # package lo contains 2 header files. one is installed flat
        # into #(includedir), the other onto a subdirectory thereof.
        lo_source = source.add(
            name='lo',
            entry=Directory())
        lo_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('InstalledIncludeDirTest-LO')",
                              "PACKAGE_VERSION('1.2.3')"]))
        lo_source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo_source.add(
            name='flat.h',
            entry=File())
        lo_source.add(
            name='deep.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['path', 'to', 'deep'])"]))

        # hi contains one file that includes both.
        hi_source = source.add(
            name='hi',
            entry=Directory())

        hi_source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('InstalledIncludeDirTest-HI')",
                              "PACKAGE_VERSION('1.2.3')"]))
        hi_source.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi_source.add(
            name='hi.c',
            entry=File(lines=["#include <flat.h>",
                              "#include <path/to/deep/deep.h>"]))


        # bootstrap ... install lo
        package = LocalPackage(rootdirectory=lo_source,
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=lo_source.abspath(),
            path=None,
            use_libtool=False,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=lo_source.abspath(),
            builddir=lo_build.abspath(),
            prefix=prefix.abspath(),
            readonly_prefixes=[])
        make.make(
            builddir=lo_build.abspath(),
            args=['install'])

        # read repo that we need for hi
            
        repo = AutomakeCascadedPackageRepository(
            prefix=prefix.abspath(),
            readonly_prefixes=[])

        # bootstrap ... make hi

        
        package = LocalPackage(rootdirectory=hi_source,
                               setups=[DefaultCSetup(short_libnames=False,
                                              use_libtool=False)])
        package.boil(external_nodes=repo.nodes())
        package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=hi_source.abspath(),
            path=None,
            use_libtool=False,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=hi_source.abspath(),
            builddir=hi_build.abspath(),
            prefix=prefix.abspath(),
            readonly_prefixes=[])
        make.make(
            builddir=hi_build.abspath(),
            args=[])
        pass
    pass
        
if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageBuildSuite())
    pass
