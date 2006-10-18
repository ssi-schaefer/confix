# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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


from libconfix.core.repo.marshalling import Marshallable

class Package(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: Package,
                Marshallable.VERSIONS: {'Package': 1},
                Marshallable.ATTRIBUTES: {}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Package']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        pass
    
    def __init__(self):
        pass

    def name(self): assert 0, 'abstract'
    def version(self): assert 0, 'abstract'
    def nodes(self): assert 0, 'abstract'
    
    pass
