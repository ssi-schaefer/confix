# Copyright (C) 2009 Joerg Faschingbauer

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

from libconfix.core.utils.error import Error, NativeError
from libconfix.core.filesys.vfs_file import VFSFile
from libconfix.core.filesys.vfs_directory import VFSDirectory

import types
import sys
import os

class CodePiece:
    def __init__(self, start_lineno, lines):
        self.start_lineno_ = start_lineno
        self.lines_ = lines
        pass
    def start_lineno(self):
        return self.start_lineno_
    def lines(self):
        return self.lines_
    pass

class InterfaceExecutor:
    def __init__(self, iface_pieces):
        self.__context = {}
        for piece in iface_pieces:
            for n, v in piece.get_globals().iteritems():
                assert type(n) is types.StringType
                assert not self.__context.has_key(n), n
                self.__context[n] = v
                pass
            pass
        pass

    def execute_file(self, file):
        assert isinstance(file, VFSFile), file
        assert file.parent() is not None
        assert isinstance(file.parent(), VFSDirectory)

        chdirbackto = None
            
        try:
            if file.is_persistent():
                dir_to_change_back_to = os.getcwd()
                
                # change to the directory that contains the file. note
                # that file.parent() is pointless in the days of union
                # filesystem.
                dir_to_change_to = os.path.dirname(os.sep.join(file.abspath()))
                os.chdir(dir_to_change_to)
                
                execfile(file.name(), self.__context)

                os.chdir(dir_to_change_back_to)
                return
            else:
                exec '\n'.join(file.lines()) in self.__context
                return
            pass
        except Exception, e:
            if chdirbackto is not None:
                os.chdir(chdirbackto)
                pass
            raise Error('Error executing '+'/'.join(file.abspath()), [NativeError(e, sys.exc_traceback)])
        pass

    def execute_pieces(self, pieces):
        for p in pieces:
            try:
                exec '\n'.join(p.lines()) in self.__context
            except Exception, e:
                raise Error('Error in code piece starting at line '+str(p.start_lineno())+' ('+p.lines()[0]+')',
                            [NativeError(e, sys.exc_traceback)])
            pass
        pass
    pass

class InterfaceProxy:
    def __init__(self):
        self.__globals = {}
        pass

    def add_global(self, key, value):
        if self.__globals.has_key(key):
            raise Error('"'+key+'" is already set')
        self.__globals[key] = value
        pass

    def get_globals(self):
        return self.__globals

    pass
