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

from vfs_file import VFSFile
from overlay_entry import OverlayEntry

from libconfix.core.utils.error import Error

import os

class OverlayFile(VFSFile, OverlayEntry):
    def __init__(self, original, overlay):
        VFSFile.__init__(self)
        OverlayEntry.__init__(self, original=original, overlay=overlay)

        # <paranoia>
        assert not (original is None and overlay is None)
        assert original is None or isinstance(original, VFSFile), original
        assert overlay is None or isinstance(overlay, VFSFile), overlay
        # </paranoia>

        pass

    def is_persistent(self):
        """
        (VFSEntry implementation)
        """
        if self.original() is not None:
            return self.original().is_persistent()
        return self.overlay().is_persistent()

    def lines(self):
        """
        (VFSFile implementation)
        """
        if self.original() is not None:
            return self.original().lines()
        return self.overlay().lines()

    def add_lines(self, lines):
        """
        (VFSFile implementation)
        """
        if self.original() is not None:
            return self.original().add_lines(lines)
        raise self.AddLinesError('Adding lines to overlayed (read-only) file')

    def truncate(self):
        """
        (VFSFile implementation)
        """
        if self.original() is not None:
            return self.original().truncate()
        raise self.TruncateError('Truncating overlayed (read-only) file')

    def is_overlayed(self):
        """
        (VFSFile implementation)
        """
        if self.original() is not None:
            return self.original().is_overlayed()
        return True

    def expand(self):
        if self.original() is not None and self.overlay() is not None:
            raise Error('Conflicting file entries: '+\
                        os.sep.join(self.original().abspath())+' and '+\
                        os.sep.join(self.overlay().abspath()))
        pass

    # needed for unit tests: we check for the exact error condition
    # rather than for the anonymous Error
    class TruncateError(Error): pass
    class AddLinesError(Error): pass

    pass
