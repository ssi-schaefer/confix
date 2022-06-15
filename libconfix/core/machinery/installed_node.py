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

from .repo import Marshallable, update_marshalling_data
from .node import Node

import types

class InstalledNode(Node):
    def get_marshalling_data(self):
        assert self.__package is not None
        assert type(self.__name) is list
        assert type(self.__provides) is list
        assert type(self.__requires) is list
        assert type(self.__buildinfos) is list
        return update_marshalling_data(
            marshalling_data=Node.get_marshalling_data(self),
            generating_class=InstalledNode,
            attributes={'package': self.__package,
                        'name': self.__name,
                        'provides': self.__provides,
                        'requires': self.__requires,
                        'buildinfos': self.__buildinfos},
            version={'InstalledNode': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['InstalledNode']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__package = data[Marshallable.ATTRIBUTES]['package']
        self.__name = data[Marshallable.ATTRIBUTES]['name']
        self.__provides = data[Marshallable.ATTRIBUTES]['provides']
        self.__requires = data[Marshallable.ATTRIBUTES]['requires']
        self.__buildinfos = data[Marshallable.ATTRIBUTES]['buildinfos']
        assert type(self.__provides) is list
        assert type(self.__requires) is list
        assert type(self.__buildinfos) is list
        Node.set_marshalling_data(self, data)

        self.__type_cache = {}
        self.__isinstance_cache = {}
        pass
    
    def __init__(self, name, provides, requires, buildinfos):
        assert type(name) is list
        self.__package = None
        self.__name = name
        self.__provides = provides
        self.__requires = requires
        self.__buildinfos = buildinfos

        self.__type_cache = {}
        self.__isinstance_cache = {}
        pass
    def __str__(self):
        return '.'.join([self.__package.name()]+self.__name)
    def short_description(self):
        return '.'.join([self.__package.name()]+self.__name)
    def set_package(self, package):
        self.__package = package
        pass
    def package(self):
        return self.__package
    def name(self):
        return self.__name
    def provides(self):
        return self.__provides
    def requires(self):
        return self.__requires
    def iter_buildinfos(self):
        return iter(self.__buildinfos)

    def iter_buildinfos_type(self, t):
        ret = self.__type_cache.get(t)
        if ret is not None:
            return ret
        ret = []
        self.__type_cache[t] = ret
        for b in self.__buildinfos:
            if type(b) is t:
                ret.append(b)
                pass
            pass
        return ret

    def iter_buildinfos_isinstance(self, t):
        ret = self.__isinstance_cache.get(t)
        if ret is not None:
            return ret
        ret = []
        self.__isinstance_cache[t] = ret
        for b in self.__buildinfos:
            if isinstance(b, t):
                ret.append(b)
                pass
            pass
        return ret
    pass
