# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.testutils.persistent import PersistentTestCase

from libconfix.frontends.confix2.confix_setup import ConfixSetup

import os, unittest

class CheckProgramBase(PersistentTestCase):
    def __init__(self, methodName):
        PersistentTestCase.__init__(self, methodName)
        self.fs_ = None
        pass

    def use_libtool(self): assert 0

    def setUp(self):
        assert False
        PersistentTestCase.setUp(self)
        self.fs_ = FileSystem(path=self.rootpath())

        self.build_ = self.fs_.rootdirectory().add(
            name='build',
            entry=Directory())

        self.source_ = self.fs_.rootdirectory().add(
            name='source',
            entry=Directory())
        self.source_.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest")',
                              'PACKAGE_VERSION("1.2.3")']))
        self.source_.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')"]))
        self.source_.add(
            name='_check_proggy.c',
            entry=File(lines=['#include <sys/types.h>',
                              '#include <sys/stat.h>',
                              '#include <fcntl.h>',
                              '#include <stdlib.h>',
                              '#include <string.h>',

                              'int main(void) {',
                              '    const char* name = getenv("name");',
                              '    if (!name)',
                              '        return 1;',
                              '    if (strcmp(name, "value"))',
                              '        return 1;',
                              '    return open("'+os.sep.join(self.build_.abspath()+['my-check-was-here'])+'",',
                              '                O_CREAT|O_RDWR) >=0?0:1;',
                              '}']))
        
        self.package_ = LocalPackage(rootdirectory=self.source_,
                                     setups=[ConfixSetup(short_libnames=False, use_libtool=self.use_libtool())])
        self.package_.boil(external_nodes=[])
        self.package_.output()
        pass

    pass

