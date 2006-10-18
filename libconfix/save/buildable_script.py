# $Id: buildable_script.py,v 1.9 2006/03/26 19:12:46 jfasch Exp $

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

import os

from buildable_single import BuildableSingle
from provide_callable import Provide_Callable

class BuildableScript(BuildableSingle):

    def __init__(self,
                 dir,
                 filename,
                 lines):

        BuildableSingle.__init__(
            self,
            dir=dir,
            filename=filename,
            lines=lines)

        self.add_provide(Provide_Callable(exename=self.filename()))

    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def contribute_makefile_am(self, buildmod):

        BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

        buildmod.makefile_am().add_bin_script(self.filename())

