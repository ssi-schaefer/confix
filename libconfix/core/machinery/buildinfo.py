# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from repo import Marshallable
from repo import Unmarshallable

class BuildInformation(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: BuildInformation,
                Marshallable.VERSIONS: {'BuildInformation': 1},
                Marshallable.ATTRIBUTES: {}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInformation']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        pass
    
    def __init__(self): pass
    def install(self): assert 0, self.__class__

    def unique_key(self):
        
        """ Unique key to easily determine object equivalence. Used to
        index BuildInformation objects, and to eventually sort out
        duplicates. """

        assert 0, self.__class__

class BuildInformationSet(Unmarshallable):

    def __init__(self):
        self.__dict = {}
        pass

    def add(self, b):
        self.__dict[b.unique_key()] = b
        pass

    def merge(self, other):
        self.__dict.update(other.__dict)
        pass

    def __iter__(self):
        return self.__dict.itervalues()

    pass
