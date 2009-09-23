# Copyright (C) 2009 Joerg Faschingbauer

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
from entrybuilder import EntryBuilder
from setup import Setup
from interface import InterfaceProxy

class IgnoreSetup(Setup):
    def setup(self, dirbuilder):
        revoker = EntryBuilderRevoker()
        dirbuilder.add_builder(revoker)
        dirbuilder.add_interface(IgnoreEntriesInterfaceProxy(revoker=revoker))
        pass
    pass

class EntryBuilderRevoker(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__pending_revoke = set()
        self.__done_revoke = set()
        pass

    def locally_unique_id(self):
        # I am supposed to be the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def ignore_entry(self, name):
        assert not name in self.__pending_revoke
        self.__pending_revoke.add(name)
        self.force_enlarge()
        pass

    def enlarge(self):
        revoke = []
        for builder in self.parentbuilder().iter_builders():
            if not isinstance(builder, EntryBuilder):
                continue
            if builder.entry().name() in self.__pending_revoke:
                revoke.append(builder)
                pass
            pass
        for builder in revoke:
            self.parentbuilder().remove_builder(builder)
            self.__pending_revoke.remove(builder.entry().name())
            self.__done_revoke.add(builder.entry().name())
            self.force_enlarge()
            pass
        pass
    pass

class IgnoreEntriesInterfaceProxy(InterfaceProxy):
    def __init__(self, revoker):
        InterfaceProxy.__init__(self)
        self.__revoker = revoker
        self.add_global('IGNORE_ENTRIES', getattr(self, 'IGNORE_ENTRIES'))
        self.add_global('IGNORE_FILE', getattr(self, 'IGNORE_FILE'))
        pass
    def IGNORE_ENTRIES(self, names):
        if type(names) not in (list, tuple):
            raise Error('IGNORE_ENTRIES() expects a list')
        for n in names:
            if type(n) is not str:
                raise Error('IGNORE_ENTRIES(): all list members must be strings')
            self.__revoker.ignore_entry(n)
            pass
        pass
    def IGNORE_FILE(self, name):
        if type(name) is not str:
            raise Error('IGNORE_FILE() expects a string')
        self.__revoker.ignore_entry(name)
        pass
    pass
