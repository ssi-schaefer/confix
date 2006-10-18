# $Id: buildable_linked.py,v 1.15 2006/07/13 20:27:24 jfasch Exp $

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
from sets import Set

from buildable_composite import BuildableComposite
from buildinfo_common import \
     BuildInfo_CLibrary_NativeLocal, \
     BuildInfo_CLibrary_NativeInstalled, \
     BuildInfo_CLibrary_External
import helper_configure_in
import helper_optmod
import readonly_prefixes

class BuildableLinked(BuildableComposite):

    """ Serves as an abstraction for everything that is built using
    the linker (such as an executable or a shared library, or even
    only ar - which we consider linked just as libtool does).

    """

    def __init__(self,
                 name,
                 dir):

        BuildableComposite.__init__(self,
                                    name=name,
                                    dir=dir)

        # names of directories (relative to the package root
        # directory) of the local package which we will be using
        # libraries from. these must appear on the linker command
        # line, as -L arguments.

        self.reverse_local_dirs_ = []
        self.have_local_dirs_ = Set()

        # -L arguments to the linker. these come from external
        # -modules, so we pass them literally, as if they began with
        # --L.

        self.reverse_external_libpath_ = []
        self.have_external_libpath_ = Set()

        # the libraries themselves.

        self.reverse_libraries_ = []
        self.have_installed_library_ = False

        # libraries we depend upon. the order does not matter. we
        # distinguish between libraries local to the package and
        # installed libraries.

        # local libraries; list of tuples (relative-dir,
        # basename). for example [('the/dir', 'somelibrary')], which
        # will be transformed into the dependency
        # '$(top_builddir)/the/dir/libsomelibrary.a'.

        self.local_dep_libraries_ = []

        # installed libraries; list of strings, the library base
        # names.

        self.installed_dep_libraries_ = []

        pass

    def gather_build_info(self, modules):

        BuildableComposite.gather_build_info(self, modules)

        for m in modules:
            for bi in m.buildinfos():

                if isinstance(bi, BuildInfo_CLibrary_NativeLocal): # in confix2
                    dir = bi.dir() # in confix2
                    libname = bi.name() # in confix2
                    assert not dir in self.have_local_dirs_, dir + '/' + self.dir() # in confix2
                    self.have_local_dirs_.add(dir) # in confix2
                    self.reverse_local_dirs_.append(dir) # in confix2
                    self.reverse_libraries_.append( # in confix2
                        ['@'+helper_optmod.native_library_linksubstname(libname)+'@']) # in confix2
                    self.add_local_configure_in( # in confix2
                        paragraph=helper_optmod.native_library_linksubst(libname), # in confix2
                        order=helper_configure_in.ORDER_LIBRARIES) # in confix2

                    # dependency libraries
                    self.local_dep_libraries_.append((bi.dir(), bi.name()))
                    
                    continue

                if isinstance(bi, BuildInfo_CLibrary_NativeInstalled):
                    libname = bi.name()
                    self.have_installed_library_ = True
                    self.reverse_libraries_.append(['-l'+libname])

                    # dependency libraries
                    self.installed_dep_libraries_.append(bi.name())
                    
                    continue

                if isinstance(bi, BuildInfo_CLibrary_External):
                    libpaths = bi.libpath()
                    libs = bi.libs()

                    key = '.'.join(libpaths)
                    if not key in self.have_external_libpath_:
                        self.have_external_libpath_.add(key)
                        self.reverse_external_libpath_.append(libpaths)
                    self.reverse_libraries_.append(libs)
                    continue

    def reset_build_infos(self):

        self.reverse_local_dirs_ = []
        self.have_local_dirs_ = Set()

        self.reverse_external_libpath_ = []
        self.have_external_libpath_ = Set()

        self.reverse_libraries_ = []
        self.have_installed_library_ = False

        BuildableComposite.reset_build_infos(self)

    def get_linkline(self):

        linkline = []

        local_dirs = self.reverse_local_dirs_[:]
        local_dirs.reverse()
        linkline.extend([os.path.join('-L$(top_builddir)', dir) for dir in local_dirs])

        if self.have_installed_library_:
            linkline.append('-L$(libdir)')
            linkline.append('$('+readonly_prefixes.libpath_var+')')

        ext_path = self.reverse_external_libpath_[:]
        ext_path.reverse()
        for p in ext_path:
            linkline.extend(p)

        libs = self.reverse_libraries_[:]
        libs.reverse()
        for l in libs:
            linkline.extend(l)

        return linkline

    def local_dep_libraries(self):
        return self.local_dep_libraries_

    def installed_dep_libraries(self):
        return self.installed_dep_libraries_
