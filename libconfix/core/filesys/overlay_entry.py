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

from vfs_entry import VFSEntry

class OverlayEntry(VFSEntry):
    def __init__(self, original, overlay):
        VFSEntry.__init__(self)

        # <paranoia>
        assert not (original is None and overlay is None)
        assert original is None or isinstance(original, VFSEntry), original
        assert overlay is None or isinstance(overlay, VFSEntry), overlay
        # </paranoia>

        self.__original = original
        self.__overlay = overlay
        pass

    def original(self):
        return self.__original

    def overlay(self):
        return self.__overlay
    
    def expand(self):
        """
        Abstract. Supposed to actually "merge" original and overlay.
        """
        assert False, "abstract"
        pass

    def abspath(self):
        """
        (VFSEntry implementation)
        """
        if self.__original is not None:
            return self.__original.abspath()
        return self.__overlay.abspath()

    def relpath(self, from_dir):
        """
        (VFSEntry implementation)
        """
        if self.__original is not None:
            return self.__original.relpath(from_dir=from_dir)
        return self.__overlay.relpath(from_dir=from_dir)
    
    pass
