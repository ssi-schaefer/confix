# $Id: buildable_library.py,v 1.10 2006/07/13 20:27:24 jfasch Exp $

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
import re

import core.debug
import versions
import helper_automake
from buildable_linked import BuildableLinked
from buildable_c_base import BuildableCBase
from buildable_cxx import BuildableCXX
from buildable_mgr_bases import BuildableCluster
from helper_configure_in import AC_PROG_RANLIB, AC_PROG_LIBTOOL
from buildinfo_common import BuildInfo_CIncludePath_NativeLocal, BuildInfo_CLibrary_NativeLocal
from core.error import Error

class BuildableLibrary(BuildableLinked, BuildableCluster):

    def __init__(self, name, dir, use_libtool, libtool_version_info=None):

        BuildableLinked.__init__(
            self,
            name=name,
            dir=dir)

        BuildableCluster.__init__(self)

        self.use_libtool_ = use_libtool # in confix2 
        self.libtool_version_info_ = libtool_version_info # in confix2

        self.add_buildinfo(BuildInfo_CIncludePath_NativeLocal())
        self.add_buildinfo(BuildInfo_CLibrary_NativeLocal(self.dir(), self.name()))
        pass

    def __str__(self):
        return 'BuildableLibrary '+os.path.join(self.dir(), self._libname())

    def cluster_add(self, buildable):

        # reject anything that is not C

        if not isinstance(buildable, BuildableCBase):
            return BuildableCluster.ADD_REJECT

        assert not buildable.has_main(), "Huh? Adding main() function to library?"
        assert not buildable in self.members(), "Seen (eaten) that already"

        # accept everything that is C. others must not take it.

        self.add_member(buildable)
        return BuildableCluster.ADD_EXCLUSIVE

    def validate(self):

        BuildableLinked.validate(self)

        if self.use_libtool_:

            # if we have C++ buildables, libtool < 1.5 will not be
            # able to deal with that. FIXME: should do this once and
            # for all, but couldn't find an appropriate place.

            for m in self.members():
                if isinstance(m, BuildableCXX):
                    check_libtool_version('libtool', '1.5')
                    break

    def gather_configure_in(self):

        if self.use_libtool_:
            return AC_PROG_LIBTOOL + BuildableLinked.gather_configure_in(self)
        else:
            return AC_PROG_RANLIB + BuildableLinked.gather_configure_in(self)
        pass

    def contribute_makefile_am(self, buildmod):

        BuildableLinked.contribute_makefile_am(self, buildmod=buildmod)

        canonic_libname = helper_automake.automake_name(self._libname())

        if self.use_libtool_:

            buildmod.makefile_am().add_lines(helper_automake.format_list( # in confix2
                name='lib'+helper_automake.automake_name(self.name())+'_la_SOURCES', # in confix2
                values=[m.filename() for m in self.members()])) # in confix2

            buildmod.makefile_am().add_lines(helper_automake.format_list( # in confix2
                name=canonic_libname+'_LIBADD', # in confix2
                values=self.get_linkline())) # in confix2

            buildmod.makefile_am().add_ltlibrary(self._libname()) # in confix2

            libtool_args = []

            # -no-undefined libtool flag: my understanding is that
            # under Doze it is not supported that one DLL has
            # undefined symbols that are resolved by another
            # DLL. Seems like their dynamic loader is extremely simple
            # minded in that it refuses to follow these chains.

            libtool_args.append('-no-undefined')

            # add libtool version info if it was explicitly passed (we
            # leave the default up to libtool)

            if self.libtool_version_info_ is not None: # in confix2
                libtool_args.append(':'.join(self.libtool_version_info_)) # in confix2
                pass # in confix2

            if len(libtool_args): # in confix2
                buildmod.makefile_am().add_lines(helper_automake.format_list( # in confix2
                    name=canonic_libname+'_LDFLAGS', # in confix2
                    values=libtool_args)) # in confix2
                pass # in confix2
            
        else:

            buildmod.makefile_am().add_lines(helper_automake.format_list( # in confix2
                name='lib'+helper_automake.automake_name(self.name())+'_a_SOURCES', # in confix2
                values=[m.filename() for m in self.members()])) # in confix2

            buildmod.makefile_am().add_library(self._libname()) # in confix2

    def _libname(self):

        if self.use_libtool_:
            return 'lib'+self.name()+'.la'
        else:
            return 'lib'+self.name()+'.a'
            
def check_libtool_version(libtool, required_version):
    ltver = libtool_version(libtool)
    if versions.compare_version_strings(ltver, required_version) < 0:
        raise Error('Libtool version too low for C++ '
                    '(found '+libtool+' version '+ltver+', required '+required_version+')')

__libtool_version = None
def libtool_version(libtool):
    global __libtool_version

    if __libtool_version is not None:
        return __libtool_version

    cmd = libtool + ' --version'
    pipe = os.popen(cmd)
    lines = pipe.readlines()
    pipe.close()
    version_line = lines[0]

    re_ver = re.compile(r'\(GNU libtool\)\s*(\d+\.\d+(?:\.[\d\w]+)?)\s')

    m = re_ver.search(version_line)
    if not m:
        raise Error('Cannot determine libtool version '
                    '(command was "'+cmd+'"): could not interpret '
                    'version string "'+version_line+'"')

    __libtool_version = m.group(1)
    return __libtool_version
