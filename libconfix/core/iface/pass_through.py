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

from libconfix.core.machinery.builder import Builder

class MethodPassThrough(Builder):
    """
    A special kind of Builder that has no responsibility of its
    own. It is supposed to be used by interface proxies that want to
    talk to a DirectoryBuilder (you know, they cannot do so directly).
    """

    def __init__(self, id):
        """
        The id argument is used to make a suitable builder ID of it.
        """
        Builder.__init__(self)
        self.__id = str(self.__class__)+':'+id
        pass
    
    def locally_unique_id(self):
        return self.__id
    
    pass
