# Copyright (C) 2008-2009 Joerg Faschingbauer

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

from builder import Builder
from setup import Setup
from interface import InterfaceProxy

import types

class CreatorSetup(Setup):
    def setup(self, dirbuilder):
        creator_slave = CreatorSlave();
        dirbuilder.add_builder(creator_slave)
        dirbuilder.add_interface(CreatorSlave.IgnoreEntriesInterfaceProxy(slave=creator_slave))
        pass
    pass

class Creator(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__candidate_builders = {}
        self.__slave = None
        pass

    def initialize(self, package):
        """
        Places a creator-slave object into the parent directory.
        """
        super(Creator, self).initialize(package)
        # add slave to parent if we don't have one yet
        if self.__slave is None:
            for b in self.parentbuilder().iter_builders():
                if isinstance(b, CreatorSlave):
                    self.__slave = b
                    break
                pass
            else:
                self.__slave = CreatorSlave()
                self.parentbuilder().add_builder(self.__slave)
                pass
            pass
        pass

    def add_candidate_builder(self, name, builder):
        """
        Called by derived classes when they have discovered a new
        builder.
        """
        self.__slave.add_candidate_builder(name, builder)
        pass        

    pass

class CreatorSlave(Builder):
    def __init__(self):
        Builder.__init__(self)
        # dictionary entry-name -> builder
        self.__added_builders = {}
        # set of entry names to ignore
        self.__ignored_entries = set()
        pass

    def locally_unique_id(self):
        # I am supposed to be the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def add_candidate_builder(self, name, builder):
        if name in self.__ignored_entries:
            return
        existing = self.__added_builders.get(name)
        if existing:
            raise Error('Multiple builders for one entry: '+str(existing)+' and '+str(builder))
        self.__added_builders[name] = builder
        self.parentbuilder().add_builder(builder)
        pass

    def ignore_entry(self, name):
        """
        Called by the interface functions that I contribute to
        Confix2.dir.
        """
        assert type(name) is str
        self.__ignored_entries.add(name)
        revoke_builder = self.__added_builders.get(name)
        if revoke_builder is not None:
            self.parentbuilder().remove_builder(revoke_builder)
            pass
        pass

    class IgnoreEntriesInterfaceProxy(InterfaceProxy):
        def __init__(self, slave):
            InterfaceProxy.__init__(self)
            self.__slave = slave
            self.add_global('IGNORE_ENTRIES', getattr(self, 'IGNORE_ENTRIES'))
            self.add_global('IGNORE_FILE', getattr(self, 'IGNORE_FILE'))
            pass
        def IGNORE_ENTRIES(self, names):
            if type(names) not in [types.ListType, types.TupleType]:
                raise Error('IGNORE_ENTRIES() expects a list')
            for n in names:
                if type(n) is not str:
                    raise Error('IGNORE_ENTRIES(): all list members must be strings')
                self.__slave.ignore_entry(n)
                pass
            pass
        def IGNORE_FILE(self, name):
            if type(name) is not types.StringType:
                raise Error('IGNORE_FILE() expects a string')
            self.__slave.ignore_entry(name)
            pass
        pass

    pass
