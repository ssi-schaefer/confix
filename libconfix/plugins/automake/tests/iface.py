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

from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.setups.explicit_setup import ExplicitSetup

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.utils import const
from libconfix.frontends.confix2.confix_setup import ConfixSetup

import unittest

class InterfaceTest(unittest.TestCase):
    def test__MAKEFILE_AM(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["MAKEFILE_AM(line='"+token+"')"]))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        rootdir_automake_builder = find_automake_output_builder(package.rootbuilder())
        self.assertTrue(token in rootdir_automake_builder.makefile_am().lines())
        pass

    def test__ADD_EXTRA_DIST(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=["PACKAGE_NAME('"+self.__class__.__name__+"')",
                              "PACKAGE_VERSION('1.2.3')"]))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["ADD_EXTRA_DIST(filename='file')"]))
        fs.rootdirectory().add(
            name='file',
            entry=File())

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ExplicitSetup(use_libtool=True)])
        package.boil(external_nodes=[])

        rootdir_automake_builder = find_automake_output_builder(package.rootbuilder())
        self.assertTrue('file' in rootdir_automake_builder.makefile_am().extra_dist())
        pass
        
    def test__CONFIGURE_AC_ACINCLUDE_M4_local(self):

        # We pass flags=[LOCAL] explicitly, to both ACINCLUDE_M4() and
        # CONFIGURE_AC(), and check if both go into acinclude.m4 and
        # configure.ac.
        
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=["CONFIGURE_AC(lines=['the_token_for_configure_ac'],",
                              "             order=AC_PROGRAMS,",
                              "             flags=[LOCAL])",
                              "ACINCLUDE_M4(lines=['the_token_for_acinclude_m4'],",
                              "             flags=[LOCAL])"]))
        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.assertFalse(configure_ac is None)
        self.assertFalse(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass
    
    def test__CONFIGURE_AC_ACINCLUDE_M4_propagate(self):

        """ We pass flags=[PROPAGATE] explicitly, to both
        ACINCLUDE_M4() and CONFIGURE_AC(), propagate it to a dependent
        node,"hi", and check if both go into acinclude.m4 and configure.ac."""

        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_SYMBOL("lo")',
                              'CONFIGURE_AC(lines=["the_token_for_configure_ac"],',
                              '             order=AC_PROGRAMS,',
                              '             flags=[PROPAGATE])',
                              'ACINCLUDE_M4(lines=["the_token_for_acinclude_m4"],',
                              '             flags=[PROPAGATE])']))
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['REQUIRE_SYMBOL("lo", URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.assertFalse(configure_ac is None)
        self.assertFalse(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass

    def test__CONFIGURE_AC_ACINCLUDE_M4_defaults(self):

        """ We do not pass any of flags, propagate it, and ..."""
        
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("blah")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File())
        lo = fs.rootdirectory().add(
            name='lo',
            entry=Directory())
        lo.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['PROVIDE_SYMBOL("lo")',
                              'CONFIGURE_AC(lines=["the_token_for_configure_ac"],',
                              '             order=AC_PROGRAMS)',
                              'ACINCLUDE_M4(lines=["the_token_for_acinclude_m4"])']))
        hi = fs.rootdirectory().add(
            name='hi',
            entry=Directory())
        hi.add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['REQUIRE_SYMBOL("lo", URGENCY_ERROR)']))

        package = LocalPackage(rootdirectory=fs.rootdirectory(),
                               setups=[ConfixSetup(use_libtool=False)])
        package.boil(external_nodes=[])
        package.output()

        configure_ac = fs.rootdirectory().find(['configure.ac'])
        acinclude_m4 = fs.rootdirectory().find(['acinclude.m4'])
        self.assertFalse(configure_ac is None)
        self.assertFalse(acinclude_m4 is None)

        for line in configure_ac.lines():
            if line == 'the_token_for_configure_ac':
                break
            pass
        else:
            self.fail()
            pass

        for line in acinclude_m4.lines():
            if line == 'the_token_for_acinclude_m4':
                break
            pass
        else:
            self.fail()
            pass
        pass

    
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(InterfaceTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
