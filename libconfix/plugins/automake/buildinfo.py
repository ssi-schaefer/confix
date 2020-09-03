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

from libconfix.core.machinery.buildinfo import BuildInformation
from libconfix.core.utils import helper
from libconfix.core.machinery.repo import \
     update_marshalling_data, \
     Marshallable, \
     MarshalledVersionUnknownError

class BuildInfo_Configure_in(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Configure_in,
            attributes={'lines': self.__lines,
                        'order': self.__order,
                        'md5': self.__md5},
            version={'BuildInfo_Configure_in': 2})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Configure_in']
        if version == 1:
            self.__lines = data[Marshallable.ATTRIBUTES]['lines']
            self.__order = data[Marshallable.ATTRIBUTES]['order']
            self.__md5 = helper.md5_hexdigest_from_lines(self.__lines)
        elif version == 2:
            self.__lines = data[Marshallable.ATTRIBUTES]['lines']
            self.__order = data[Marshallable.ATTRIBUTES]['order']
            self.__md5 = data[Marshallable.ATTRIBUTES]['md5']
        else:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=2)
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, lines, order):
        BuildInformation.__init__(self)
        self.__lines = lines
        self.__order = order
        self.__md5 = helper.md5_hexdigest_from_lines(lines)
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + self.__md5
    def lines(self): return self.__lines
    def order(self): return self.__order
    def md5(self): return self.__md5

    def install(self): return self
    pass

class BuildInfo_ACInclude_m4(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_ACInclude_m4,
            attributes={'lines': self.__lines,
                        'md5': self.__md5},
            version={'BuildInfo_ACInclude_m4': 2})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_ACInclude_m4']
        if version == 1:
            self.__lines = data[Marshallable.ATTRIBUTES]['lines']
            self.__md5 = helper.md5_hexdigest_from_lines(self.__lines)
        elif version == 2:
            self.__lines = data[Marshallable.ATTRIBUTES]['lines']
            self.__md5 = data[Marshallable.ATTRIBUTES]['md5']
        else:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=2)
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, lines):
        BuildInformation.__init__(self)
        self.__lines = lines
        self.__md5 = helper.md5_hexdigest_from_lines(lines)
        pass
    def __str__(self): return self.unique_key()
    def unique_key(self):
        return self.__class__.__name__ + ':' + self.__md5
    def lines(self): return self.__lines
    def md5(self): return self.__md5

    def install(self): return self
    pass
