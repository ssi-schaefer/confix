# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from rule import Rule
from list import List
from set import Set
import helper

from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import types

class Makefile_am(object):

    class DirectoryDefinition(object):
        def __init__(self, dirname):
            self.dirname_ = dirname
            self.family_files_ = {}
            pass
        def dirname(self):
            return self.dirname_
        def families(self):
            return self.family_files_.keys()
        def files(self, family):
            return self.family_files_.get(family)
        def add(self, family, files):
            assert type(files) in (types.ListType, types.TupleType)
            ffiles = self.family_files_.setdefault(family, [])
            ffiles.extend(files)
            pass
        pass

    def __init__(self):
        # free lines to be output.

        self.lines_ = []

        # AUTOMAKE_OPTIONS.

        self.automake_options_ = Set(name='AUTOMAKE_OPTIONS', values=[], mitigate=False)

        # SUBDIRS.

        self.subdirs_ = List(name='SUBDIRS', values=[], mitigate=True)

        # "Makefile elements": Rule and List objects.

        self.elements_ = []

        # sets of filenames that will come to rest in EXTRA_DIST,
        # MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES, and
        # MAINTAINERCLEANFILES, respectively.

        self.extra_dist_ = Set(name='EXTRA_DIST', values=[], mitigate=True)
        self.mostlycleanfiles_ = Set(name='MOSTLYCLEANFILES', values=[], mitigate=True)
        self.cleanfiles_ = Set(name='CLEANFILES', values=[], mitigate=True)
        self.distcleanfiles_ = Set(name='DISTCLEANFILES', values=[], mitigate=True)
        self.maintainercleanfiles_ = Set(name='MAINTAINERCLEANFILES', values=[], mitigate=True)

        # AM_CFLAGS, AM_CXXFLAGS, AM_LFLAGS, AM_YFLAGS. we collect
        # them in a dictionary to keep them unique. (keys are the
        # flags themselves, data is irrelevant.)

        self.am_cflags_ = Set(name='AM_CFLAGS', values=[], mitigate=True)
        self.am_cxxflags_ = Set(name='AM_CXXFLAGS', values=[], mitigate=True)
        self.am_lflags_ = Set(name='AM_LFLAGS', values=[], mitigate=True)
        self.am_yflags_ = Set(name='AM_YFLAGS', values=[], mitigate=True)

        # source files (_SOURCES) of compound objects (i.e. libraries
        # and executables).

        self.compound_sources_ = CompoundListManager(unique=True, extension='SOURCES')

        # _LDFLAGS specific to an executable or a library.

        self.compound_ldflags_ = CompoundListManager(unique=False, extension='LDFLAGS')

        # _LIBADD for compound objects.

        self.compound_libadd_ = CompoundListManager(unique=True, extension='LIBADD')

        # _LDADD for compound objects.

        self.compound_ldadd_ = CompoundListManager(unique=True, extension='LDADD')
        
        # _DEPENDENCIES for compound objects.

        self.compound_dependencies_ = CompoundListManager(unique=True, extension='DEPENDENCIES')
        
        # AM_CPPFLAGS. includepath and commandline macros make their
        # way into AM_CPPFLAGS. we maintain them separately because
        # they have different overriding semantics.

        self.includepath_ = []
        self.have_includedir_ = {}

        self.cmdlinemacros_ = {}

        # generic way to register files (programs, libraries, etc.)
        # that will be built, and eventually installed. for example,
        # 'lib_LIBRARIES' is a list of library names that have to be
        # built (ok, we only build one library in a module, but that's
        # another story). other examples are 'bin_PROGRAMS', or
        # 'check_PROGRAMS'.

        # the structure is a dictionary, with the keys being the
        # variables (such as 'lib_LIBRARIES'), and the data being
        # dictionaries that have as keys the filenames that the
        # variable holds. sounds complicated, see the
        # add_dir_primary() method for more.

        self.dir_primary_ = {}

        # directories where files will be installed to
        # {symbolicname -> (dirname, {family -> filelist})}

        # for example:

        # {'publicheader_WXUtils': ('$(includedir)/WX/Utils',
        #                           {'HEADERS': ['error.h',
        #                                        'errortrace.h',
        #                                        'error_impl.h',
        #                                        'error_macros.h']})}

        # note that we predefine the default directories (for
        # include_HEADERS, or data_DATA, for example) -- these must
        # not be explicitly defined in Makefile.am.
        
        self.install_directories_ = {'': Makefile_am.DirectoryDefinition(dirname=None)}

        # TESTS_ENVIRONMENT. a dictionary (string->string) that
        # contains the environment for test programs.

        self.tests_environment_ = {}

        # BUILT_SOURCES. list of files that must be built before
        # everything else is built.

        self.built_sources_ = Set(name='BUILT_SOURCES', values=[], mitigate=True)

        # hook-targets to be made after the local (module) thing is
        # over. see the "all-local:" and "clean-local:" hook target
        # documentation in the automake manual.

        self.all_local_ = Rule(targets=['all-local'])
        self.clean_local_ = Rule(targets=['clean-local'])
        self.install_data_local_ = Rule(targets=['install-data-local'])
        self.distclean_local_ = Rule(targets=['distclean-local'])
        self.mostlyclean_local_  = Rule(targets=['mostlyclean-local'])
        self.maintainer_clean_local_ = Rule(targets=['maintainer-clean-local'])

        pass

    def add_line(self, line): self.lines_.append(line)

    def add_lines(self, lines): self.lines_.extend(lines)

    
    def automake_options(self): return self.automake_options_
    def add_automake_options(self, option): self.automake_options_.add(option)

    def subdirs(self): return self.subdirs_
    def add_subdir(self, subdir): self.subdirs_.append(subdir)

    def elements(self): return self.elements_
    def add_element(self, e): self.elements_.append(e)

    def extra_dist(self): return self.extra_dist_
    def add_extra_dist(self, name): self.extra_dist_.add(name)

    def add_mostlycleanfiles(self, name): self.mostlycleanfiles_.add(name)

    def add_cleanfiles(self, name): self.cleanfiles_.add(name)

    def add_distcleanfiles(self, name): self.distcleanfiles_.add(name)

    def maintainercleanfiles(self): return self.maintainercleanfiles_
    def add_maintainercleanfiles(self, name): self.maintainercleanfiles_.add(name)

    def am_cflags(self): return self.am_cflags_
    def add_am_cflags(self, f): self.am_cflags_.add(f)

    def am_cxxflags(self): return self.am_cxxflags_
    def add_am_cxxflags(self, f): self.am_cxxflags_.add(f)

    def add_am_lflags(self, f): self.am_lflags_.add(f)

    def add_am_yflags(self, f): self.am_yflags_.add(f)

    def compound_sources(self, compound_name):
        return self.compound_sources_.list(compound_name)
    def add_compound_sources(self, compound_name, source):
        self.compound_sources_.add(compound_name, source)
        pass

    def compound_ldflags(self, compound_name):
        return self.compound_ldflags_.list(compound_name)
    def add_compound_ldflags(self, compound_name, flag):
        self.compound_ldflags_.add(compound_name, flag)
        pass

    def compound_libadd(self, compound_name):
        return self.compound_libadd_.list(compound_name)
    def add_compound_libadd(self, compound_name, lib):
        self.compound_libadd_.add(compound_name, lib)
        pass

    def compound_ldadd(self, compound_name):
        return self.compound_ldadd_.list(compound_name)
    def add_compound_ldadd(self, compound_name, lib):
        self.compound_ldadd_.add(compound_name, lib)
        pass

    def compound_dependencies(self, compound_name):
        return self.compound_dependencies_.list(compound_name)
    def add_compound_dependencies(self, compound_name, dependency):
        self.compound_dependencies_.add(compound_name, dependency)
        pass

    def includepath(self): return self.includepath_
    def add_includepath(self, d):
        dirs = d.split()
        for dir in dirs:
            if not self.have_includedir_.has_key(dir):
                self.includepath_.append(dir)
                self.have_includedir_[dir] = 1
                pass
            pass
        pass

    def cmdlinemacros(self):
        return self.cmdlinemacros_
    def add_cmdlinemacro(self, m, value=None):

        if self.cmdlinemacros_.has_key(m):
            if self.cmdlinemacros_[m] != value:
                raise Error("Conflicting definitions of macro "+m+": "+\
                            str(self.cmdlinemacros_[m])+" and "+str(value))
        self.cmdlinemacros_[m] = value
        pass

    def install_directories(self):
        return self.install_directories_
    def define_install_directory(self, symbolicname, dirname):
        assert not self.install_directories_.has_key(symbolicname), symbolicname+' already defined'
        self.install_directories_[symbolicname] = Makefile_am.DirectoryDefinition(dirname=dirname)
        pass
    def add_to_install_directory(self, symbolicname, family, files):
        dirdef = self.install_directories_.get(symbolicname)
        assert dirdef is not None, symbolicname+' is not defined'
        dirdef.add(family=family, files=files)
        pass

    def add_dir_primary(self, dir, primary, filename):

        # insane sanity checks

        assert dir.find('_')<0, "add_dir_primary(): dir cannot contain '_'"
        assert primary.find('_')<0, "add_dir_primary(): primary cannot contain '_'"

        # compose variable

        key = '_'.join([dir, primary])

        # create variable if not yet defined

        if not self.dir_primary_.has_key(key):
            self.dir_primary_[key] = []
            pass

        if filename in self.dir_primary_[key]:
            raise Error('Duplicate addition of "'+filename+' to "'+key+'"')
        self.dir_primary_[key].append(filename)
        pass

    def dir_primary(self, dir, primary):

        # insane sanity checks

        assert dir.find('_')<0, "dir_primary(): dir cannot contain '_'"
        assert primary.find('_')<0, "dir_primary(): primary cannot contain '_'"

        # compose variable

        key = '_'.join([dir, primary])

        if not self.dir_primary_.has_key(key):
            return []

        return self.dir_primary_[key]

    def add_library(self, libname):
        self.add_dir_primary('lib', 'LIBRARIES', libname)
        pass
        
    def ltlibraries(self): return self.dir_primary('lib', 'LTLIBRARIES')        
    def add_ltlibrary(self, libname):
        self.add_dir_primary('lib', 'LTLIBRARIES', libname)
        pass

    def bin_programs(self): return self.dir_primary('bin', 'PROGRAMS')
    def add_bin_program(self, progname):
        self.add_dir_primary('bin', 'PROGRAMS', progname)
        pass

    def add_bin_script(self, scriptname):
        self.add_dir_primary('bin', 'SCRIPTS', scriptname)
        pass

    def check_programs(self): return self.dir_primary('check', 'PROGRAMS')
    def add_check_program(self, progname):
        self.add_dir_primary('check', 'PROGRAMS', progname)
        pass

    def add_check_script(self, scriptname):
        self.add_dir_primary('check', 'SCRIPTS', scriptname)
        pass
    
    def noinst_programs(self): return self.dir_primary('noinst', 'PROGRAMS')
    def add_noinst_program(self, progname):
        self.add_dir_primary('noinst', 'PROGRAMS', progname)
        pass

    def add_noinst_script(self, scriptname):
        self.add_dir_primary('noinst', 'SCRIPTS', scriptname)
        pass

    def tests_environment(self): return self.tests_environment_        
    def add_tests_environment(self, name, value):
        assert type(name) is types.StringType
        assert type(value) is types.StringType
        self.tests_environment_[name] = value
        pass

    def add_built_sources(self, filename):
        self.built_sources_.add(filename)
        pass

    def all_local(self): return self.all_local_
    def add_all_local(self, hook):
        self.all_local_.add_prerequisite(hook)
        pass
    def clean_local(self): return self.clean_local_
    def add_clean_local(self, hook):
        self.clean_local_.add_prerequisite(hook)
        pass
    def install_data_local(self): return self.install_data_local_
    def add_install_data_local(self, hook):
        self.install_data_local_.add_prerequisite(hook)
        pass
    def distclean_local(self): return self.distclean_local_
    def add_distclean_local(self, hook):
        self.distclean_local_.add_prerequisite(hook)
        pass
    def mostlyclean_local(self): return self.mostlyclean_local_
    def add_mostlyclean_local(self, hook):
        self.mostlyclean_local_.add_prerequisite(hook)
        pass
    def maintainer_clean_local(self): return self.maintainer_clean_local_
    def add_maintainer_clean_local(self, hook):
        self.maintainer_clean_local_.add_prerequisite(hook)
        pass

    def lines(self):
        lines = ['# DO NOT EDIT! This file was automatically generated',
                 '# by Confix version '+const.CONFIX_VERSION,
                 '']

        # AUTOMAKE_OPTIONS
        lines.extend(self.automake_options_.lines())

        # SUBDIRS

        lines.extend(self.subdirs_.lines())

        # Free Makefile elements

        for e in self.elements_:
            lines.extend(e.lines())
            pass

        # EXTRA_DIST, MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES,
        # and MAINTAINERCLEANFILES

        lines.extend(self.extra_dist_.lines())
        lines.extend(self.mostlycleanfiles_.lines())
        lines.extend(self.cleanfiles_.lines())
        lines.extend(self.distcleanfiles_.lines())
        lines.extend(self.maintainercleanfiles_.lines())
        lines.append('')

        # AM_{C,CXX,L,Y}FLAGS, straightforwardly.

        lines.extend(self.am_cflags_.lines())
        lines.extend(self.am_cxxflags_.lines())
        lines.extend(self.am_lflags_.lines())
        lines.extend(self.am_yflags_.lines())

        # AM_CPPFLAGS. it is supposed to contain include paths and
        # macros.

        am_cppflags = List(name='AM_CPPFLAGS', values=self.includepath_, mitigate=True)
        for m in self.cmdlinemacros_.iterkeys():
            macro = '-D' + m
            if self.cmdlinemacros_[m] is not None:
                macro = macro + '=' + self.cmdlinemacros_[m]
                pass
            am_cppflags.append(macro)
            pass
        lines.extend(am_cppflags.lines())
 
        # primaries

        for dp in self.dir_primary_.iterkeys():
            assert len(self.dir_primary_[dp])
            lines.extend(List(name=dp, values=self.dir_primary_[dp], mitigate=False).lines())
            pass

        # compound-sources and such
        lines.extend(self.compound_sources_.lines())
        lines.extend(self.compound_ldflags_.lines())
        lines.extend(self.compound_libadd_.lines())
        lines.extend(self.compound_ldadd_.lines())
        lines.extend(self.compound_dependencies_.lines())

        # install directories
        for symbolicname, dirdef in self.install_directories_.iteritems():
            if symbolicname != '':
                lines.extend(List(name=symbolicname+'dir',
                                  values=[dirdef.dirname()],
                                  mitigate=False)
                             .lines())
                pass
            for family in dirdef.families():
                if symbolicname == '':
                    if family == 'HEADERS':
                        the_symname = 'include'
                    elif family == 'DATA':
                        the_symname = 'data'
                    else:
                        assert 0, 'unknown family "'+family+'"'
                        pass
                    pass
                else:
                    the_symname = symbolicname
                    pass
                lines.extend(List(name=the_symname+'_'+family,
                                  values=dirdef.files(family),
                                  mitigate=True)
                             .lines())
                pass
            pass
        
        # register automatic tests and set their environment

        tests = self.dir_primary('check', 'PROGRAMS') + \
                self.dir_primary('check', 'SCRIPTS')
        if len(tests):
            lines.extend(List(name='TESTS', values=tests, mitigate=True).lines())
            if len(self.tests_environment_):
                lines.extend(List(name='TESTS_ENVIRONMENT',
                                  values=[k+'='+self.tests_environment_[k] \
                                          for k in self.tests_environment_.iterkeys()],
                                  mitigate=True)
                             .lines())
                pass
            pass

        # BUILT_SOURCES
        lines.extend(self.built_sources_.lines())

        # the registered local-hooks.

        lines.extend(self.all_local_.lines())
        lines.extend(self.clean_local_.lines())
        lines.extend(self.install_data_local_.lines())
        lines.extend(self.distclean_local_.lines())
        lines.extend(self.mostlyclean_local_.lines())
        lines.extend(self.maintainer_clean_local_.lines())

        # code directly contributed by my files.

        lines.append('')
        lines.extend(self.lines_)

        return lines

    pass

class CompoundList:
    def __init__(self, unique):
        self.list_ = []
        if unique:
            self.have_ = set()
        else:
            self.have_ = None
            pass
        pass
    def add(self, member):
        assert type(member) is types.StringType, str(member)
        if self.have_ is not None:
            if member in self.have_:
                raise Error('Duplicate addition of "'+member+'"')
            self.have_.add(member)
            pass
        self.list_.append(member)
        pass
    def list(self):
        return self.list_
    pass

class CompoundListManager:
    def __init__(self,
                 unique, # complain about duplicates?
                 extension, # e.g. SOURCES, or LIBADD, and such
                 ):
        self.compounds_ = {}
        self.unique_ = unique
        self.extension_ = extension
        pass
    def add(self, compound_name, member):
        canonic_name = helper.automake_name(compound_name)
        compound_list = self.compounds_.get(canonic_name)
        if compound_list is None:
            compound_list = CompoundList(self.unique_)
            self.compounds_[canonic_name] = compound_list
            pass
        try:
            compound_list.add(member)
        except Error, e:
            raise Error('Cannot add member "'+member+'" to "'+compound_name+'_'+self.extension_+'"', [e])
        pass
    def list(self, compound_name):
        canonic_name = helper.automake_name(compound_name)
        list = self.compounds_.get(canonic_name)
        if list:
            return list.list()
        else:
            return None
        pass
    def lines(self):
        ret = []
        for compound_name, list in self.compounds_.iteritems():
            assert len(list.list()) > 0
            ret.extend(List(name=compound_name+'_'+self.extension_,
                            values=list.list(),
                            mitigate=True)
                       .lines())
            pass
        return ret
    pass
