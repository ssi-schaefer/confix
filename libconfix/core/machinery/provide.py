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
from require import Require
from require import Require_Symbol
from require import Require_Callable

from libconfix.core.utils import debug

import fnmatch

class Provide(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: Provide,
                Marshallable.VERSIONS: {'Provide': 1},
                Marshallable.ATTRIBUTES: {}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        pass

    def __init__(self):
        pass
    def resolve(self, req):
        "Can self resolve the requirement?"
        debug.abstract("Provide::resolve()")
        pass
    def update(self, req):
        assert 0, 'abtract'
        return False

    pass

class Provide_String(Provide):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide.get_marshalling_data(self),
            generating_class=Provide_String,
            attributes={'string': self.string_,
                        'match': self.match_},
            version={'Provide_String': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_String']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.string_ = data[Marshallable.ATTRIBUTES]['string']
        self.match_ = data[Marshallable.ATTRIBUTES]['match']
        Provide.set_marshalling_data(self, data)
        pass
    
    EXACT_MATCH = 0
    PREFIX_MATCH = 1
    GLOB_MATCH = 2
    AUTO_MATCH = 3

    def __init__(self, string, match=EXACT_MATCH):
        assert match in [self.EXACT_MATCH,
                         self.PREFIX_MATCH,
                         self.GLOB_MATCH,
                         self.AUTO_MATCH]
        Provide.__init__(self)
        self.string_ = string
        if match == self.AUTO_MATCH:
            if ('*' in string) or ('?' in string) or ('[' in string) or (']' in string):
                self.match_ = self.GLOB_MATCH
            else:
                self.match_ = self.EXACT_MATCH
                pass
            pass
        else:
            self.match_ = match
            pass
        pass
    def string(self):
        return self.string_
    def match(self):
        return self.match_

    def resolve(self, req):
        assert isinstance(req, Require), \
               "Provide_CInclude::resolve(): not even a Require"
        
        for c in self.can_match_classes():
            if c is req.__class__:
                break
            pass
        else:
            return False

        if self.match_ == Provide_String.EXACT_MATCH:
            return req.string_ == self.string_
        if self.match_ == Provide_String.PREFIX_MATCH:
            return req.string_.startswith(self.string_)
        if self.match_ == Provide_String.GLOB_MATCH:
            return fnmatch.fnmatchcase(req.string(), self.string_)
        assert False
        pass

    def update(self, other):
        return isinstance(other, self. __class__) and self.string_ == other.string_

    def is_equal(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.string_ == other.string_ and self.match_ == other.match_

    def can_match_classes(self):
        assert 0
        pass

    pass

class Provide_Symbol(Provide_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide_String.get_marshalling_data(self),
            generating_class=Provide_Symbol,
            attributes={},
            version={'Provide_Symbol': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_Symbol']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide_String.set_marshalling_data(self, data)
        pass

    MATCH_CLASSES = [Require_Symbol]

    def __init__(self, symbol, match=Provide_String.EXACT_MATCH):
        Provide_String.__init__(
            self,
            string=symbol,
            match=match)
        pass
    def __str__(self):
        return str(self.__class__)+'('+self.symbol()+')'
    def symbol(self):
        return self.string()
    def can_match_classes(self):
        return Provide_Symbol.MATCH_CLASSES

    pass

class Provide_Callable(Provide_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide_String.get_marshalling_data(self),
            generating_class=Provide_Callable,
            attributes={},
            version={'Provide_Callable': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_Callable']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide_String.set_marshalling_data(self, data)
        pass


    MATCH_CLASSES = [Require_Callable]

    def __init__(self, exename):
        
        Provide_String.__init__(
            self,
            string=exename,
            match=Provide_String.EXACT_MATCH)

    def __repr__(self): return self.__class__.__name__ + ':' + self.string()

    def can_match_classes(self): return Provide_Callable.MATCH_CLASSES

    pass
