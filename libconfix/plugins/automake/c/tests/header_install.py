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

from libconfix.plugins.automake import makefileparser
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

from libconfix.testutils import dirhier

import unittest

class HeaderInstallInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(BasicHeaderInstallTest('test_zerodeep'))
        self.addTest(BasicHeaderInstallTest('test_onedeep'))
        self.addTest(BasicHeaderInstallTest('test_twodeep'))
        pass
    pass

class BasicHeaderInstallTest(unittest.TestCase):
    def test_zerodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=[])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False,
                                                   use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        # installation of file.h goes directly to $(includedir); no
        # subdir involved.
        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)

        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() is None)
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])

        # no local install is done; user will have his includepath
        # pointed to $(srcdir)
        pass

    def test_onedeep(self):

        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False,
                                                   use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        # public installation goes to $(includedir)/xxx; see if the
        # subdir stuff is handled correctly.
        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)
        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('publicheader_xxx')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() == '$(includedir)/xxx')
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])

        # private installation stuff.

        # all-local -> confix-install-local -> $(top_builddir)/confix_include/file.h -> $(top_builddir)/confix_include

        confix_install_local = makefileparser.find_rule(
            targets=['confix-install-local'],
            elements=rootdir_output_builder.makefile_am().elements())
        install_file_h = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include/xxx/file.h'],
            elements=rootdir_output_builder.makefile_am().elements())
        mkdir = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include/xxx'],
            elements=rootdir_output_builder.makefile_am().elements())
        self.failIf(confix_install_local is None)
        self.failIf(install_file_h is None)
        self.failIf(mkdir is None)
        self.failUnless('confix-install-local' in rootdir_output_builder.makefile_am().all_local().prerequisites())
        self.failUnless('$(top_builddir)/confix_include/xxx/file.h' in confix_install_local.prerequisites())

        # clean-local -> confix-clean-local -> $(top_builddir)/confix_include/file.h-clean

        confix_clean_local = makefileparser.find_rule(
            targets=['confix-clean-local'],
            elements=rootdir_output_builder.makefile_am().elements())
        clean_file_h = makefileparser.find_rule(
            targets=['$(top_builddir)/confix_include/xxx/file.h-clean'],
            elements=rootdir_output_builder.makefile_am().elements())
        self.failIf(confix_clean_local is None)
        self.failIf(clean_file_h is None)
        self.failUnless('confix-clean-local' in rootdir_output_builder.makefile_am().clean_local().prerequisites())
        self.failUnless('$(top_builddir)/confix_include/xxx/file.h-clean' in confix_clean_local.prerequisites())
        
        pass

    def test_twodeep(self):
        fs = dirhier.packageroot()
        file_h = fs.rootdirectory().add(name='file.h',
                                        entry=File())
        file_h.set_property(name='INSTALLPATH_CINCLUDE', value=['xxx/yyy'])
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(short_libnames=False,
                                                   use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        rootdir_output_builder = find_automake_output_builder(package.rootbuilder())
        self.failIf(rootdir_output_builder is None)

        directory_definition = rootdir_output_builder.makefile_am().install_directories().get('publicheader_xxxyyy')
        self.failIf(directory_definition is None)
        self.failUnless(directory_definition.dirname() == '$(includedir)/xxx/yyy')
        self.failIf(directory_definition.files('HEADERS') is None)
        self.failUnless(directory_definition.files('HEADERS') == ['file.h'])
        pass
        
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(HeaderInstallInMemorySuite())
    pass
