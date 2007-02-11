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

import os

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.filesys import scan
from libconfix.core.utils.error import Error
from libconfix.core.utils import external_cmd

class MakeCallerInterfaceProxy(InterfaceProxy):
    def __init__(self, caller):
        InterfaceProxy.__init__(self)
        self.__caller = caller
        self.add_global('CALL_MAKE_AND_RESCAN', getattr(self, 'CALL_MAKE_AND_RESCAN'))
        self.add_global('CALL_MAKE_AND_RESCAN_SYNC', getattr(self, 'CALL_MAKE_AND_RESCAN_SYNC'))
        pass
    def CALL_MAKE_AND_RESCAN(self, filename='Makefile', args=[]):
        """
        Create a builder object that calls make when it is
        enlarge()d. This means that make is called in a deferred way,
        not at the time the method is called.
        """
        self.__caller.add_call(filename=filename, args=args)
        pass
    def CALL_MAKE_AND_RESCAN_SYNC(self, filename='Makefile', args=[]):
        """
        Call make immediately, and rescan the directory. This is done
        synchronously, so that the caller can be sure that make has
        been called when the function returns.
        """
        cwd = self.__caller.parentbuilder().directory()
        
        external_cmd.exec_program(
            program='make',
            dir=cwd.abspath(),
            args=['-f', filename] + args)
        pass

        # make might have had side effects that we don't see
        scan.rescan_dir(cwd)
        
        pass
    pass
