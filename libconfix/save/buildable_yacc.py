# $Id: buildable_yacc.py,v 1.27 2006/03/22 15:03:54 jfasch Exp $

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

import os

import core.debug
import core.helper
import helper_c
from buildable_c_base import BuildableCBase
from buildable_mgr_bases import BuildableCreator
from helper_configure_in import AC_PROG_YACC, AC_PROG_CC, AC_PROG_CXX
from core.error import Error
from paragraph import OrderedParagraphSet

class BuildableYaccCreator(BuildableCreator):
    def create_from_file(self, dir, filename, lines):
        if self.is_valid_ext(filename):
            return BuildableYacc(
                dir=dir,
                filename=filename,
                lines=lines)
        return None

    def is_valid_ext(self, filename):
        return filename.endswith('.y') or filename.endswith('.yy')    

class BuildableYacc(BuildableCBase):

    def __init__(self,
                 dir,
                 filename,
                 lines):

        BuildableCBase.__init__(self,
                                dir=dir,
                                filename=filename,
                                lines=lines,
                                search_for_main=False)

    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def gather_configure_in(self):

        ret = OrderedParagraphSet()
        ret.update(AC_PROG_YACC)
        if self.filename().endswith('.y'):
            ret.update(AC_PROG_CC)
        else:
            ret.update(AC_PROG_CXX)
        ret.update(BuildableCBase.gather_configure_in(self))
        return ret

    def contribute_makefile_am(self, buildmod):

        # perform the basic C stuff, using our base class

        BuildableCBase.contribute_makefile_am(self, buildmod=buildmod)

        (root, ext) = os.path.splitext(self.filename())
        if ext == '.y':
            buildmod.makefile_am().add_built_sources(root + '.c')
        else:
            buildmod.makefile_am().add_built_sources(root + '.cc')

        # force Yacc to output files named y.tab.h

        buildmod.makefile_am().add_am_yflags('-d');
