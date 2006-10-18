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

import sys, os

from libconfix.core.utils.error import Error

from filesys import FileSystem
from directory import Directory, DirectoryState
from file import File, FileState

def scan_filesystem(path):
    return FileSystem(path=path, rootdirectory=scan_dir(path))
    
def scan_dir(path):
    ret = Directory(state=DirectoryState.SYNC)
    for entry in os.listdir(os.sep.join(path)):
        if entry == '.' or entry == '..':
            continue
        next_path = path + [entry]
        next_path_str = os.sep.join(next_path)
        if os.path.isfile(next_path_str):
            ret.add(name=entry, entry=File(state=FileState.SYNC_CLEAR))
            continue
        if os.path.isdir(next_path_str):
            dir = scan_dir(next_path)
            ret.add(entry, dir)
            continue
        raise Error(next_path_str+' has unknown type')
    return ret

def print_filesys(fs, indent):
    print ' '*indent + os.sep.join(fs.path())
    print_dir_contents(fs.rootdirectory(), indent+2)
    pass

def print_dir_contents(dir, indent):
    for name, entry in dir.entries():
        if isinstance(entry, Directory):
            print ' '*indent + name + '/'
            print_dir_contents(entry, indent+2)
        elif isinstance(entry, File):
            print ' '*indent + name
            pass
        pass
    pass

def build_inmem_filesys():
    fs = FileSystem(path=['', 'tmp', 'test-the-filesystem'],
                    rootdirectory=Directory())
    fs.rootdirectory().add(name='Confix2.in',
                           entry=File(lines=['PACKAGE_NAME("basic")',
                                             'PACKAGE_VERSION("6.6.6")']))

    dir1 = Directory()
    dir1.add(name='Confix2.in', entry=File(lines=['IGNORE_ENTRIES(["file1_1.h", "file1_1.c"])']))
    dir1.add(name='file1_1.h', entry=File(lines=[]))
    dir1.add(name='file1_1.c', entry=File(lines=[]))
    dir1.add(name='file1_2.h', entry=File(lines=[]))
    dir1.add(name='file1_2.c', entry=File(lines=[]))
    
    dir2 = Directory()
    dir2.add(name='file2_1.h', entry=File(lines=[]))
    dir2.add(name='file2_1.c', entry=File(lines=[]))
    
    dir1.add(name='dir2', entry=dir2)
    fs.rootdirectory().add(name='dir1', entry=dir1)
    
    return fs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fs = scan_filesystem(sys.argv[1].split(os.sep))
    else:
        fs = build_inmem_filesys()
        pass

    print_filesys(fs, 0)
