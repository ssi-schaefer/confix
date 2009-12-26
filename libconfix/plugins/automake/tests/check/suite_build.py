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

from libconfix.plugins.automake import bootstrap, configure, make
from libconfix.frontends.confix2.confix_setup import ConfixSetup
from libconfix.setups.explicit_setup import ExplicitSetup
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.testutils.persistent import PersistentTestCase

from check import CheckProgramBase

import os
import sys
import unittest

class CheckProgramBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(Test('test_implicit_with_libtool'))
        self.addTest(Test('test_implicit_without_libtool'))
        self.addTest(Test('test_explicit_with_libtool'))
        self.addTest(Test('test_explicit_without_libtool'))
        pass
    pass

class Test(PersistentTestCase):
    def test_implicit_with_libtool(self):
        fs, source, build = _skeleton(path=self.rootpath())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest.test_implicit_with_libtool")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')"]))
        source.add(
            name='_check_proggy.c',
            entry=File(lines=_check_program(os.sep.join(build.abspath()+['my-check-was-here']))))
        
        _generate(source=source, use_libtool=True, explicit=False)
        fs.sync()
        _build_and_check(source=source, build=build)

        # as a side effect, the test program creates a file for us.
        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['my-check-was-here'])))
        pass
    
    def test_implicit_without_libtool(self):
        fs, source, build = _skeleton(path=self.rootpath())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest.test_implicit_without_libtool")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')"]))
        source.add(
            name='_check_proggy.c',
            entry=File(lines=_check_program(os.sep.join(build.abspath()+['my-check-was-here']))))
        
        _generate(source=source, use_libtool=False, explicit=False)
        fs.sync()
        _build_and_check(source=source, build=build)

        # as a side effect, the test program creates a file for us.
        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['my-check-was-here'])))
        pass
    
    def test_explicit_with_libtool(self):
        fs, source, build = _skeleton(path=self.rootpath())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest.test_implicit_without_libtool")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')",
                              "EXECUTABLE(center=C(filename='main.c'),",
                              "           exename='the-test-program',",
                              "           what=EXECUTABLE_CHECK)"]))
        source.add(
            name='main.c',
            entry=File(lines=_check_program(os.sep.join(build.abspath()+['my-check-was-here']))))
        
        _generate(source=source, use_libtool=True, explicit=True)
        fs.sync()
        _build_and_check(source=source, build=build)

        # as a side effect, the test program creates a file for us.
        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['my-check-was-here'])))
        pass
    
    def test_explicit_without_libtool(self):
        fs, source, build = _skeleton(path=self.rootpath())

        source.add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("CheckProgramTest.test_implicit_without_libtool")',
                              'PACKAGE_VERSION("1.2.3")']))
        source.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["TESTS_ENVIRONMENT('name', 'value')",
                              "EXECUTABLE(center=C(filename='main.c'),",
                              "           exename='the-test-program',",
                              "           what=EXECUTABLE_CHECK)"]))
        source.add(
            name='main.c',
            entry=File(lines=_check_program(os.sep.join(build.abspath()+['my-check-was-here']))))
        
        _generate(source=source, use_libtool=False, explicit=True)
        fs.sync()
        _build_and_check(source=source, build=build)

        # as a side effect, the test program creates a file for us.
        self.failUnless(os.path.isfile(os.sep.join(build.abspath()+['my-check-was-here'])))
        pass

    pass

def _skeleton(path):
    fs = FileSystem(path=path)
    build = fs.rootdirectory().add(
        name='build',
        entry=Directory())

    source = fs.rootdirectory().add(
        name='source',
        entry=Directory())
    return (fs, source, build)

def _generate(source, use_libtool, explicit):
    if explicit:
        setup = ExplicitSetup(use_libtool=use_libtool)
    else:
        setup = ConfixSetup(use_libtool=use_libtool)
        pass
    package = LocalPackage(
        rootdirectory=source,
        setups=[setup])
    package.boil(external_nodes=[])
    package.output()
    pass

def _build_and_check(source, build):
    bootstrap.bootstrap(
        packageroot=source.abspath(),
        path=None,
        use_kde_hack=False,
        argv0=sys.argv[0])
    configure.configure(
        packageroot=source.abspath(),
        builddir=build.abspath(),
        prefix='/dev/null'.split(os.sep),
        readonly_prefixes=[])
    make.make(
        builddir=build.abspath(),
        args=['check'])
    pass

def _check_program(stampfile_path):
    return ['#include <sys/types.h>',
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
            '    return open("'+stampfile_path+'",',
            '                O_CREAT|O_RDWR, S_IRUSR|S_IWUSR) >=0?0:1;',
            '}']

if __name__ == '__main__':
    unittest.TextTestRunner().run(CheckProgramBuildSuite())
    pass

