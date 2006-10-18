# $Id: buildable_exe.py,v 1.46 2006/06/21 11:09:32 jfasch Exp $

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
import helper_automake
import helper_configure_in
import readonly_prefixes
from buildable_linked import BuildableLinked
from buildable_c_base import BuildableCBase
from buildable_h import BuildableHeader
from buildable_mgr_bases import BuildableCluster
from provide_callable import Provide_Callable
from helper_configure_in import AC_PROG_LIBTOOL
from paragraph import OrderedParagraphSet, Paragraph

class BuildableExecutable(BuildableLinked, BuildableCluster):

    """ Builds an executable. """

    BIN = 0 # in confix2
    CHECK = 1 # in confix2
    NOINST = 2 # in confix2

    def __init__(
        self,
        name,
        dir,
        center,
        what,
        use_libtool):

        BuildableLinked.__init__(
            self,
            name=name,
            dir=dir)

        BuildableCluster.__init__(self)

        assert what in [BuildableExecutable.BIN, BuildableExecutable.CHECK, BuildableExecutable.NOINST]

        self.exename_ = name
        self.what_ = what

        self.center_ = center

        self.use_libtool_ = use_libtool

        self.add_provide(Provide_Callable(exename=self.exename_))

    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def center(self):

        return self.center_

    def cluster_add(self, buildable):

        # reject any buildables which are not C

        if not isinstance(buildable, BuildableCBase):
            return BuildableCluster.ADD_REJECT

        # reject main() buildable that is not our center. an
        # executable cannot have two main() functions.

        if buildable.has_main() and buildable is not self.center_:
            return BuildableCluster.ADD_REJECT

        # accept our center exclusively (so that nobody else can take
        # it accidentally, for whatever reason).

        if buildable.has_main() and buildable is self.center_:

            # we use to take our center ADD_EXCLUSIVE, so we shouldn't
            # see it twice.
            assert buildable not in self.members()

            self.add_member(buildable)
            return BuildableCluster.ADD_EXCLUSIVE

        # accept non-main buildables, but leave it open to others to
        # take that buildable as well. note that we inhibit
        # installation of header files once we have taken them.

        if buildable in self.members():
            return BuildableCluster.ADD_NOCHANGE

        if isinstance(buildable, BuildableHeader):
            buildable.set_provide_mode(BuildableHeader.PROVIDE_NOTATALL)
        self.add_member(buildable)

        if buildable is self.center_:
            return BuildableCluster.ADD_EXCLUSIVE
        else:
            return BuildableCluster.ADD_SHARED

    def validate(self):

        BuildableLinked.validate(self)

    def contribute_makefile_am(self, buildmod):

        core.debug.indent()

        BuildableLinked.contribute_makefile_am(self, buildmod=buildmod)

        # register ourselves with the module. how we register depends
        # on our filename, as always.

        if self.what_ == BuildableExecutable.BIN: # in confix2
            buildmod.makefile_am().add_bin_program(self.exename_) # in confix2
        elif self.what_ == BuildableExecutable.CHECK: # in confix2
            buildmod.makefile_am().add_check_program(self.exename_) # in confix2
        elif self.what_ == BuildableExecutable.NOINST: # in confix2
            buildmod.makefile_am().add_noinst_program(self.exename_) # in confix2
        else: assert 0 # in confix2

        # register our members with the module.

        builds = []
        for m in self.members():
            builds.append(m.filename())

        progname = helper_automake.automake_name(self.exename_)

        buildmod.makefile_am().add_lines(helper_automake.format_list(
            name=progname+'_SOURCES',
            values=builds))
        
        buildmod.makefile_am().add_lines(helper_automake.format_list(
            name=progname+'_LDADD',
            values=self.get_linkline()))

        # add dependencies for local libraries. note that we can only
        # do this if we are not using libtool - only in this case we
        # know the name of the library that will be generated. if we
        # are using libtool, we cannot know what te user will choose
        # to generate (--disble-shared, --enable-shared, or even .sl,
        # .so, .dll, ...).

        # however, this whole stuff here is a bad heuristic anyway
        # which should better be handled by the autotools (in the
        # automake manual, '_DEPENDENCIES', they claim to calculate
        # dependencies, but I cannot imagine how they would accomplish
        # this.

        if not self.use_libtool_:
            deps = []
            for dir, name in self.local_dep_libraries():
                deps.append("$(top_builddir)/"+dir+'/lib'+name+'.a')
                pass
            for name in self.installed_dep_libraries():
                deps.append('@deplib_'+helper_automake.automake_name(name)+'@')
                pass
            
            buildmod.makefile_am().add_lines(helper_automake.format_list(
                name=progname+'_DEPENDENCIES',
                values=deps))
            pass

        # bad heuristics for installed libraries as well. as opposed
        # to the local stuff above, here we can check for existence of
        # a static library. only in this case we add a dependency -
        # there's no need to relink when using a shared library.

        # again: however if we have both static and shared installed
        # libraries, and the user chooses to use shared libraries
        # (this is the default on most systems I am aware of), then we
        # trigger a false relink.
            
        code.extend(
            ['libs="'+' '.join(self.installed_dep_libraries())+'"',
             "# cannot use ${libdir} because it is left unexpanded as",
             "# '${exec_prefix}/lib', and ${exec_prefix} is set to",
             "# NONE. still don't know what's going on.",
             'dirs="${prefix}/lib ${'+readonly_prefixes.libdirs_var+'}"',
             'for lib in ${libs}; do',
             '    for dir in ${dirs}; do',
             '        libfile=${dir}/lib${lib}.a',
             '        if test -f ${libfile}; then',
             '            deps="${deps} ${libfile}"',
             '            break',
             '        fi',
             '    done',
             'done',
             self.depsubstvar_()+'=${deps}',
             'AC_SUBST('+self.depsubstvar_()+')'
             ])

    def gather_configure_in(self):
        ret = OrderedParagraphSet()
        if self.use_libtool_ == 1:
            ret.update(AC_PROG_LIBTOOL)
            pass
        ret.update(BuildableLinked.gather_configure_in(self))

        # see the comment in contribute_makefile_am() for this one

        if not self.use_libtool_:
            libsearch_code = [
                '# Search for the actual location of ',
                '# the libraries we will link against.',
                'dirs="${prefix}/lib ${'+readonly_prefixes.libdirs_var+'}"',
                "# cannot use ${libdir} because it is left unexpanded as",
                "# '${exec_prefix}/lib', and ${exec_prefix} is set to",
                "# NONE. still don't know what's going on."]

            for name in self.installed_dep_libraries():
                libsearch_code.extend([
                    'deplib_'+helper_automake.automake_name(name)+'=',
                    'for dir in ${dirs}; do',
                    '    libfile=${dir}/lib'+name+'.a',
                    '    if test -f ${libfile}; then',
                    '        deplib_'+helper_automake.automake_name(name)+'=${libfile}',
                    '        break',
                    '    fi',
                    'done',
                    'AC_SUBST(deplib_'+helper_automake.automake_name(name)+')',
                    ''])
                pass

            ret.add(order=helper_configure_in.ORDER_LIBRARIES,
                    paragraph=Paragraph(libsearch_code))

        return ret
