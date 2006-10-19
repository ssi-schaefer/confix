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


from directory import Directory

import os

class FileSystem:

    CLEAR_ON_SYNC = 0
    
    def __init__(self, path, rootdirectory=None, flags=None):
        self.path_ = path
        if rootdirectory is None:
            self.rootdirectory_ = Directory()
        else:
            self.rootdirectory_ = rootdirectory
            pass
        self.rootdirectory_.set_filesystem(self)

        if flags is None:
            self.flags_ = set()
        else:
            self.flags_ = flags
            pass
        
        pass

    def flags(self):
        return self.flags_
    
    def path(self):
        return self.path_

    def rootdirectory(self):
        return self.rootdirectory_

    def sync(self):
        # ensure that the directory containing the root directory exists.
        containing_dir = self.path_[0:-1]
        if len(containing_dir) > 0:
            path = os.sep.join(containing_dir)
            if os.path.exists(path):
                if not os.path.isdir(path):
                    raise Error('Directory "'+path+'" exists but is not a directory')
                pass
            else:
                try:
                    os.makedirs(path)
                except OSError, e:
                    raise Error('Could not create directory "'+path+'"', [e])
                pass
            pass

        # now finally, sync our rootdirectory
        self.rootdirectory_.sync()
        pass

    pass
