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
from .package import Package

import types

class InstalledPackage(Package):
    def get_marshalling_data(self):
        assert self.__name is not None
        return update_marshalling_data(
            marshalling_data=Package.get_marshalling_data(self),
            generating_class=InstalledPackage,
            attributes={'name': self.__name,
                        'version': self.__version,
                        'nodes': self.__nodes},
            version={'core.InstalledPackage': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['core.InstalledPackage']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.__name = data[Marshallable.ATTRIBUTES]['name']
        self.__version = data[Marshallable.ATTRIBUTES]['version']
        self.__nodes = data[Marshallable.ATTRIBUTES]['nodes']
        Package.set_marshalling_data(self, data)
        pass
    
    def __init__(self, name, version, nodes):
        Package.__init__(self)
        self.__name = name
        self.__version = version
        self.__nodes = nodes

        for n in self.__nodes:
            n.set_package(self)
            pass

        # <paranoia>
        assert type(name) is str
        assert type(version) is str
        # </paranoia>
        pass
    def name(self):
        return self.__name
    def version(self):
        return self.__version
    def nodes(self):
        return self.__nodes

    pass
