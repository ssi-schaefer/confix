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

from .repo import Marshallable

class Node(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: Node,
                Marshallable.VERSIONS: {'Node': 1},
                Marshallable.ATTRIBUTES: {}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Node']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        pass
    
    def __init__(self):
        pass

    def short_description(self):
        assert False, 'abstract'
        pass
    
    def provides(self):
        assert False, 'abstract'
        pass
    def requires(self):
        assert False, 'abstract'
        pass
    def iter_buildinfos(self):
        assert False, 'abstract'
        pass
    def iter_buildinfos_type(self, t):
        assert False, 'abstract'
        pass
    def iter_buildinfos_isinstance(self, t):
        assert False, 'abstract'
        pass
    pass
