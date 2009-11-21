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

from libconfix.plugins.automake.out_automake import find_automake_output_builder
from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.hierarchy.implicit_setup import ImplicitDirectorySetup
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const

import unittest

class BuildInfoSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicBuildInfoTest('test'))
        self.addTest(UniqueFlags_n_MacrosTest('test'))
        pass
    pass

class BasicBuildInfoTest(unittest.TestCase):
    def test(self):
        fs = FileSystem(path=['', 'path', 'to', 'it'])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('BasicBuildInfoTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["from libconfix.plugins.c.buildinfo import \\",
                              "    BuildInfo_CommandlineMacros, \\",
                              "    BuildInfo_CFLAGS, \\",
                              "    BuildInfo_CXXFLAGS",
                              "PROVIDE_SYMBOL('lo')",
                              "BUILDINFORMATION(BuildInfo_CommandlineMacros(macros={'macro_key': 'macro_value',",
                              "                                                     'macro': None}))",
                              "BUILDINFORMATION(BuildInfo_CFLAGS(cflags=['some_cflag', 'some_other_cflag']))",
                              "BUILDINFORMATION(BuildInfo_CXXFLAGS(cxxflags=['some_cxxflag', 'some_other_cxxflag']))"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File())
        hi.add(
            name='hi_c.c',
            entry=File(lines=["// CONFIX:REQUIRE_SYMBOL('lo', URGENCY_ERROR)"]))
        hi.add(
            name='hi_cc.cc',
            entry=File(lines=["// CONFIX:REQUIRE_SYMBOL('lo', URGENCY_ERROR)"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        hidir_builder = package.rootbuilder().find_entry_builder(['hi'])
        hi_c_builder = package.rootbuilder().find_entry_builder(['hi', 'hi_c.c'])
        hi_cc_builder = package.rootbuilder().find_entry_builder(['hi', 'hi_cc.cc'])
        self.failIf(hidir_builder is None)
        self.failIf(hi_c_builder is None)
        self.failIf(hi_cc_builder is None)

        # command line macros go to every c like builder (C and C++)
        self.failUnless(hi_c_builder.cmdlinemacros()['macro_key'] == 'macro_value')
        self.failUnless(hi_c_builder.cmdlinemacros()['macro'] == None)
        self.failUnless(hi_cc_builder.cmdlinemacros()['macro_key'] == 'macro_value')
        self.failUnless(hi_cc_builder.cmdlinemacros()['macro'] == None)
        # cflags go to both C and C++
        self.failUnless('some_cflag' in hi_c_builder.cflags())
        self.failUnless('some_other_cflag' in hi_c_builder.cflags())
        self.failUnless('some_cflag' in hi_cc_builder.cflags())
        self.failUnless('some_other_cflag' in hi_cc_builder.cflags())
        # cxxflags go to C++ only
        self.failUnless('some_cxxflag' in hi_cc_builder.cxxflags())
        self.failUnless('some_other_cxxflag' in hi_cc_builder.cxxflags())
        self.failIf('some_cxxflag' in hi_c_builder.cflags())
        self.failIf('some_other_cxxflag' in hi_c_builder.cflags())

        # see if the builders let the info flow into their surrounding
        # Makefile.am.
        hi_dir_output_builder = find_automake_output_builder(hidir_builder)
        self.failIf(hi_dir_output_builder is None)
        
        self.failUnless(hi_dir_output_builder.makefile_am().cmdlinemacros()['macro_key'] == 'macro_value')
        self.failUnless(hi_dir_output_builder.makefile_am().cmdlinemacros()['macro'] == None)
        self.failUnless('some_cflag' in hi_dir_output_builder.makefile_am().am_cflags())
        self.failUnless('some_other_cflag' in hi_dir_output_builder.makefile_am().am_cflags())
        self.failUnless('some_cxxflag' in hi_dir_output_builder.makefile_am().am_cxxflags())
        self.failUnless('some_other_cxxflag' in hi_dir_output_builder.makefile_am().am_cxxflags())
        pass
    pass

class UniqueFlags_n_MacrosTest(unittest.TestCase):

    # buildinformation (in the case of C: cflags, cxxflags,
    # cmdlinemacros) may float to the receiver over multiple
    # paths. (lo, mid1, hi) and (lo, mid2, hi) in this testcase.

    # the receiver is responsible for sorting out duplicates.
    
    def test(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('UniqueFlags_n_MacrosTest')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())

        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('lo')",
                              "EXTERNAL_LIBRARY(",
                              "    cflags=['cflags_token'],",
                              "    cxxflags=['cxxflags_token'],",
                              "    cmdlinemacros={",
                              "        'key': 'value'",
                              "       })"]))

        mid1 = fs.rootdirectory().add(
            name='mid1',
            entry=Directory())
        mid1.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('mid1')",
                              "REQUIRE_SYMBOL('lo')"]))
        mid2 = fs.rootdirectory().add(
            name='mid2',
            entry=Directory())
        mid2.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["PROVIDE_SYMBOL('mid2')",
                              "REQUIRE_SYMBOL('lo')"]))

        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["REQUIRE_SYMBOL('mid1')",
                              "REQUIRE_SYMBOL('mid2')"]))
        hi.add(
            name='file1.cc',
            entry=File())
        hi.add(
            name='file2.cc',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        hi_dirbuilder = package.rootbuilder().find_entry_builder(['hi'])
        self.failIf(hi_dirbuilder is None)
        hi_dir_output_builder = find_automake_output_builder(hi_dirbuilder)
        self.failIf(hi_dir_output_builder is None)

        # see if lo's build information (cflags, cxxflags,
        # cmdlinemacros) made it into hi's build.

        self.failUnless('cflags_token' in hi_dir_output_builder.makefile_am().am_cflags())
        self.failUnless('cxxflags_token' in hi_dir_output_builder.makefile_am().am_cxxflags())
        self.failUnless(hi_dir_output_builder.makefile_am().cmdlinemacros().has_key('key'))
        self.failUnless(hi_dir_output_builder.makefile_am().cmdlinemacros()['key'] == 'value')
        
        # hi's build should not contain duplicates of either of lo's
        # build information.

        unique_cflags = set()
        for f in hi_dir_output_builder.makefile_am().am_cflags():
            self.failIf(f in unique_cflags)
            unique_cflags.add(f)
            pass

        unique_cxxflags = set()
        for f in hi_dir_output_builder.makefile_am().am_cxxflags():
            self.failIf(f in unique_cxxflags)
            unique_cxxflags.add(f)
            pass

        cmdlinemacros = {}
        for macro, value in hi_dir_output_builder.makefile_am().cmdlinemacros().iteritems():
            self.failIf(macro in cmdlinemacros)
            cmdlinemacros[macro] = value
            pass
        
        pass
    pass
    
if __name__ == '__main__':
    unittest.TextTestRunner().run(BuildInfoSuite())
    pass

