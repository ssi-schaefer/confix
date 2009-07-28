# Copyright (C) 2007-2009 Joerg Faschingbauer

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

from check import CheckProgramBase

from libconfix.plugins.automake import bootstrap, configure, make

import os, sys, unittest

class CheckProgramBuildSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CheckProgramBuildWithLibtool('test'))
        self.addTest(CheckProgramBuildWithoutLibtool('test'))
        pass
    pass

class CheckProgramBuildBase(CheckProgramBase):
    def __init__(self, methodName):
        CheckProgramBase.__init__(self, methodName)
        pass
    def test(self):
        self.fs_.sync()
        bootstrap.bootstrap(
            packageroot=self.source_.abspath(),
            path=None,
            use_kde_hack=False,
            argv0=sys.argv[0])
        configure.configure(
            packageroot=self.source_.abspath(),
            builddir=self.build_.abspath(),
            prefix='/dev/null'.split(os.sep),
            readonly_prefixes=[])
        make.make(
            builddir=self.build_.abspath(),
            args=['check'])

        # as a side effect, the test program creates a file for us.
        self.failUnless(os.path.isfile(os.sep.join(self.build_.abspath()+['my-check-was-here'])))
        pass
    pass

class CheckProgramBuildWithLibtool(CheckProgramBuildBase):
    def __init__(self, methodName):
        CheckProgramBuildBase.__init__(self, methodName)
        pass
    def use_libtool(self): return True
    pass

class CheckProgramBuildWithoutLibtool(CheckProgramBuildBase):
    def __init__(self, methodName):
        CheckProgramBuildBase.__init__(self, methodName)
        pass
    def use_libtool(self): return False
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CheckProgramBuildSuite())
    pass

