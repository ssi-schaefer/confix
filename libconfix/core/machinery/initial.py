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

class InitialBuilders:
    """ A simple container for builders, along with interface proxies
    that operate upon them."""

    def __init__(self):
        self.__builders = []
        self.__iface_proxies = []
        pass

    def builders(self):
        return self.__builders
    def add_builder(self, b):
        self.__builders.append(b)
        pass

    def iface_proxies(self):
        return self.__iface_proxies
    def add_iface_proxy(self, p):
        self.__iface_proxies.append(p)
        pass

    def add(self, rhs):
        """ Add the InitialBuilders rhs to my own stuff."""
        self.__builders.extend(rhs.__builders)
        self.__iface_proxies.extend(rhs.__iface_proxies)
        pass

    pass
