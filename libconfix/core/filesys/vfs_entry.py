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

class VFSEntry(object):
    """
    A directory entry a virtual file system.

    This class is meant to be the base class for every object - file
    or directory - in the game. As such, it provides the following
    relations:

    - parent; a back-reference to the entry's parent object, which is
      supposed to be of type VFSDirectory (actually, a derived
      instance).

    - filesystem; a reference to the filesystem that owns this node.

    The class also implements so-called properties. These are
    name/value pairs, where name is a string, and value can be any
    type.
    """
    def __init__(self):
        self.__properties = {}
        self.__parent = None
        self.__filesystem = None
        pass

    def abspath(self):
        """
        Return the absolute path to this object.
        """
        assert 0, 'abstract'
        pass

    def relpath(self, from_dir):
        """
        Return the relative path from dir to this object.
        """
        assert 0, 'abstract'
        pass

    def sync(self):
        """
        Write back to the backing storage, whatever this means. To be
        implemented by derived classes.
        """
        assert 0, 'abstract'
        pass

    def is_persistent(self):
        """
        Does this entry correspond to a physical OS file system entry
        that can be accessed directly?

        This information is quite useful under certain circumstances;
        for example when it is better to pass the file to python's
        execfile(), rather than exec'ing it from memory (execfile()
        gives better error messages).
        """
        assert 0, 'abstract'
        pass

    def parent(self):
        return self.__parent

    def set_parent(self, parent):
        assert self.__parent is None
        self.__parent = parent
        pass

    def filesystem(self):
        return self.__filesystem

    def set_filesystem(self, filesystem):
        assert filesystem is not None
        assert self.__filesystem is None
        self.__filesystem = filesystem
        pass

    def name(self):
        assert self.__parent is not None, 'not yet mounted'
        return self.__parent.entryname(self)

    def set_property(self, name, value):
        self.__properties[name] = value
        pass

    def get_property(self, name):
        return self.__properties.get(name)

    def del_property(self, name):
        del self.__properties[name]
        pass

