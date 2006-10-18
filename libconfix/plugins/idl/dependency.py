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

from libconfix.core.utils import helper
from libconfix.core.require_string import Require_String
from libconfix.core.provide_string import Provide_String
from libconfix.core.repo.marshalling import \
     MarshalledVersionUnknownError, \
     Marshallable, \
     update_marshalling_data

class Require_IDL(Require_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Require_String.get_marshalling_data(self),
            generating_class=Require_IDL,
            attributes={},
            version={'Require_IDL': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require_IDL']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Require_String.set_marshalling_data(self, data)
        pass

    def __init__(self, filename, found_in, urgency):
        Require_String.__init__(
            self,
            string=helper.normalize_filename(filename),
            found_in=found_in,
            urgency=urgency)
        pass
    def __str__(self):
        ret = 'plugins.idl:#include<%s>' % self.string()
        if len(self.found_in_):
            ret = ret + ' (from ' + str([f for f in self.found_in()]) + ')'
        return ret
    pass

class Provide_IDL(Provide_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide_String.get_marshalling_data(self),
            generating_class=Provide_IDL,
            attributes={},
            version={'Provide_IDL': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_IDL']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide_String.set_marshalling_data(self, data)
        pass

    EXACT_MATCH = Provide_String.EXACT_MATCH
    PREFIX_MATCH = Provide_String.PREFIX_MATCH
    GLOB_MATCH = Provide_String.GLOB_MATCH

    MATCH_CLASSES = [Require_IDL]

    def __init__(self, filename, match=EXACT_MATCH):

        Provide_String.__init__(self,
                                string=helper.normalize_filename(filename),
                                match=match)

    def can_match_classes(self): return Provide_IDL.MATCH_CLASSES
    pass
