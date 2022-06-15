# Copyright (C) 2007-2013 Joerg Faschingbauer

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
from libconfix.core.filesys.directory import Directory, DirectoryState
from libconfix.core.filesys.file import File, FileState
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.utils.error import Error

from libconfix.testutils.persistent import PersistentTestCase

import unittest, os, stat, shutil, sys

class BasicTest(PersistentTestCase):
    def test__very_basic(self):
        fs = FileSystem(path=['a', 'b'])
        subdir = Directory()
        subdir.add(name='file', entry=File())
        fs.rootdirectory().add(name='subdir', entry=subdir)

        file = fs.rootdirectory().find(['subdir', 'file'])
        self.assertNotEqual(file, None)
        self.assertTrue(isinstance(file, File))

        self.assertEqual(subdir.abspath(), ['a', 'b', 'subdir'])
        self.assertEqual(subdir.relpath(fs.rootdirectory()), ['subdir'])

        self.assertRaises(Directory.AlreadyMounted, fs.rootdirectory().add, name='subdir', entry=File())

        pass

    def test__relative_path(self):
        fs = FileSystem(path=['a', 'b'])
        subdir = fs.rootdirectory().add(name='subdir', entry=Directory())
        subsubdir = subdir.add(name='subsubdir', entry=Directory())
        file = subsubdir.add(name='file', entry=File())

        self.assertTrue(subsubdir.relpath(fs.rootdirectory()) == ['subdir', 'subsubdir'])
        self.assertTrue(file.relpath(subdir) == ['subsubdir', 'file'])
        pass
        
    def test__sync_mem2sync(self):
        fs = FileSystem(path=self.rootpath())
        subdir = Directory(mode=0o700)
        fs.rootdirectory().add(name='subdir', entry=subdir)
        file = File(mode=0o755)
        subdir.add(name='file', entry=file)

        self.assertEqual(fs.rootdirectory().state(), DirectoryState.INMEMORY)
        self.assertEqual(subdir.state(), DirectoryState.INMEMORY)
        self.assertEqual(file.state(), FileState.NEW)
        
        fs.sync()

        self.assertEqual(fs.rootdirectory().state(), DirectoryState.SYNC)
        self.assertEqual(subdir.state(), DirectoryState.SYNC)
        self.assertEqual(file.state(), FileState.SYNC_INMEM)

        self.assertTrue(os.path.isdir(os.sep.join(self.rootpath())))
        self.assertTrue(os.path.isdir(os.sep.join(self.rootpath()+['subdir'])))
        self.assertTrue(os.path.isfile(os.sep.join(self.rootpath()+['subdir', 'file'])))

        self.assertEqual(stat.S_IMODE(os.stat(os.sep.join(self.rootpath()+['subdir'])).st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(os.stat(os.sep.join(self.rootpath()+['subdir', 'file'])).st_mode), 0o755)
        pass

    def test__sync_dirty2sync(self):
        fs = FileSystem(path=self.rootpath())
        subdir = Directory(mode=0o700)
        fs.rootdirectory().add(name='subdir', entry=subdir)
        file = File(mode=0o755)
        subdir.add(name='file', entry=file)

        fs.sync()

        newfile = File()
        subdir.add(name='newfile', entry=newfile)
        self.assertEqual(newfile.state(), FileState.NEW)

        fs.sync()

        self.assertEqual(newfile.state(), FileState.SYNC_INMEM)
        self.assertTrue(os.path.isfile(os.sep.join(self.rootpath()+['subdir', 'newfile'])))

        pass

    def test__sync_filechange(self):
        # build up filesystem with our test file and sync it.
        fs = FileSystem(path=self.rootpath())
        file = File(lines=['line 0'])
        fs.rootdirectory().add(name='file', entry=file)
        file.add_lines(['line 1', 'line 2', 'line 3'])
        fs.sync()

        # re-read our file and see if everything is there
        fs = scan_filesystem(path=self.rootpath())
        file = fs.rootdirectory().find(['file'])
        lines = file.lines()
        self.assertEqual(lines[0], 'line 0')
        self.assertEqual(lines[1], 'line 1')
        self.assertEqual(lines[2], 'line 2')
        self.assertEqual(lines[3], 'line 3')
        file.add_lines(['line 4'])
        fs.sync()

        # append to our file without explicitly reading it.
        fs = scan_filesystem(path=self.rootpath())
        file = fs.rootdirectory().find(['file'])
        file.add_lines(['line 5'])
        fs.sync()

        # see if there's still everything there.
        fs = scan_filesystem(path=self.rootpath())
        file = fs.rootdirectory().find(['file'])
        lines = file.lines()
        self.assertEqual(lines[0], 'line 0')
        self.assertEqual(lines[1], 'line 1')
        self.assertEqual(lines[2], 'line 2')
        self.assertEqual(lines[3], 'line 3')
        self.assertEqual(lines[4], 'line 4')
        self.assertEqual(lines[5], 'line 5')
        pass

    def test__sync_file_clear_on_sync_false(self):
        fs = FileSystem(path=self.rootpath())
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()
        self.assertFalse(file.raw_lines() is None)
        pass
        
    def test__sync_file_clear_on_sync_true(self):
        fs = FileSystem(path=self.rootpath(), flags=set([FileSystem.CLEAR_ON_SYNC]))
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()
        self.assertTrue(file.raw_lines() is None)
        pass

    def test__sync_file_truncate_persistent(self):

        fs = FileSystem(path=self.rootpath())
        file = File(lines=['line'])
        fs.rootdirectory().add(name='file', entry=file)
        fs.sync()

        fs = scan_filesystem(path=self.rootpath())
        file = fs.rootdirectory().find(['file'])
        file.truncate()
        fs.sync()

        fs = scan_filesystem(path=self.rootpath())
        file = fs.rootdirectory().find(['file'])
        self.assertTrue(file.lines() == [])
        pass

    def test__virtual_file(self):
        fs = FileSystem(path=self.rootpath())
        dir = fs.rootdirectory().add(
            name='dir',
            entry=Directory())
        file = dir.add(
            name='file',
            entry=File(state=FileState.VIRTUAL,
                       lines=['some token']))
        file.add_lines(['some other token'])
        
        fs.sync()

        self.assertFalse(os.path.exists(os.sep.join(file.abspath())))
        self.assertTrue(file.state() == FileState.VIRTUAL)
        self.assertFalse(file.raw_lines() is None)
        self.assertTrue(file.lines() == ['some token', 'some other token'])
        pass

    def test__sync_root_more_than_one_deep(self):
        # the above tests only test syncing an in-memory filesystem
        # whose root is only one directory apart from a physical
        # directory. here we test whether it work with two directory
        # entries in the air as well.

        fs = FileSystem(path=self.rootpath())
        fs.sync()
        self.assertTrue(os.path.isdir(os.sep.join(self.rootpath())))
        pass

    def test__explicit_mode(self):
        fs = FileSystem(path=self.rootpath())
        file_with_0755 = fs.rootdirectory().add(
            name='file_with_0755',
            entry=File(mode=0o755))
        fs.sync()

        self.assertTrue(os.path.isfile(os.sep.join(file_with_0755.abspath())))
        self.assertEqual(stat.S_IMODE(os.stat(os.sep.join(file_with_0755.abspath())).st_mode), 0o755)
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(BasicTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
