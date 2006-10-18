# $Id: buildable_cxx.py,v 1.31 2006/03/22 15:03:54 jfasch Exp $

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


# NOTE: this is essentially a copy of buildable_c.py, and should
# therefore be kept in sync with that.

import os

from buildable_c_base import BuildableCBase
from buildable_mgr_bases import BuildableCreator
from buildinfo_common import BuildInfo_CXXFLAGS
from helper_configure_in import AC_PROG_CXX
from core.error import Error

class BuildableCXXCreator(BuildableCreator):
    def create_from_file(self, dir, filename, lines):
        if self.is_valid_ext(filename):
            return BuildableCXX(dir=dir,
                                filename=filename,
                                lines=lines)
        return None

    def is_valid_ext(self, filename):
        return filename.endswith('.cpp') or \
               filename.endswith('.cc') or \
               filename.endswith('.cxx') or \
               filename.endswith('.C')
    
class BuildableCXX(BuildableCBase):
    def __init__(self,
                 dir,
                 filename,
                 lines):
        
        BuildableCBase.__init__(self,
                                dir=dir,
                                filename=filename,
                                lines=lines,
                                search_for_main=True)

        # C++ compiler flags I get distributed from the content
        # objects in the dependency graph

        self.cxxflags_ = []

    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def gather_build_info(self, modules):

        BuildableCBase.gather_build_info(self, modules)

        for m in modules:
            for bi in m.buildinfos():
                if isinstance(bi, BuildInfo_CXXFLAGS):
                    self.cxxflags_.extend(bi.cxxflags())

    def reset_build_infos(self):

        self.cxxflags_ = []

        BuildableCBase.reset_build_infos(self)

    def gather_configure_in(self):

        return AC_PROG_CXX + BuildableCBase.gather_configure_in(self)

    def contribute_makefile_am(self, buildmod):

        BuildableCBase.contribute_makefile_am(self, buildmod=buildmod)

        for f in self.cxxflags_:
            buildmod.makefile_am().add_am_cxxflags(f)            
