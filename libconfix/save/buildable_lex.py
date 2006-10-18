# $Id: buildable_lex.py,v 1.28 2006/03/22 15:03:54 jfasch Exp $

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

from buildable_c_base import BuildableCBase
from buildable_mgr_bases import BuildableCreator
from helper_configure_in import AM_PROG_LEX, AC_PROG_CC, AC_PROG_CXX
from core.error import Error
from paragraph import OrderedParagraphSet

class BuildableLexCreator(BuildableCreator):
    def create_from_file(self, dir, filename, lines):
        if self.is_valid_ext(filename):
            return BuildableLex(
                dir=dir,
                filename=filename,
                lines=lines)
        return None

    def is_valid_ext(self, filename):
        return filename.endswith('.l') or filename.endswith('.ll')    

class BuildableLex(BuildableCBase):
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
        ret.update(AM_PROG_LEX)
        if self.filename().endswith('.l'):
            ret.update(AC_PROG_CC)
        else:
            ret.update(AC_PROG_CXX)
        ret.update(BuildableCBase.gather_configure_in(self))
        return ret

    def contribute_makefile_am(self, buildmod):

        # perform the basic C stuff, using our base class

        BuildableCBase.contribute_makefile_am(self, buildmod=buildmod)

        (root, ext) = os.path.splitext(self.filename())
        if ext == '.l':
            buildmod.makefile_am().add_built_sources(root + '.c')
        else:

            # argh: when using "%option c++" in the lex source file,
            # flex generates lex.yy.cc, which automake doesn't seem to
            # be aware of. force it to generate the file automake is
            # aware of. this is not supposed to work with other lexers
            # however. but, as the documentation states, it is better
            # to not use the C++ feature of lex since it is inherently
            # non-portable anyway.
            
            buildmod.makefile_am().add_am_lflags('-olex.yy.c')
            
            buildmod.makefile_am().add_built_sources(root + '.cc')
