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

from libconfix.core.repo.marshalling import Marshallable, MarshalledVersionUnknownError, update_marshalling_data
import libconfix.core.utils.debug

from provide_string import Provide_String
from require_symbol import Require_Symbol

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
