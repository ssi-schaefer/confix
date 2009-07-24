# Copyright (C) 2007-2009 Joerg Faschingbauer

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

import libconfix.plugins.c.relocated_headers.tests.inter_package as inter_package

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.plugins.automake import bootstrap, configure, make, helper
from libconfix.plugins.automake.repo_automake import AutomakePackageRepository
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.testutils.persistent import PersistentTestCase

import unittest
import sys

class ImplicitInterPackageBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(InterPackageBuildTest('test'))
        pass
    pass

class InterPackageBuildTest(PersistentTestCase):
    def use_libtool(self): return False
    def short_libnames(self): return False
    def use_kde_hack(self): return False
    
    def test(self):
        common_source, lo_source, hi_source = inter_package.make_source(
            classname=helper.automake_name(self.__class__.__name__))

        fs = FileSystem(path=self.rootpath())
        source = fs.rootdirectory().add(
            name='source',
            entry=Directory())
        source.add(
            name='common',
            entry=common_source)
        source.add(
            name='lo',
            entry=lo_source)
        source.add(
            name='hi',
            entry=hi_source)

        build = fs.rootdirectory().add(
            name='build',
            entry=Directory())
        common_build = build.add(
            name='common',
            entry=Directory())
        lo_build = build.add(
            name='lo',
            entry=Directory())
        hi_build = build.add(
            name='hi',
            entry=Directory())

        install = fs.rootdirectory().add(
            name='install',
            entry=Directory())

        # massage common
        
        common_package = LocalPackage(
            rootdirectory=common_source,
            setups=[ConfixSetup(short_libnames=self.short_libnames(), use_libtool=self.use_libtool())])
        common_package.boil(external_nodes=[])
        common_package.output()
        fs.sync()                                      
        
        bootstrap.bootstrap(
            packageroot=common_source.abspath(),
            use_kde_hack=self.use_kde_hack(),
            argv0=sys.argv[0])
        configure.configure(
            packageroot=common_source.abspath(),
            builddir=common_build.abspath(),
            prefix=install.abspath())
        make.make(
            builddir=common_build.abspath(),
            args=['install'])

        # massage lo

        lo_package = LocalPackage(
            rootdirectory=lo_source,
            setups=[ConfixSetup(short_libnames=self.short_libnames(), use_libtool=self.use_libtool())])
        lo_package.boil(external_nodes=AutomakePackageRepository(prefix=install.abspath()).nodes())
        lo_package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=lo_source.abspath(),
            use_kde_hack=self.use_kde_hack(),
            argv0=sys.argv[0])
        configure.configure(
            packageroot=lo_source.abspath(),
            builddir=lo_build.abspath(),
            prefix=install.abspath())
        make.make(
            builddir=lo_build.abspath(),
            args=['install'])
        repo = AutomakePackageRepository(prefix=install.abspath())

        # massage hi

        hi_package = LocalPackage(
            rootdirectory=hi_source,
            setups=[ConfixSetup(short_libnames=self.short_libnames(), use_libtool=self.use_libtool())])
        hi_package.boil(external_nodes=AutomakePackageRepository(prefix=install.abspath()).nodes())
        hi_package.output()
        fs.sync()

        bootstrap.bootstrap(
            packageroot=hi_source.abspath(),
            use_kde_hack=self.use_kde_hack(),
            argv0=sys.argv[0])
        configure.configure(
            packageroot=hi_source.abspath(),
            builddir=hi_build.abspath(),
            prefix=install.abspath())
        make.make(
            builddir=hi_build.abspath(),
            args=[])

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(InterPackageBuildSuite())
    pass


