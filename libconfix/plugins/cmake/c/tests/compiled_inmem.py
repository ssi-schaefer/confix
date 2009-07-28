# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.plugins.cmake.c.setup import CMakeCSetup

from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const

import unittest

class CompiledInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(CompiledInMemoryTest('macros'))
        self.addTest(CompiledInMemoryTest('include_path'))
        self.addTest(CompiledInMemoryTest('whatnot'))
        pass
    pass

class CompiledInMemoryTest(unittest.TestCase):
    def macros(self):
        self.fail()
        pass

    def include_path(self):
        self.fail()
        pass

    def whatnot(self):
        self.fail()
        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(CompiledInMemorySuite())
    pass
