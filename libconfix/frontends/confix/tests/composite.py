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

import unittest

from libconfix.frontends.confix.composite_config import CompositeConfiguration 
from libconfix.frontends.confix.cmdline_config import CommandlineConfiguration 
from libconfix.frontends.confix.default_config import DefaultConfiguration
from libconfix.frontends.confix.configfile import ConfigFile
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem

class CompositeConfigSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CompositeConfigTest('test'))
        pass
    pass

class CompositeConfigTest(unittest.TestCase):
    def test(self):
        config = CompositeConfiguration()
        config.add(CommandlineConfiguration(
            configdir='not that interesting since not part of Configuration interface',
            configfile=None,
            profile='not that interesting since not part of Configuration interface',
            packageroot='/package/root',
            overlayroot='/overlay/root',
            packagename='packagename',
            packageversion='packageversion',
            prefix='/the/prefix',
            readonly_prefixes=['/one/readonly/prefix', '/two/readonly/prefixes'],
            buildroot='/build/root',
            builddir=None,
            short_libnames=None,
            use_libtool=None,
            use_bulk_install=None,
            use_kde_hack=None,
            verbosity=1,
            trace=None,
            debug=None,
            print_timings=None,
            message_prefix=None,
            advanced=None,
            make_args=None,
            ))

        fs = FileSystem(path=['', 'home', 'jfasch'])
        confixfile=fs.rootdirectory().add(
            name='.confix',
            entry=File(lines=["the_profile = {",
                              "    'PREFIX': '/some/prefix',",
                              "    'READONLY_PREFIXES': ['/some/prefix', '/some/other/prefix'],",
                              "    'SHORT_LIBNAMES': True,",
                              "    'USE_LIBTOOL': True,",
                              "    'USE_BULK_INSTALL': True,",
                              "    'BUILDROOT': '/some/build/dir',",
                              "    'MESSAGE_PREFIX': 'some-message-prefix',",
                              "    'PRINT_TIMINGS': True,",
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
                              "    'the_profile': the_profile,",
                              "}",
                              ]))
        config.add(ConfigFile(file=confixfile).get_profile('the_profile'))
        config.add(DefaultConfiguration())

        self.failUnlessEqual(config.packageroot(), '/package/root') # cmdline
        self.failUnlessEqual(config.overlayroot(), '/overlay/root') # cmdline
        self.failUnlessEqual(config.packagename(), 'packagename') # cmdline
        self.failUnlessEqual(config.packageversion(), 'packageversion') # cmdline
        self.failUnlessEqual(config.prefix(), '/the/prefix') # cmdline overriding profile
        self.failUnlessEqual(config.readonly_prefixes(), ['/one/readonly/prefix', '/two/readonly/prefixes']) # cmdline overriding profile
        self.failUnlessEqual(config.buildroot(), '/build/root') # cmdline
        self.failUnless(config.builddir() is None) # not set at all
        self.failUnless(config.short_libnames() is True) # profile
        self.failUnless(config.use_libtool() is True) # profile
        self.failUnless(config.use_bulk_install() is True) # profile
        self.failUnless(config.use_kde_hack() is False) # default
        self.failUnless(config.print_timings() is True) # profile
        self.failUnlessEqual(config.message_prefix(), 'some-message-prefix')
        self.failUnlessEqual(config.advanced(), False) # profile
        self.failUnlessEqual(config.configure_env()['CFLAGS'], '-some-cflags')
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CompositeConfigSuite())
    pass
