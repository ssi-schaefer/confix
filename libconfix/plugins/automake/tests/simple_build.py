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

from libconfix.plugins.automake import bootstrap, configure, make
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.core.utils.error import Error
from libconfix.testutils.persistent import PersistentTestCase
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import os
import shutil
import sys
import unittest

class SimpleBuildBase(PersistentTestCase):
    def __init__(self, methodName):
        PersistentTestCase.__init__(self, methodName)
        pass
    def setUp(self):
        PersistentTestCase.setUp(self)
        try:
            self.sourcerootpath_ = self.rootpath() + ['source']
            self.fs_ = FileSystem(path=self.sourcerootpath_)

            self.buildrootpath_ = self.rootpath() + ['build']

            self.fs_.rootdirectory().add(name=const.CONFIX2_PKG,
                                         entry=File(lines=['PACKAGE_NAME("simplebuildtest")',
                                                           'PACKAGE_VERSION("6.6.6")']))
            self.fs_.rootdirectory().add(name=const.CONFIX2_DIR,
                                         entry=File())
            self.fs_.rootdirectory().add(name='file.h',
                                         entry=File(lines=['#ifndef FILE_H',
                                                           '#define FILE_H',
                                                           'extern int i;',
                                                           '#endif',
                                                           ]))
            self.fs_.rootdirectory().add(name='file.c',
                                         entry=File(lines=['#include "file.h"',
                                                           'int i;',
                                                           ]))
            
            self.package_ = LocalPackage(rootdirectory=self.fs_.rootdirectory(),
                                         setups=[ConfixSetup(use_libtool=self.use_libtool())])
            self.package_.boil(external_nodes=[])
            self.package_.output()
            self.fs_.sync()
        except Error as e:
            sys.stderr.write(repr(e)+'\n')
            raise
        pass

    def test(self):
        try:
            bootstrap.bootstrap(
                packageroot=self.sourcerootpath_,
                path=None,
                use_kde_hack=False,
                argv0=sys.argv[0])
            os.makedirs(os.sep.join(self.buildrootpath_))
            configure.configure(
                packageroot=self.sourcerootpath_,
                builddir=self.buildrootpath_,
                prefix='/dev/null'.split(os.sep),
                readonly_prefixes=[])
            make.make(
                builddir=self.buildrootpath_,
                args=[])
        except Error as e:
            sys.stderr.write(repr(e)+'\n')
            raise

        self.assertTrue(os.path.isfile(os.sep.join(self.buildrootpath_+['file.o'])))
        pass

    pass

class SimpleBuildWithLibtool(SimpleBuildBase):
    def __init__(self, str):
        SimpleBuildBase.__init__(self, str)
        pass
    def use_libtool(self):
        return True
    pass
    
class SimpleBuildWithoutLibtool(SimpleBuildBase):
    def __init__(self, str):
        SimpleBuildBase.__init__(self, str)
        pass
    def use_libtool(self):
        return False
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SimpleBuildWithLibtool))
suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SimpleBuildWithoutLibtool))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
