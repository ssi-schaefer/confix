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

from libconfix.core.filesys.file import File
from libconfix.plugins.c import helper

import unittest

class MainSearchSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(MainSearch('test'))
        pass
    pass

class MainSearch(unittest.TestCase):
    def test(self):
        file1 = File(lines=['int main() {}'])
        self.assertEqual(helper.has_main(file1), True)

        file2 = File(lines=['int main() {}'])
        file2.set_property(name='MAIN', value=False)
        self.assertEqual(helper.has_main(file2), False)

        file3 = File(lines=[])
        file3.set_property(name='MAIN', value=True)
        self.assertEqual(helper.has_main(file3), True)

        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MainSearchSuite())
    pass
