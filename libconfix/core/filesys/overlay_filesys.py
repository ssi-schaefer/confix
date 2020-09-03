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

from vfs_filesys import VFSFileSystem
from overlay_directory import OverlayDirectory

class OverlayFileSystem(VFSFileSystem):
    """
    Filesystem composed of an original and an overlay, which are again
    filesystem objects of type VFSFileSystem.

    All write (and sync()) access goes to the original filesystem.
    """
    def __init__(self, original, overlay):
        VFSFileSystem.__init__(self)

        assert original is not None
        assert overlay is not None

        self.__original = original
        self.__overlay = overlay

        self.__rootdirectory = OverlayDirectory(original=original.rootdirectory(),
                                                overlay=overlay.rootdirectory())
        self.__rootdirectory.set_filesystem(self)
        self.__rootdirectory.expand()
        pass
    
    def path(self):
        """
        (VFSFileSystem implementation.)
        """
        return self.__original.path()
    
    def rootdirectory(self):
        """
        (VFSFileSystem implementation.)
        """
        return self.__rootdirectory

    def sync(self):
        """
        (VFSFileSystem implementation.)
        """
        self.__original.sync()
        pass

    pass
