# $Id: modbuildprops.py,v 1.2 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2003 Salomon Automation

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

from core.error import Error

class BuildableModuleProperties:

    LIBNAME = 'LIBNAME'

    def __init__(self, properties=None):

        if properties is None:
            self.props_ = {}
        else:
            assert type(properties) is types.DictionaryType
            self.props_ = properties

    def keys(self):

        return self.props_.keys()

    def set(self, name, value):

        assert type(name) is types.StringType

        if value is None:
            raise Error("Value of module property '"+name+"' cannot be None")
            
        self.props_[name] = value

    def get(self, name):

        assert type(name) is types.StringType

        try:
            return self.props_[name]
        except KeyError:
            return None

    def update(self, other):

        assert isinstance(other, BuildableModuleProperties)
        self.props_.update(other.props_)

    def set_libname(self, n):

        assert len(name) != 0
        self.set(BuildableModuleProperties.LIBNAME, n)

    def get_libname(self):

        return self.get(BuildableModuleProperties.LIBNAME)

