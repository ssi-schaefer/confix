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

from libconfix.plugins.automake.makefile_am import Makefile_am
import libconfix.plugins.automake.makefileparser as makefileparser

from libconfix.core.utils.error import Error

import unittest

class MakefileAmSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(MakefileAmTest('test_standard_lists'))
        self.addTest(MakefileAmTest('test_errors'))
        self.addTest(MakefileAmTest('test_default_install_directories'))
        self.addTest(MakefileAmTest('test_nondefault_install_directories'))
        pass
    pass

class MakefileAmTest(unittest.TestCase):
    def test_standard_lists(self):
        mf_am = Makefile_am()

        mf_am.add_compound_sources('the_program', 'source.h')
        mf_am.add_compound_sources('the_program', 'source.c')

        mf_am.add_compound_ldflags('the_program', '-some-flag')
        mf_am.add_compound_ldflags('the_program', '-some-other-flag')

        mf_am.add_compound_libadd('libsome_ltlibrary_la', 'some_library')
        mf_am.add_compound_libadd('libsome_ltlibrary_la', 'some_other_library')

        mf_am.add_compound_ldadd('the_program', 'some_library')
        mf_am.add_compound_ldadd('the_program', 'some_other_library')

        mf_am.add_am_cflags('-some-cflag')
        mf_am.add_am_cflags('-some-other-cflag')
        mf_am.add_am_cxxflags('-some-cxxflag')
        mf_am.add_am_cxxflags('-some-other-cxxflag')
        mf_am.add_am_lflags('-some-lflag')
        mf_am.add_am_lflags('-some-other-lflag')
        mf_am.add_am_yflags('-some-yflag')
        mf_am.add_am_yflags('-some-other-yflag')

        mf_am.add_extra_dist('some-extra-dist-file')
        mf_am.add_extra_dist('some-other-extra-dist-file')
        mf_am.add_mostlycleanfiles('some-mostlycleanfile')
        mf_am.add_mostlycleanfiles('some-other-mostlycleanfile')
        mf_am.add_cleanfiles('some-cleanfile')
        mf_am.add_cleanfiles('some-other-cleanfile')
        mf_am.add_distcleanfiles('some-distcleanfile')
        mf_am.add_distcleanfiles('some-other-distcleanfile')
        mf_am.add_maintainercleanfiles('some-maintainercleanfiles')
        mf_am.add_maintainercleanfiles('some-other-maintainercleanfiles')
        
        mf_am.add_ltlibrary('libsome-ltlibrary.la')
        mf_am.add_ltlibrary('libsome-other-ltlibrary.la')
        mf_am.add_library('libsome-library.a')
        mf_am.add_library('libsome-other-library.a')
        mf_am.add_bin_program('some-program')
        mf_am.add_bin_program('some-other-program')
        mf_am.add_bin_script('some-script')
        mf_am.add_bin_script('some-other-script')
        mf_am.add_check_program('some-check-program')
        mf_am.add_check_program('some-other-check-program')
        mf_am.add_dir_primary('xxx', 'YYY', 'some-xxx-YYY-thing')
        mf_am.add_dir_primary('xxx', 'YYY', 'some-other-xxx-YYY-thing')
        mf_am.add_dir_primary('aaa', 'YYY', 'some-aaa-YYY-thing')
        mf_am.add_dir_primary('aaa', 'YYY', 'some-other-aaa-YYY-thing')

        mf_am.add_built_sources('some-built-source')
        mf_am.add_built_sources('some-other-built-source')

        mf_am.add_includepath('-Isome_path')
        mf_am.add_includepath('-Isome_other_path')

        mf_am.add_cmdlinemacro('key1', 'value1')
        mf_am.add_cmdlinemacro('key2', 'value2')
        mf_am.add_cmdlinemacro('key3')
        mf_am.add_cmdlinemacro('key4')

        mf_am.add_tests_environment(name='name1', value='value1')
        mf_am.add_tests_environment(name='name2', value='value2')

        ##########################
        lines = mf_am.lines()
        elements = makefileparser.parse_makefile(lines=lines)

        self.failUnlessEqual(set(makefileparser.find_list(name='the_program_SOURCES', elements=elements).values()),
                             set(['source.h', 'source.c']))
        self.failUnlessEqual(makefileparser.find_list(name='the_program_LDFLAGS', elements=elements).values(),
                             ['-some-flag', '-some-other-flag'])
        self.failUnlessEqual(makefileparser.find_list(name='libsome_ltlibrary_la_LIBADD', elements=elements).values(),
                             ['some_library', 'some_other_library'])
        self.failUnlessEqual(makefileparser.find_list(name='the_program_LDADD', elements=elements).values(),
                             ['some_library', 'some_other_library'])
        self.failUnlessEqual(set(makefileparser.find_list(name='AM_CFLAGS', elements=elements).values()),
                             set(['-some-cflag', '-some-other-cflag']))
        self.failUnlessEqual(set(makefileparser.find_list(name='AM_CXXFLAGS', elements=elements).values()),
                             set(['-some-cxxflag', '-some-other-cxxflag']))
        self.failUnlessEqual(set(makefileparser.find_list(name='AM_LFLAGS', elements=elements).values()),
                             set(['-some-lflag', '-some-other-lflag']))
        self.failUnlessEqual(set(makefileparser.find_list(name='AM_YFLAGS', elements=elements).values()),
                             set(['-some-yflag', '-some-other-yflag']))
        self.failUnlessEqual(set(makefileparser.find_list(name='EXTRA_DIST', elements=elements).values()),
                             set(['some-extra-dist-file', 'some-other-extra-dist-file']))
        self.failUnlessEqual(set(makefileparser.find_list(name='MOSTLYCLEANFILES', elements=elements).values()),
                             set(['some-mostlycleanfile', 'some-other-mostlycleanfile']))
        self.failUnlessEqual(set(makefileparser.find_list(name='CLEANFILES', elements=elements).values()),
                             set(['some-cleanfile', 'some-other-cleanfile']))
        self.failUnlessEqual(set(makefileparser.find_list(name='DISTCLEANFILES', elements=elements).values()),
                             set(['some-distcleanfile', 'some-other-distcleanfile']))
        self.failUnlessEqual(set(makefileparser.find_list(name='MAINTAINERCLEANFILES', elements=elements).values()),
                             set(['some-maintainercleanfiles', 'some-other-maintainercleanfiles']))
        self.failUnlessEqual(makefileparser.find_list(name='lib_LTLIBRARIES', elements=elements).values(),
                             ['libsome-ltlibrary.la', 'libsome-other-ltlibrary.la'])
        self.failUnlessEqual(makefileparser.find_list(name='lib_LIBRARIES', elements=elements).values(),
                             ['libsome-library.a', 'libsome-other-library.a'])
        self.failUnlessEqual(makefileparser.find_list(name='bin_PROGRAMS', elements=elements).values(),
                             ['some-program', 'some-other-program'])
        self.failUnlessEqual(makefileparser.find_list(name='bin_SCRIPTS', elements=elements).values(),
                             ['some-script', 'some-other-script'])
        self.failUnlessEqual(makefileparser.find_list(name='check_PROGRAMS', elements=elements).values(),
                             ['some-check-program', 'some-other-check-program'])
        self.failUnlessEqual(makefileparser.find_list(name='xxx_YYY', elements=elements).values(),
                             ['some-xxx-YYY-thing', 'some-other-xxx-YYY-thing'])
        self.failUnlessEqual(makefileparser.find_list(name='aaa_YYY', elements=elements).values(),
                             ['some-aaa-YYY-thing', 'some-other-aaa-YYY-thing'])
        self.failUnlessEqual(set(makefileparser.find_list(name='BUILT_SOURCES', elements=elements).values()),
                             set(['some-built-source', 'some-other-built-source']))

        # mf_am.add_includepath() and add_cmdlinemacro() goes into
        # AM_CPPFLAGS
        am_cppflags = makefileparser.find_list(name='AM_CPPFLAGS', elements=elements).values()
        self.failUnless('-Isome_path' in am_cppflags)
        self.failUnless('-Isome_other_path' in am_cppflags)
        self.failUnless('-Dkey1=value1' in am_cppflags)
        self.failUnless('-Dkey2=value2' in am_cppflags)
        self.failUnless('-Dkey3' in am_cppflags)
        self.failUnless('-Dkey4' in am_cppflags)

        # TESTS_ENVIRONMENT
        tests_environment = makefileparser.find_list(name='TESTS_ENVIRONMENT', elements=elements).values()
        self.failUnlessEqual(len(tests_environment), 2)
        self.failUnless('name1=value1' in tests_environment)
        self.failUnless('name2=value2' in tests_environment)
        
        pass

    def test_errors(self):
        mf_am = Makefile_am()

        mf_am.add_compound_sources('the_program', 'source.c')
        self.assertRaises(Error, mf_am.add_compound_sources, 'the_program', 'source.c')

        mf_am.add_dir_primary('dir', 'PRIMARY', 'something')
        self.assertRaises(Error, mf_am.add_dir_primary, 'dir', 'PRIMARY', 'something')
        
        pass

    def test_default_install_directories(self):
        mf_am = Makefile_am()
        # default directory
        mf_am.add_to_install_directory(symbolicname='',
                                       family='HEADERS',
                                       files=['defaultfile1.h', 'defaultfile2.h'])
        mf_am.add_to_install_directory(symbolicname='',
                                       family='HEADERS',
                                       files=['defaultfile0.h'])

        lines = mf_am.lines()
        elements = makefileparser.parse_makefile(lines=lines)
        
        headerlist = makefileparser.find_list(name='include_HEADERS', elements=elements)
        self.failIf(headerlist is None)
        self.failUnless(headerlist.values() == ['defaultfile1.h', 'defaultfile2.h', 'defaultfile0.h'])
        
        pass

    def test_nondefault_install_directories(self):
        mf_am = Makefile_am()

        mf_am.define_install_directory(symbolicname='publicheaders_blah',
                                       dirname='$(includedir)/blah')
        mf_am.add_to_install_directory(symbolicname='publicheaders_blah',
                                       family='HEADERS',
                                       files=['nondefaultfile1.h', 'nondefaultfile2.h'])
        mf_am.add_to_install_directory(symbolicname='publicheaders_blah',
                                       family='HEADERS',
                                       files=['nondefaultfile0.h'])

        lines = mf_am.lines()

        elements = makefileparser.parse_makefile(lines=lines)

        dirdefinition = makefileparser.find_list(name='publicheaders_blahdir', elements=elements)
        self.failIf(dirdefinition is None)
        self.failUnless(len(dirdefinition) == 1)
        self.failUnless(dirdefinition[0] == '$(includedir)/blah')

        headerlist = makefileparser.find_list(name='publicheaders_blah_HEADERS', elements=elements)
        self.failIf(headerlist is None)
        self.failUnless(headerlist.values() == ['nondefaultfile1.h', 'nondefaultfile2.h', 'nondefaultfile0.h'])
        
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MakefileAmSuite())
    pass
