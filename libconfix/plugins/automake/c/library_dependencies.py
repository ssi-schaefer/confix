# Copyright (C) 2006-2009 Joerg Faschingbauer

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

from libconfix.plugins.automake import readonly_prefixes
from libconfix.plugins.automake import helper
from libconfix.plugins.automake.configure_ac import Configure_ac
from libconfix.plugins.automake.out_automake import find_automake_output_builder

from libconfix.plugins.c.executable import ExecutableBuilder
from libconfix.plugins.c.buildinfo import BuildInfo_CLibrary_NativeLocal, BuildInfo_CLibrary_NativeInstalled

from libconfix.core.machinery.setup import Setup
from libconfix.core.machinery.builder import Builder
from libconfix.core.utils.paragraph import Paragraph

class LibraryDependenciesFinderSetup(Setup):
    def __init__(self, use_libtool):
        Setup.__init__(self)
        self.__use_libtool = use_libtool
        pass
    def setup(self, dirbuilder):
        dirbuilder.add_builder(ExecutableWatcher(use_libtool=self.__use_libtool))
        pass
    pass

class ExecutableWatcher(Builder):

    """
    Among my parent's builders, watch out for ones of type
    ExecutableBuilder. If I see one that doesn't use libtool, create a
    LibraryDependenciesFinder for him. If an ExecutableBuilder
    disappears for which I have created a LibraryDependenciesFinder,
    then I remove that object.
    """
    
    def __init__(self, use_libtool):
        Builder.__init__(self)
        self.__use_libtool = use_libtool
        # { exebuilder: depfinder }
        self.__library_dependency_finder_by_exe = {}
        pass

    def locally_unique_id(self):
        # I am supposed to the only one of my kind among all the
        # builders in a directory, so my class suffices as a unique
        # id.
        return str(self.__class__)

    def enlarge(self):
        super(ExecutableWatcher, self).enlarge()

        current_exes = set()
        for exe in self.parentbuilder().iter_builders():
            if isinstance(exe, ExecutableBuilder):
                current_exes.add(exe)
                pass
            pass

        # kick depfinders whose exe has disappeared
        rem_exes = []
        for exe, depfinder in self.__library_dependency_finder_by_exe.iteritems():
            if exe not in current_exes:
                self.parentbuilder().remove_builder(depfinder)
                rem_exes.append(exe)
                pass
            pass
        for exe in rem_exes:
            del self.__library_dependency_finder_by_exe[exe]
            pass

        # add depfinders for new exes
        for exe in current_exes:
            if exe not in self.__library_dependency_finder_by_exe:
                depfinder = self.parentbuilder().add_builder(LibraryDependenciesFinder(exe))
                self.__library_dependency_finder_by_exe[exe] = depfinder
                pass
            pass
        pass

    pass

class LibraryDependenciesFinder(Builder):

    """ Do the real hard work. On output(), write an appropriate
    <name_of_our_linked_builder>_DEPENDENCIES construct to our
    Makefile.am that contains substitutions for the libraries our
    linked_builder depends on. Generate configure.ac code to find and
    substitute them."""
    
    def __init__(self, exe_builder):
        Builder.__init__(self)
        self.__exe_builder = exe_builder
        pass

    def locally_unique_id(self):
        return str(self.__class__) + ':' + self.__exe_builder.center().file().name()

    def exe_builder(self): return self.__exe_builder

    def output(self):
        super(LibraryDependenciesFinder, self).output()

        automake_output_builder = find_automake_output_builder(self.parentbuilder())

        # sort out local and installed library infos for later use
        # below.
        local_libs = []
        installed_libs = []
        for lib_buildinfo in self.__exe_builder.topo_libraries():
            if isinstance(lib_buildinfo, BuildInfo_CLibrary_NativeLocal):
                local_libs.append(lib_buildinfo)
                continue
            if isinstance(lib_buildinfo, BuildInfo_CLibrary_NativeInstalled):
                installed_libs.append(lib_buildinfo)
                continue
            pass

        # provide a "function" (yeah, in M4, you know :-) to search
        # for our libraries. acinclude.m4.
        automake_output_builder.acinclude_m4().add_paragraph(
            paragraph=Paragraph(lines=[m4_installed_libsearch_func]))

        # write Makefile.am stuff: blah_DEPENDENCIES
        for lib_buildinfo in local_libs:
            automake_output_builder.makefile_am().add_compound_dependencies(
                compound_name=helper.automake_name(self.__exe_builder.exename()),
                dependency='$(top_builddir)/'+'/'.join(lib_buildinfo.dir())+'/lib'+lib_buildinfo.basename()+'.a')
            pass
        for lib_buildinfo in installed_libs:
            automake_output_builder.makefile_am().add_compound_dependencies(
                compound_name=helper.automake_name(self.__exe_builder.exename()),
                dependency='@'+self.installed_substname(lib_buildinfo.basename())+'@')
            pass

        # add code to configure.ac which searches for our libraries,
        # and substitutes the output variables.
        for lib_buildinfo in installed_libs:
            automake_output_builder.configure_ac().add_paragraph(
                paragraph=Paragraph(lines=['CONFIX_LIBDEPS_SEARCH_INSTALLED_LIBRARY(',
                                           '    ['+self.installed_substname(lib_buildinfo.basename())+'],',
                                           # cannot use ${libdir}
                                           # because it is left
                                           # unexpanded as
                                           # '${exec_prefix}/lib', and
                                           # ${exec_prefix} is set to
                                           # NONE. still don't know
                                           # what's going on.
                                           '    [${prefix}/lib ${'+readonly_prefixes.libdirs_var+'}],',
                                           '    ['+lib_buildinfo.basename()+'])']),
                order=Configure_ac.LIBRARIES)
            pass
        pass

    def local_substname(self, dir, name):
        return helper.automake_name('localdeplib_'+'_'.join(dir)+'_'+name)
    def installed_substname(self, name):
        return helper.automake_name('installeddeplib_'+name)
    pass

m4_installed_libsearch_func = """

dnl $1: name of the output variable to substitute
dnl $2: search directories, separated with space
dnl $3: basename of the library

AC_DEFUN([CONFIX_LIBDEPS_SEARCH_INSTALLED_LIBRARY],
[

$1=
found=
for dir in $2; do
    libfile=${dir}/lib$3.a
    if test -f ${libfile}; then
        $1=${libfile}
        found=true
        break
    fi
done
if test x${found} != xtrue; then
    AC_MSG_WARN([nothing found for -l$3])
fi
AC_SUBST($1)

])

"""
