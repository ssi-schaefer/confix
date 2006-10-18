# $Id: buildable_composite.py,v 1.17 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import core.debug
from buildable import Buildable

class BuildableComposite(Buildable):

    """ Manages building something from multiple source files. """
    
    def __init__(self,
                 name,
                 dir):

        Buildable.__init__(self,
                           name=name,
                           dir=dir)

        self.members_ = []

    def members(self):
        return self.members_

    def add_member(self, b):

        """ Add a buildable which is going to be a member of
        myself. For example, an archive of object files will receive
        as members the buildables which will build themselves into
        object files. """

        assert isinstance(b, Buildable)

        for m in self.members_:
            if m.name() == b.name():
                assert 0, self.name() + ": add_member(): already have " + m.name()

        self.members_.append(b)
