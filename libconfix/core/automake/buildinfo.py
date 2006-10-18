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

from libconfix.core.buildinfo import BuildInformation
from libconfix.core.utils.helper import md5_hexdigest_from_lines
from libconfix.core.repo.marshalling import \
     update_marshalling_data, \
     Marshallable, \
     MarshalledVersionUnknownError

class BuildInfo_Configure_in(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_Configure_in,
            attributes={'lines': self.lines_,
                        'order': self.order_},
            version={'BuildInfo_Configure_in': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_Configure_in']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.lines_ = data[Marshallable.ATTRIBUTES]['lines']
        self.order_ = data[Marshallable.ATTRIBUTES]['order']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, lines, order):
        BuildInformation.__init__(self)
        self.lines_ = lines
        self.order_ = order
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + md5_hexdigest_from_lines(self.lines_)
    def lines(self): return self.lines_
    def order(self): return self.order_

    def install(self): return self
    pass

class BuildInfo_ACInclude_m4(BuildInformation):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=BuildInformation.get_marshalling_data(self),
            generating_class=BuildInfo_ACInclude_m4,
            attributes={'lines': self.lines_},
            version={'BuildInfo_ACInclude_m4': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['BuildInfo_ACInclude_m4']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.lines_ = data[Marshallable.ATTRIBUTES]['lines']
        BuildInformation.set_marshalling_data(self, data)
        pass

    def __init__(self, lines):
        BuildInformation.__init__(self)
        self.lines_ = lines
        pass
    def unique_key(self):
        return self.__class__.__name__ + ':' + md5_hexdigest_from_lines(self.lines_)
    def lines(self): return self.lines_

    def install(self): return self
    pass
