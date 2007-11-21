# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from vfs_directory import VFSDirectory
from entry import Entry

from libconfix.core.utils.error import NativeError

import os, types, sys

class DirectoryState(object):
    INMEMORY = 0
    SYNC = 1
    pass

class Directory(VFSDirectory, Entry):
    def __init__(self, mode=None, state=DirectoryState.INMEMORY):
        VFSDirectory.__init__(self)
        Entry.__init__(self, mode=mode)
        self.__state = state
        pass

    def is_persistent(self):
        """
        (VFSEntry implementation)
        """
        return self.__state == DirectoryState.SYNC

    def sync(self):
        """
        (VFSEntry implementation)
        """
        if self.__state == DirectoryState.SYNC:
            pass
        elif self.__state == DirectoryState.INMEMORY:
            try:
                path = os.sep.join(self.abspath())
                if self.mode() is None:
                    os.mkdir(path)
                else:
                    os.mkdir(path, self.mode())
                    pass
                self.__state = DirectoryState.SYNC
                pass
            except OSError, err:
                raise Error('Could not create directory '+path, [NativeError(err, sys.exc_traceback)])
            pass
        else:
            assert 0
            pass

        # recursively sync child entries
        child_errors = []
        for name, entry in self.entries():
            try:
                entry.sync()
                pass
            except Error, err:
                child_errors.append(err)
                pass
            pass
        if len(child_errors):
            raise Error('Could not sync child nodes of directory '+path, child_errors)
        pass

    def state(self):
        return self.__state

    pass
