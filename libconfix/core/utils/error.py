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

import sys
import traceback

class Error(Exception):

    def __init__(self, msg, list=[]):
        self.__message = msg
        self.__list = list[:]
        pass

    def __str__(self):
        list = self.format_list()
        return '\n'.join(list)

    def errors(self):
        return self.__list

    def add(self, e):
        self.__list.append(e)

    def format_list(self, offset=0):
        ret = [' ' * offset + self.__message]
        for e in self.__list:
            if isinstance(e, Error):
                ret.extend(e.format_list(offset+2))
            elif isinstance(e, NativeError):
                ret.extend(self.format_standard_exception(e.exception(), e.traceback(), offset+2))
            else:
                ret.extend(self.format_standard_exception(e, sys.exc_info()[2], offset+2))
                pass
            pass
        return ret

    def format_standard_exception(self, e, tb, offset):
        exc_list = traceback.format_exception(e.__class__, e, tb)
        lines = []
        for l in exc_list:
            if len(l):
                lines.append(' '*offset + '|' + l.replace('\n', ''))
                pass
            pass
        return lines

    def contains_error_of_type(self, t):
        """ Do I contain a nested error of type t?
        
        This is true when I am of type t, or when I contain an error
        of type t. """

        if isinstance(self, t):
            return True
        for e in self.__list:
            if e.contains_error_of_type(t):
                return True
            pass
        return False

    pass

class NativeError(Exception):

    def __init__(self, exception, traceback):
        self.exception_ = exception
        self.traceback_ = traceback

    def exception(self): return self.exception_
    def traceback(self): return self.traceback_
