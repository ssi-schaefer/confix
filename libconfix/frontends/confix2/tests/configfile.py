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

from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.frontends.confix2.configfile import ConfigFile

import unittest

class ConfigFileTest(unittest.TestCase):
    def setUp(self):
        fs = FileSystem(path=['', 'home', 'jfasch', '.confix2'])
        self.file_ = fs.rootdirectory().add(
            name='rc',
            entry=File(lines=["the_profile = {",
                              "    'PREFIX': '/some/prefix',",
                              "    'READONLY_PREFIXES': ['/some/prefix', '/some/other/prefix'],",
                              "    'SHORT_LIBNAMES': True,",
                              "    'USE_LIBTOOL': True,",
                              "    'USE_BULK_INSTALL': True,",
                              "    'USE_KDE_HACK': False,",
                              "    'BUILDROOT': '/some/build/dir',",
                              "    'MESSAGE_PREFIX': 'some-message-prefix',",
                              "    'PRINT_TIMINGS': False,",
                              "    'ADVANCED': False,",
                              "",
                              "    'CONFIGURE': {",
                              "        'ENV': {",
                              "            'CFLAGS': '-some-cflags',",
                              "            'CXXFLAGS': '-some-cxxflags',",
                              "            'INSTALL': '/bin/install'",
                              "        },",
                              "        'ARGS': ['--arg1', '--arg2'],",
                              "    },",
                              "}",
                              "PROFILES = {",
                              "    'some_profile': the_profile,",
                              "}",
                              ]))
        pass
    
    def test(self):
        configfile = ConfigFile(file=self.file_)
        profile = configfile.get_profile('some_profile')
        self.failIf(profile is None)

        self.failUnlessEqual(profile.prefix(), '/some/prefix')
        self.failUnlessEqual(profile.readonly_prefixes(), ['/some/prefix', '/some/other/prefix'])
        self.failUnlessEqual(profile.buildroot(), '/some/build/dir')
        self.failUnlessEqual(profile.short_libnames(), True)
        self.failUnlessEqual(profile.use_libtool(), True)
        self.failUnlessEqual(profile.use_bulk_install(), True)
        self.failUnlessEqual(profile.use_kde_hack(), False)
        self.failUnlessEqual(profile.print_timings(), False)
        self.failUnlessEqual(profile.message_prefix(), 'some-message-prefix')
        self.failUnlessEqual(profile.advanced(), False)
        self.failUnlessEqual(profile.configure_args(), ['--arg1', '--arg2'])

        configure_env = profile.configure_env()
        self.failIf(configure_env is None)
        self.failUnless(configure_env.get('CFLAGS') == '-some-cflags')
        self.failUnless(configure_env.get('CXXFLAGS') == '-some-cxxflags')
        self.failUnless(configure_env.get('INSTALL') == '/bin/install')
        
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(ConfigFileTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
