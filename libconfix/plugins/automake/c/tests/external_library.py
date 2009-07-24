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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.plugins.automake.c.out_c import LibraryOutputBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

from libconfix.setups.explicit_setup import ExplicitSetup

import unittest

class ExternalLibraryInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ExternalLibraryTest('testIncludePath'))
        self.addTest(ExternalLibraryTest('testCmdlineMacros'))
        self.addTest(ExternalLibraryTest('testCFlags'))
        self.addTest(ExternalLibraryTest('testCXXFlags'))
        self.addTest(ExternalLibraryTest('testLinkery'))
        pass
    pass

class ExternalLibraryTest(unittest.TestCase):
    def setUp(self):
        fs = FileSystem(path=['', 'path', 'to', 'it'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('ExternalLibraryTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['DIRECTORY(["lolo"])',
                              'DIRECTORY(["lo"])',
                              'DIRECTORY(["hi"])',
                              ]))
        lolo = fs.rootdirectory().add(
            name='lolo',
            entry=Directory())
        lolo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('lolo')",
                              "EXTERNAL_LIBRARY(",
                              "    incpath=['-I/the/include/path/of/lolo'],",
                              "    libpath=['-L/the/first/library/path/of/lolo', '-L/the/second/library/path/of/lolo'],",
                              "    cflags=['lolo_cflags'],",
                              "    cxxflags=['lolo_cxxflags'],",
                              "    cmdlinemacros={'cmdlinemacro_lolo': 'value_lolo'},",
                              "    libs=['-llolo'])"]))

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('lolo', URGENCY_ERROR)",
                              "PROVIDE_SYMBOL('lo')",
                              "EXTERNAL_LIBRARY(",
                              "    incpath=['-I/the/include/path/of/lo'],",
                              "    libpath=['-L/the/first/library/path/of/lo', '-L/the/second/library/path/of/lo'],",
                              "    cflags=['lo_cflags'],",
                              "    cxxflags=['lo_cxxflags'],",
                              "    cmdlinemacros={'cmdlinemacro_lo': 'value_lo'},",
                              "    libs=['-llo'])"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines = ['hi_c = C(filename="hi_c.c")',
                                'hi_cc = CXX(filename="hi_cc.cc")',
                                'LIBRARY(basename="hi", members=[hi_c, hi_cc])'
                                ]))
        hi.add(
            name='hi_c.c',
            entry=File(lines=["// CONFIX:REQUIRE_SYMBOL('lo', URGENCY_ERROR)"]))
        hi.add(
            name='hi_cc.cc',
            entry=File(lines=["// CONFIX:REQUIRE_SYMBOL('lo', URGENCY_ERROR)"]))

        self.__package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        self.__package.boil(external_nodes=[])
        self.__package.output()

        pass
    
    def tearDown(self):
        self.__package = None
        pass

    def testIncludePath(self):
        # lolo must not be seen in lo's include path since nothing is
        # built there
        lodir_builder = self.__package.rootbuilder().find_entry_builder(['lo'])
        self.failIf(lodir_builder is None) # paranoia
        lodir_output_builder = find_automake_output_builder(lodir_builder)
        self.failIf(lodir_output_builder is None)
        
        self.failIf('-I/the/include/path/of/lolo' in lodir_output_builder.makefile_am().includepath())
        
        # hi is building something, so we should definitely see
        # include paths. lo must come before lolo in hi's include
        # path.
        hidir_builder = self.__package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)
        
        pos_lo = pos_lolo = None
        i = -1
        for ip in hidir_output_builder.makefile_am().includepath():
            i += 1
            if ip == '-I/the/include/path/of/lolo':
                pos_lolo = i
                continue
            if ip == '-I/the/include/path/of/lo':
                pos_lo = i
                continue
            pass
        self.failIf(pos_lo is None)
        self.failIf(pos_lolo is None)
        
        self.failUnless(pos_lo < pos_lolo)
        pass

    def testCmdlineMacros(self):
        hidir_builder = self.__package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)

        self.failIf(hidir_output_builder.makefile_am().cmdlinemacros().get('cmdlinemacro_lolo') is None)
        self.failUnless(hidir_output_builder.makefile_am().cmdlinemacros().get('cmdlinemacro_lolo') == 'value_lolo')
        self.failIf(hidir_output_builder.makefile_am().cmdlinemacros().get('cmdlinemacro_lo') is None)
        self.failUnless(hidir_output_builder.makefile_am().cmdlinemacros().get('cmdlinemacro_lo') == 'value_lo')
        pass

    def testCFlags(self):
        hidir_builder = self.__package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)
        
        self.failUnless('lolo_cflags' in hidir_output_builder.makefile_am().am_cflags())
        self.failUnless('lo_cflags' in hidir_output_builder.makefile_am().am_cflags())
        pass

    def testCXXFlags(self):
        hidir_builder = self.__package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)

        self.failUnless('lolo_cxxflags' in hidir_output_builder.makefile_am().am_cxxflags())
        self.failUnless('lo_cxxflags' in hidir_output_builder.makefile_am().am_cxxflags())
        pass

    def testLinkery(self):
        hidir_builder = self.__package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hidir_builder is None)
        hidir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hidir_output_builder is None)

        # paths (-L): lo (first and second) must come before lolo
        # (first and second). the order of lo's and lolo's both paths
        # must be preserved (in other words, first before second)

        # libraries (-l): lo before lolo.
        pos_Llo_first = pos_Llo_second = pos_Llolo_first = pos_Llolo_second = pos_llolo = pos_llo = None
        i = -1
        for lp in hidir_output_builder.makefile_am().compound_libadd(compound_name='libhi_la'):
            i += 1
            if lp == '-L/the/first/library/path/of/lo':
                pos_Llo_first = i
                continue
            if lp == '-L/the/second/library/path/of/lo':
                pos_Llo_second = i
                continue
            if lp == '-L/the/first/library/path/of/lolo':
                pos_Llolo_first = i
                continue
            if lp == '-L/the/second/library/path/of/lolo':
                pos_Llolo_second = i
                continue
            if lp == '-llo':
                pos_llo = i
                continue
            if lp == '-llolo':
                pos_llolo = i
                continue
            pass

        self.failIf(pos_Llo_first is None)
        self.failIf(pos_Llo_second is None)
        self.failIf(pos_Llolo_first is None)
        self.failIf(pos_Llolo_second is None)
        self.failIf(pos_llolo is None)
        self.failIf(pos_llo is None)
        
        self.failUnless(pos_Llo_first < pos_Llo_second)
        self.failUnless(pos_Llo_second < pos_Llolo_first)
        self.failUnless(pos_Llolo_first < pos_Llolo_second)
        self.failUnless(pos_llo < pos_llolo)
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ExternalLibraryInMemorySuite())
    pass

