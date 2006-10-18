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

from entry import DirectoryEntry

from libconfix.core.utils.error import Error, NativeError

import os, types, sys

class DirectoryState:
    INMEMORY = 0
    SYNC = 1
    pass

class Directory(DirectoryEntry):
    class AlreadyMounted(Error):
        def __init__(self, dir, name):
            Error.__init__(self, name+' has already been mounted in '+'/'.join(dir.abspath()))
            pass
        pass
    
    def __init__(self, mode=None, state=DirectoryState.INMEMORY):
        DirectoryEntry.__init__(self, mode=mode)
        self.state_ = state
        self.entry_by_name_ = {}
        self.name_by_entry_ = {}
        pass

    def state(self):
        return self.state_

    def entries(self):
        return self.entry_by_name_.iteritems()

    def get(self, name):
        return self.entry_by_name_.get(name)

    def find(self, path):
        assert type(path) is types.ListType
        list = path[:]
        if len(list) == 0:
            return self
        elem = self.get(list.pop(0))
        if elem is None:
            return None
        if len(list) == 0:
            return elem
        return elem.find(list)
        
    def has(self, name):
        return self.entry_by_name_.has_key(name)

    def add(self, name, entry):
        assert isinstance(entry, DirectoryEntry)
        assert entry.filesystem() is None or entry.filesystem() is self.filesystem()
        if self.entry_by_name_.has_key(name):
            raise Directory.AlreadyMounted(name=name, dir=self)
        self.entry_by_name_[name] = entry
        self.name_by_entry_[entry] = name
        entry.set_parent(self)
        if self.filesystem_ is not None:
            entry.set_filesystem(self.filesystem())
            pass
        return entry # for convenience

    def set_filesystem(self, filesystem):
        assert filesystem is not None
        assert self.filesystem_ is None
        self.filesystem_ = filesystem
        for name, entry in self.entry_by_name_.iteritems():
            entry.set_filesystem(filesystem)
            pass
        pass

    def entryname(self, entry):
        return self.name_by_entry_[entry]

    def sync(self):
        if self.state_ == DirectoryState.SYNC:
            pass
        elif self.state_ == DirectoryState.INMEMORY:
            try:
                path = os.sep.join(self.abspath())
                if self.mode() is None:
                    os.mkdir(path)
                else:
                    os.mkdir(path, self.mode())
                    pass
                self.state_ = DirectoryState.SYNC
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
    
    pass
