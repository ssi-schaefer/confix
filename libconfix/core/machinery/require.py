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
from repo import MarshalledVersionUnknownError
from repo import update_marshalling_data

from libconfix.core.utils.error import Error
from libconfix.core.utils import debug

import types

class Require(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: Require,
                Marshallable.VERSIONS: {'Require': 1},
                Marshallable.ATTRIBUTES: {'urgency': self.urgency_}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.urgency_ = data[Marshallable.ATTRIBUTES]['urgency']
        pass

    # it is no accident that these are sorted by urgency level

    URGENCY_IGNORE = URGENCY_DEFAULT = URGENCY_DONTCARE = 0
    URGENCY_WARN = 1
    URGENCY_ERROR = 2

    def __init__(self, urgency=URGENCY_DEFAULT):
        self.urgency_ = urgency
        pass
    def id(self):
        assert 0, 'remove that'
        return self.id_
    def urgency(self):
        return self.urgency_
    def set_urgency(self, u):
        self.urgency_ = u

    def update(self, r):

        """ When multiple equivalent Require objects are added to the
        same module, this adds unnecessary (and sometimes
        considerable) overhead to the resolving process. This method
        is an attempt to collapse r with self.

        @rtype: boolean

        @return: A boolean that indicates whether the objects could be
        collapsed.

        """

        debug.abstract('Require.update()')
        pass

    pass

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

    pass

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

    pass

class Require_Callable(Require_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require_String.get_marshalling_data(self),
            generating_class=Require_Callable,
            attributes={},
            version={'Require_Callable': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require_Callable']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Require_String.set_marshalling_data(self, data)
        pass

    def __init__(self, exename, found_in, urgency):
        Require_String.__init__(
            self,
            string=exename,
            found_in=found_in,
            urgency=urgency)
        pass

    def __str__(self):
        return str(self.__class__)+':'+self.string()

    pass
