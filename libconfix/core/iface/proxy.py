# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.utils.error import Error

class InterfaceProxy:
    def __init__(self, object):
        self.__object = object
        self.__globals = {}
        pass

    def object(self):
        return self.__object

    def add_global(self, key, value):
        if self.__globals.has_key(key):
            raise Error('"'+key+'" is already set')
        self.__globals[key] = value
        pass

    def get_globals(self):
        return self.__globals

    pass
