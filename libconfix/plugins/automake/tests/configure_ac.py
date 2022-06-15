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

from libconfix.plugins.automake.configure_ac import Configure_ac

import unittest, re

class ConfigureACTest(unittest.TestCase):

    re_AC_INIT = re.compile(r'^\s*AC_INIT\((.*),(.*)\)\s*$')
    re_AC_CONFIG_AUXDIR = re.compile(r'^\s*AC_CONFIG_AUX_DIR\(\[(.*)\]\)\s*$')
    re_AC_CONFIG_SRCDIR = re.compile(r'^\s*AC_CONFIG_SRCDIR\((.*)\)\s*$')
    re_AC_CONFIG_FILES = re.compile(r'^\s*AC_CONFIG_FILES\((.*)\)\s*$')
    re_AC_PREREQ = re.compile(r'^\s*AC_PREREQ\((.*)\)\s*$')
    re_white = re.compile(r'\s+')

    def test__basic(self):
        cf_ac = Configure_ac()

        cf_ac.set_packagename('package')
        cf_ac.set_packageversion('1.2.3')
        cf_ac.set_ac_config_aux_dir('auxdir')
        cf_ac.set_unique_file_in_srcdir('some-unique-file')
        cf_ac.set_minimum_autoconf_version('2.53')
        cf_ac.add_ac_config_files('this-subdir/Makefile')
        cf_ac.add_ac_config_files('that-subdir/Makefile')

        found_this_subdir = found_that_subdir = False
        
        for l in cf_ac.lines():
            match = ConfigureACTest.re_AC_INIT.search(l)
            if match is not None:
                self.assertTrue(match.group(1) == 'package')
                self.assertTrue(match.group(2) == '1.2.3')
                continue

            match = ConfigureACTest.re_AC_CONFIG_AUXDIR.search(l)
            if match is not None:
                self.assertTrue(match.group(1) == 'auxdir')
                continue

            match = ConfigureACTest.re_AC_CONFIG_SRCDIR.search(l)
            if match is not None:
                self.assertTrue(match.group(1) == 'some-unique-file')
                continue

            match = ConfigureACTest.re_AC_PREREQ.search(l)
            if match is not None:
                self.assertTrue(match.group(1) == '2.53')
                continue
            
            match = ConfigureACTest.re_AC_CONFIG_FILES.search(l)
            if match is not None:
                list = set(ConfigureACTest.re_white.split(match.group(1)))
                self.assertTrue('this-subdir/Makefile' in list)
                self.assertTrue('that-subdir/Makefile' in list)
                continue
            pass
        
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ConfigureACTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
