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

from libconfix.core.utils.error import Error

class BuilderSet:

    class DuplicateBuilderError(Error):
        def __init__(self, existing_builder, new_builder):
            Error.__init__(self, msg='Duplicate builder: existing "'+str(existing_builder)+'", new "'+str(new_builder)+'"')
            pass
        pass
    
    def __init__(self):
        self.__builders = {}
        pass

    def iter_builders(self):
        return self.__builders.itervalues()

    def add_builder(self, b):
        id = b.locally_unique_id()
        existing_builder = self.__builders.get(id)
        if existing_builder is not None:
            raise BuilderSet.DuplicateBuilderError(existing_builder=existing_builder, new_builder=b)
        self.__builders[id] = b
        pass

    def remove_builder(self, b):
        id = b.locally_unique_id()
        assert id in self.__builders
        del self.__builders[id]
        pass
        
    pass
