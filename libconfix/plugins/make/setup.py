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

from caller import MakeCaller

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.setup import Setup
from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor
from libconfix.core.utils.error import Error

class _MakeInterface_Confix2_dir(Confix2_dir_Contributor):
    class MakeCallerInterfaceProxy(InterfaceProxy):
        def __init__(self, object):
            InterfaceProxy.__init__(self, object)
            self.add_global('CALL_MAKE_AND_RESCAN', getattr(self, 'CALL_MAKE_AND_RESCAN'))
            # self.add_global('CALL_MAKE_AND_RESCAN_SYNC', getattr(self, 'CALL_MAKE_AND_RESCAN_SYNC'))
            pass
        def CALL_MAKE_AND_RESCAN(self, filename='Makefile', args=[]):
            """
            Create a builder object that calls make when it is
            enlarge()d. This means that make is called in a deferred
            way, not at the time the method is called.
            """
            self.object().add_call(filename=filename, args=args)
            pass
        pass

    def __init__(self, caller):
        Confix2_dir_Contributor.__init__(self)
        self.__caller = caller
        pass
    def get_iface_proxies(self):
        return [self.MakeCallerInterfaceProxy(object=self.__caller)]
    def locally_unique_id(self):
        return str(self.__class__)
    pass

class MakeSetup(Setup):
    def initial_builders(self):
        caller = MakeCaller()
        return super(MakeSetup, self).initial_builders() + \
               [caller, _MakeInterface_Confix2_dir(caller=caller)]
    pass
