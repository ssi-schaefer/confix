# $Id: buildable_clusterer_c.py,v 1.13 2006/06/21 11:06:49 jfasch Exp $

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

from buildable_mgr_bases import BuildableClusterer
from buildable_single import BuildableSingle
from buildable_c_base import BuildableCBase
from buildable_h import BuildableHeader
from buildable_exe import BuildableExecutable
from buildable_library import BuildableLibrary
from core.error import Error

class BuildableClusterer_C(BuildableClusterer):

    def __init__(self):
        # key: package name
        # value: set of already assigned names
        self.exenames_per_package_ = {}
        self.libnames_per_package_ = {}
        pass

    def make_clusters(self, buildables, existing_clusters, module):

        # if we already have a library, we don't create anything since
        # that library will consume all c-type buildables.

        # also we take care not to generate executables twice.

        # note that we do not correctly handle the case where we see a
        # main() buildable after we have created a library. we abort
        # in this case. the correct way to handle this would be to
        # break up the library cluster and to re-add its now-free
        # buildables to the active buildables.

        existing_lib = None
        existing_exes = []
        for c in existing_clusters:
            if isinstance(c, BuildableLibrary):
                assert not existing_lib, "Building 2 libraries?"
                existing_lib = c
            elif isinstance(c, BuildableExecutable):
                existing_exes.append(c)

        assert not (existing_lib and len(existing_exes)), "Building executables and a library?"

        main_buildables = []
        no_main_buildables = []
        
        for b in buildables:
            if not isinstance(b, BuildableCBase): continue
            if isinstance(b, BuildableHeader):
                # a header file shouldn't make us build anything
                continue
            if b.has_main():
                main_buildables.append(b)
            else:
                no_main_buildables.append(b)

        if len(main_buildables) and existing_lib:
            raise Error("Cannot build executables when already building a library")

        if len(main_buildables):
            return [self.make_exe_(center=b, module=module) for b in main_buildables]

        if len(existing_exes):
            # we are already building executables, thus we must not
            # create a library at this point.
            return []

        if len(no_main_buildables) and not existing_lib:
            return [self.make_lib_(module=module)]

        return []

    def make_exe_(self, center, module):

        if center.filename().startswith('_check'):
            what = BuildableExecutable.CHECK
        elif center.filename().startswith('_'):
            what = BuildableExecutable.NOINST
        else:
            what = BuildableExecutable.BIN
            pass

        assigned_names = self.exenames_per_package_.setdefault(module.packagename(), set())
        exename = center.exename()
        if not exename:
            root, ext = os.path.splitext(center.filename())
            exename = self.find_unassigned_name_(packagename=module.packagename(),
                                                 available=module.localname()+[root],
                                                 assigned=assigned_names)
            pass

        if exename in assigned_names:
            raise Error('Executable name '+exename+' has already been assigned')
        assigned_names.add(exename)

        return BuildableExecutable(dir=center.dir(),
                                   name=exename,
                                   what=what,
                                   center=center,
                                   use_libtool=module.use_libtool())

    def make_lib_(self, module):
        assigned_names = self.libnames_per_package_.setdefault(module.packagename(), set())
        name = module.buildmodprops().get_libname()
        if name is None:
            name = self.find_unassigned_name_(packagename=module.packagename(),
                                              available=module.localname(),
                                              assigned=assigned_names)
            pass

        if name in assigned_names:
            raise Error('Library name '+name+' has already been assigned')
        assigned_names.add(name)

        return BuildableLibrary(dir=module.dir(),
                                name=name,
                                use_libtool=module.use_libtool())

    def find_unassigned_name_(self,
                              packagename,
                              available,
                              assigned):

        if len(available) == 0:
            if packagename in assigned:
                raise Error('Name '+packagename+' has already been assigned')
            return packagename

        candidate = []
        iter = range(len(available))
        iter.reverse()
        
        for i in iter:
            candidate.insert(0, available[i])
            name = '_'.join([packagename]+candidate)
            if name not in assigned:
                return name
            pass

        raise Error('Could not find unique name for '+'.'.join(available))
