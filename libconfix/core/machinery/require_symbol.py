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

from require import Require
from require_string import Require_String

from libconfix.core.repo.marshalling import \
     Marshallable, \
     MarshalledVersionUnknownError, \
     update_marshalling_data

import types

class Require_Symbol(Require_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require_String.get_marshalling_data(self),
            generating_class=Require_Symbol,
            attributes={},
            version={'Require_Symbol': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require_Symbol']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Require_String.set_marshalling_data(self, data)

    def __init__(self,
                 symbol,
                 found_in,
                 urgency=Require.URGENCY_DEFAULT):
        assert type(found_in) in [types.ListType, types.TupleType]
        Require_String.__init__(
            self,
            string=symbol,
            found_in=found_in,
            urgency=urgency)
        pass

    def __str__(self):
        ret = str(self.__class__)+'('+self.string()+')'
        if len(self.found_in()):
            ret = ret + ' (from ' + str(self.found_in()) + ')'
        return ret

    def symbol(self):
        return self.string()
