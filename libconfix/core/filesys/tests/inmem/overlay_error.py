# Copyright (C) 2007 Joerg Faschingbauer

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
from libconfix.core.filesys.overlay_filesys import OverlayFileSystem
from libconfix.core.filesys.overlay_directory import OverlayDirectory

import unittest

class OverlayErrorSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(OverlayErrorTest('test'))
        pass
    pass

class OverlayErrorTest(unittest.TestCase):
    def test(self):
        fs_orig = FileSystem(path=[])
        fs_overlay = FileSystem(path=[])
        fs_overlay.rootdirectory().add(
            name='dir',
            entry=Directory())
        fs = OverlayFileSystem(original=fs_orig, overlay=fs_overlay)
        dir = fs.rootdirectory().get('dir')
        try:
            dir.add(
                name='file',
                entry=File())
            self.fail()
        except OverlayDirectory.OverlayAddError: pass
        pass
    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(OverlayErrorSuite())
    pass
