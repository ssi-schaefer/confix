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
import os
import sys
import shutil

from libconfix.core.automake import bootstrap, configure, make
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.default_setup import DefaultDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

from libconfix.testutils import packages
from libconfix.testutils.persistent import PersistentTestCase

from libconfix.plugins.c.setups.default_setup import DefaultCSetup

class IntraPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IntraPackageBuildWithLibtool('test'))
        self.addTest(IntraPackageBuildWithoutLibtool('test'))
        self.addTest(LocalIncludeDirTest('test'))
        pass
    pass

class IntraPackageBuildBase(PersistentTestCase):
    def __init__(self, methodName):
        PersistentTestCase.__init__(self, methodName)
        pass

    def use_libtool(self): assert 0

    def setUp(self):
        PersistentTestCase.setUp(self)
        
        self.sourcerootpath_ = self.rootpath() + ['source']
        self.buildrootpath_ = self.rootpath() + ['build']

        self.fs_ = FileSystem(path=self.sourcerootpath_,
                              rootdirectory=packages.lo_hi1_hi2_highest_exe(name='intrapackagebuildtest',
                                                                            version='1.2.3'))
        
        self.package_ = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                                     setups=[DefaultDirectorySetup(),
                                             DefaultCSetup(short_libnames=False,
                                                    use_libtool=self.use_libtool())])
        self.package_.boil(external_nodes=[])
        self.package_.output()
        self.fs_.sync()
        pass

    def test(self):
        try:
            bootstrap.bootstrap(
                packageroot=self.sourcerootpath_,
                path=None,
                use_libtool=self.use_libtool(),
                use_kde_hack=False,
                argv0=sys.argv[0])
            os.makedirs(os.sep.join(self.buildrootpath_))
            configure.configure(
                packageroot=self.sourcerootpath_,
                builddir=self.buildrootpath_,
                prefix='/dev/null'.split(os.sep),
                readonly_prefixes=[])
            make.make(builddir=self.buildrootpath_, args=[])
        except Error, e:
            sys.stderr.write(`e`+'\n')
            raise
        
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['lo', 'lo.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['hi1', 'hi1.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['hi2', 'hi2.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['highest', 'highest.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['exe', 'main.o'])))
        self.failUnless(os.path.isfile(os.sep.join(self.buildrootpath_+['exe', 'intrapackagebuildtest_exe_main'])))
        pass

    pass

class IntraPackageBuildWithLibtool(IntraPackageBuildBase):
    def __init__(self, str):
        IntraPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return True
    pass

class IntraPackageBuildWithoutLibtool(IntraPackageBuildBase):
    def __init__(self, str):
        IntraPackageBuildBase.__init__(self, str)
        pass
    def use_libtool(self): return False
    pass

class LocalIncludeDirTest(PersistentTestCase):
    def test(self):
        fs = FileSystem(path=self.rootpath())
        
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('LocalIncludeDirTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File())

        flat = source.add(
            name='flat',
            entry=Directory())
        flat.add(
            name=const.CONFIX2_DIR,
            entry=File())
        flat.add(
            name='flat.h',
            entry=File())

        deep = source.add(
            name='deep',
            entry=Directory())
        deep.add(
            name=const.CONFIX2_DIR,
            entry=File())
        deep.add(
            name='deep.h',
            entry=File(lines=["// CONFIX:INSTALLPATH(['path', 'to', 'deep'])"]))

        user = source.add(
            name='user',
            entry=Directory())
        user.add(
            name=const.CONFIX2_DIR,
            entry=File())
        user.add(
            name='user.c',
            entry=File(lines=["#include <flat.h>",
                              "#include <path/to/deep/deep.h>"]))

        package = LocalPackage(rootdirectory=source,
                               setups=[DefaultDirectorySetup(),
                                       DefaultCSetup(use_libtool=False, short_libnames=False)])
        package.boil(external_nodes=[])
        package.output()

        fs.sync()

        bootstrap.bootstrap(
            packageroot=source.abspath(),
            path=None,
            use_libtool=False,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=source.abspath(),
            builddir=build.abspath(),
            prefix='/dev/null'.split(os.sep),
            readonly_prefixes=[])
        make.make(
            builddir=build.abspath(),
            args=[])
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IntraPackageBuildSuite())
    pass

