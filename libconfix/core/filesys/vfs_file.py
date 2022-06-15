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

from .vfs_entry import VFSEntry

class VFSFile(VFSEntry):
    """
    A file in the virtual filesystem game.
    """

    def lines(self):
        """
        Return the lines of the file, with newlines removed.
        """
        assert False, "abstract"
        pass

    def add_lines(self, lines):
        """
        Add lines to the file. The lines are strings, newlines will be
        added.
        """
        assert False, "abstract"
        pass
    
    def truncate(self):
        """
        Truncate the file.
        """
        assert False, "abstract"
        pass

    def is_overlayed(self):
        """
        Does the file come from an overlay?
        
        Sadly, I have to burden the interface with that - at least as
        long as something better comes to mind. Fact is that we need
        to know that when we generate input for the backend build
        tool.
        """
        assert False, "abstract"
        pass
    
    pass
