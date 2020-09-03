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

from vfs_directory import VFSDirectory
from vfs_file import VFSFile
from overlay_entry import OverlayEntry
from overlay_file import OverlayFile

from libconfix.core.utils.error import Error

import os

class OverlayDirectory(VFSDirectory, OverlayEntry):
    def __init__(self, original, overlay):
        VFSDirectory.__init__(self)
        OverlayEntry.__init__(self, original=original, overlay=overlay)

        # <paranoia>
        assert not (original is None and overlay is None)
        assert original is None or isinstance(original, VFSDirectory), original
        assert overlay is None or isinstance(overlay, VFSDirectory), overlay
        # </paranoia>

        pass

    def expand(self):
        """
        Creates child objects based on what original and overlay
        contain. Does this recursively until both trees are overlay'd.
        """
        # compose dictionary name -> [original, overlay] out of
        # original and overlay's direct descendants.
        compound_entries = {}
        if self.original() is not None:
            for name, entry in self.original().entries():
                compound_entries[name] = [entry, None]
                pass
            pass
        if self.overlay() is not None:
            for name, entry in self.overlay().entries():
                pair = compound_entries.setdefault(name, [None, None])
                pair[1] = entry
                pass
            pass

        # create entries, and recurse
        for name, pair in compound_entries.iteritems():
            original_entry = pair[0]
            overlay_entry = pair[1]
            assert not (original_entry is None and overlay_entry is None)
            compound_entry = None
            if \
                   original_entry is None and isinstance(overlay_entry, VFSDirectory) or \
                   isinstance(original_entry, VFSDirectory) and overlay_entry is None or \
                   isinstance(original_entry, VFSDirectory) and isinstance(overlay_entry, VFSDirectory):
                compound_entry = OverlayDirectory(original=original_entry, overlay=overlay_entry)
                pass
            elif \
                     original_entry is None and isinstance(overlay_entry, VFSFile) or \
                     isinstance(original_entry, VFSFile) and overlay_entry is None or \
                     isinstance(original_entry, VFSFile) and isinstance(overlay_entry, VFSFile):
                compound_entry = OverlayFile(original=original_entry, overlay=overlay_entry)
                pass

            compound_entry.expand()
            super(OverlayDirectory, self).add(name=name, entry=compound_entry)
            pass
                
        pass

    def add(self, name, entry):
        """
        Overloaded VFSDirectory method. Add the appropriate VFSEntry
        to VFSDirectory, and the argument entry to the original.

        Returns the compound entry, not the original.
        """

        if self.original() is None:
            raise self.OverlayAddError('Adding '+name+' to overlayed directory '+os.sep.join(self.abspath()))
        
        vfs_entry = None
        if isinstance(entry, VFSDirectory):
            vfs_entry = OverlayDirectory(original=entry, overlay=None)
        elif isinstance(entry, VFSFile):
            vfs_entry = OverlayFile(original=entry, overlay=None)
        else:
            assert False, type(entry)
            pass

        self.original().add(name=name, entry=entry)
        return super(OverlayDirectory, self).add(name=name, entry=vfs_entry)

    # this one is for tests that want to check for exactly this error.
    class OverlayAddError(Error): pass

    pass
