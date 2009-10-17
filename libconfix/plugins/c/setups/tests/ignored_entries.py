# Copyright (C) 2008 Joerg Faschingbauer

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
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const
from libconfix.core.machinery.local_package import LocalPackage

import unittest

class IgnoredEntriesTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name='h.h',
            entry=File())
        fs.rootdirectory().add(
            name='c.c',
            entry=File())
        fs.rootdirectory().add(
            name='cc.cc',
            entry=File())
        fs.rootdirectory().add(
            name='lex.l',
            entry=File())
        fs.rootdirectory().add(
            name='llex.ll',
            entry=File())
        fs.rootdirectory().add(
            name='yacc.y',
            entry=File())
        fs.rootdirectory().add(
            name='yyacc.yy',
            entry=File())
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("xx")',
                              'PACKAGE_VERSION("1.2.3")',
                              'from libconfix.frontends.confix2.confix_setup import ConfixSetup',
                              'SETUP([ConfixSetup(use_libtool=False, short_libnames=False)])']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["IGNORE_ENTRIES(names=['h.h',",
                              "                      'c.c',",
                              "                      'cc.cc',",
                              "                      'lex.l',",
                              "                      'llex.ll',",
                              "                      'yacc.y',",
                              "                      'yyacc.yy'])"
                              ]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=None)
        package.boil(external_nodes=[])

        self.failIf(package.rootbuilder().find_entry_builder(path=['h.h']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['c.c']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['cc.cc']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['lex.l']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['llex.ll']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['yacc.y']))
        self.failIf(package.rootbuilder().find_entry_builder(path=['yyacc.yy']))
            
        pass
    pass

class IgnoredEntriesSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(IgnoredEntriesTest('test'))
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(IgnoredEntriesSuite())
    pass
