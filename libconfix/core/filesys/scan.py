# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2010 Joerg Faschingbauer

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

from .filesys import FileSystem
from .directory import Directory, DirectoryState
from .file import File, FileState

def scan_filesystem(path):
    assert type(path) is list
    return FileSystem(path=path, rootdirectory=scan_dir(path))
    
def scan_dir(path):
    ret = Directory(state=DirectoryState.SYNC)
    for entry in os.listdir(os.sep.join(path)):
        if entry in ['.', '..']:
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

def rescan_dir(dir):
    if dir.state() != DirectoryState.SYNC:
        raise Error('Cannot rescan directory: not yet in sync')
    abspath = os.sep.join(dir.abspath())

    physical_dir_entries = set(os.listdir(abspath))

    # first pass: add entries that are new in the physical directory.
    for name in physical_dir_entries:
        if name in ['.', '..']:
            continue
        absname = os.path.join(abspath, name)
        existing_entry = dir.get(name)
        if existing_entry is not None:
            if os.path.isfile(absname):
                if not isinstance(existing_entry, File):
                    # entry type change; bail out
                    raise Error('Cannot convert existing entry '+name+' to a file')
                pass
            elif os.path.isdir(absname):
                if not isinstance(existing_entry, Directory):
                    # entry type change; bail out
                    raise Error('Cannot convert existing entry '+name+' to a directory')
                # descend rescanning into subdirectory.
                rescan_dir(existing_entry)
                pass
            else:
                raise Error(absname+' has unknown type')
            pass
        else:
            # go add the new entry
            if os.path.isfile(absname):
                dir.add(name=name, entry=File(state=FileState.SYNC_CLEAR))
            elif os.path.isdir(absname):
                dir.add(name=name, entry=scan_dir(dir.abspath()+[name]))
            else:
                raise Error(absname+' has unknown type')
            pass
        pass

    # second pass: remove entries that have disappeared from the
    # physical directory. (first iterate, then remove)
    remove_names = []
    for name, entry in dir.entries():
        if not entry.is_persistent():
            # the file has been added up in the air for the purpose of
            # persisting it later.
            continue
        if name in physical_dir_entries:
            continue
        remove_names.append(name)
        pass
    for name in remove_names:
        dir.remove_but_be_careful_no_sync(name)
        pass
    pass

def print_filesys(fs, indent):
    print(' '*indent + os.sep.join(fs.path()))
    print_dir_contents(fs.rootdirectory(), indent+2)
    pass

def print_dir_contents(dir, indent):
    for name, entry in dir.entries():
        if isinstance(entry, Directory):
            print(' '*indent + name + '/')
            print_dir_contents(entry, indent+2)
        elif isinstance(entry, File):
            print(' '*indent + name)
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
