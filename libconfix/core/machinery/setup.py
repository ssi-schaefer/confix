# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

class Setup(object):
    def setup(self, dirbuilder):
        assert False, 'abstract: '+str(self)
        pass
    pass

class CompositeSetup(Setup):
    def __init__(self, setups):
        Setup.__init__(self)
        self.__setups = setups
        pass
    def add_setup(self, s):
        self.__setups.append(s)
        pass
    def __iter__(self):
        for s in self.__setups:
            if isinstance(s, CompositeSetup):
                for s_next in s:
                    yield s_next
                    pass
                pass
            else:
                yield s
                pass
            pass
        pass
                
    def setup(self, dirbuilder):
        for s in self.__setups:
            s.setup(dirbuilder)
            pass
        pass
    pass
