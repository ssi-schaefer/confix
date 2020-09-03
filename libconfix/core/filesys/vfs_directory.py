# Copyright (C) 2007-2010 Joerg Faschingbauer

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

from libconfix.core.utils.error import Error

class VFSDirectory(VFSEntry):
    """
    A directory node in the virtual filesystem game. As such it
    provides the necessary parent/child relations.

    Note that, for now, derived classes are required to use this
    implementation of these relations. It is not currently possible
    for derived classes to provide their own.
    """
    
    class AlreadyMounted(Error):
        def __init__(self, dir, name):
            Error.__init__(self, name+' has already been mounted in '+'/'.join(dir.abspath()))
            pass
        pass

    def __init__(self):
        self.__entry_by_name = {}
        self.__name_by_entry = {}
        pass

    def entries(self):
        """
        Return list of all the entries of a directory, as [(name,
        entry)].
        """
        return self.__entry_by_name.iteritems()

    def entryname(self, entry):
        """
        Return the name under which the given entry has been added.
        """
        return self.__name_by_entry[entry]

    def get(self, name):
        """
        Get a directory entry by name. Return None if not found.
        """
        return self.__entry_by_name.get(name)

    def add(self, name, entry):
        """
        Add a directory entry under the specified name. Returns the
        added entry (for convenience).
        """
        assert isinstance(entry, VFSEntry)
        assert entry.filesystem() is None or entry.filesystem() is self.filesystem()
        if self.__entry_by_name.has_key(name):
            raise self.AlreadyMounted(name=name, dir=self)
        self.__entry_by_name[name] = entry
        self.__name_by_entry[entry] = name
        entry.set_parent(self)
        if self.filesystem() is not None:
            entry.set_filesystem(self.filesystem())
            pass
        return entry # for convenience

    def remove_but_be_careful_no_sync(self, name):
        """
        Remove an entry from the directory's in-memory
        incarnation. Careful: the removal is not carried out
        physically when the directory is sync'ed; only the in-memory
        cache is manipulated.

        This is only useful scan.rescan_dir() when we bring the
        in-memory cache in sync with the on-disk entries some of which
        might have disappeared.
        """
        entry = self.__entry_by_name.get(name)
        assert entry is not None
        del self.__entry_by_name[name]
        del self.__name_by_entry[entry]
        pass

    def set_filesystem(self, filesystem):
        """
        Set my and my children's filesystem.
        """
        super(VFSDirectory, self).set_filesystem(filesystem)
        for name, entry in self.__entry_by_name.iteritems():
            entry.set_filesystem(filesystem)
            pass
        pass



    def find(self, path):
        """
        Starting at this object, find a descendant at path. If none is
        found, return None.
        """
        assert type(path) is list
        the_path = path[:]
        if len(the_path) == 0:
            return directory
        elem = self.get(the_path.pop(0))
        if elem is None:
            return None
        if len(the_path) == 0:
            return elem
        return elem.find(the_path)

    pass
