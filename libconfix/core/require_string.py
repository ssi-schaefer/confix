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

import types

from libconfix.core.repo.marshalling import Marshallable, update_marshalling_data

from require import Require

class Require_String(Require):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require.get_marshalling_data(self),
            generating_class=Require_String,
            attributes={'string': self.string_,
                        'found_in': [f for f in self.found_in_]},
            version={'Require_String': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require_String']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.string_ = data[Marshallable.ATTRIBUTES]['string']
        self.found_in_ = set(data[Marshallable.ATTRIBUTES]['found_in'])
        Require.set_marshalling_data(self, data)
        pass

    def __init__(self,
                 string,
                 found_in,
                 urgency=Require.URGENCY_DEFAULT):

        Require.__init__(self, urgency=urgency)

        self.string_ = string
        self.found_in_ = set()

        if type(found_in) is types.StringType:
            self.found_in_.add(found_in)
        elif type(found_in) in [types.ListType, types.TupleType] and len(found_in):
            self.found_in_ = set(found_in)
            pass            
        pass

    def update(self, r):
        if r.__class__ != self.__class__:
            return False

        if r.string_ != self.string_:
            return False

        # we have a match. add r's found_in to my list, and update the
        # urgency appropriately

        self.found_in_ |= r.found_in()
        if r.urgency() > self.urgency():
            self.set_urgency(r.urgency())
            pass

        return True

    def is_equal(self, other):
        return isinstance(other, self.__class__) and self.string_ == other.string_

    def string(self): return self.string_

    def found_in(self): return self.found_in_
