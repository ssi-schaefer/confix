# Copyright (C) 2002-2006 Salomon Automation
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

import makefile
import helper

from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import types

class Makefile_am(object):

    class DirectoryDefinition(object):
        def __init__(self, dirname):
            self.dirname_ = dirname
            self.__family_files = {}
            pass
        def dirname(self):
            return self.dirname_
        def families(self):
            return self.__family_files.keys()
        def files(self, family):
            return self.__family_files.get(family)
        def add(self, family, files):
            assert type(files) in (types.ListType, types.TupleType)
            ffiles = self.__family_files.setdefault(family, [])
            ffiles.extend(files)
            pass
        pass

    def __init__(self):
        # free lines to be output.

        self.__lines = []

        # AUTOMAKE_OPTIONS.

        self.__automake_options = makefile.Set(name='AUTOMAKE_OPTIONS', values=[], mitigate=False)

        # SUBDIRS.

        self.__subdirs = makefile.List(name='SUBDIRS', values=[], mitigate=True)

        # "Makefile elements": Rule and List objects.

        self.__elements = []

        # sets of filenames that will come to rest in EXTRA_DIST,
        # MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES, and
        # MAINTAINERCLEANFILES, respectively.

        self.__extra_dist = makefile.Set(name='EXTRA_DIST', values=[], mitigate=True)
        self.__mostlycleanfiles = makefile.Set(name='MOSTLYCLEANFILES', values=[], mitigate=True)
        self.__cleanfiles = makefile.Set(name='CLEANFILES', values=[], mitigate=True)
        self.__distcleanfiles = makefile.Set(name='DISTCLEANFILES', values=[], mitigate=True)
        self.__maintainercleanfiles = makefile.Set(name='MAINTAINERCLEANFILES', values=[], mitigate=True)

        # AM_CFLAGS, AM_CXXFLAGS, AM_LFLAGS, AM_YFLAGS. we collect
        # them in a dictionary to keep them unique. (keys are the
        # flags themselves, data is irrelevant.)

        self.__am_cflags = makefile.Set(name='AM_CFLAGS', values=[], mitigate=True)
        self.__am_cxxflags = makefile.Set(name='AM_CXXFLAGS', values=[], mitigate=True)
        self.__am_lflags = makefile.Set(name='AM_LFLAGS', values=[], mitigate=True)
        self.__am_yflags = makefile.Set(name='AM_YFLAGS', values=[], mitigate=True)

        # source files (_SOURCES) of compound objects (i.e. libraries
        # and executables).

        self.__compound_sources = CompoundListManager(unique=True, extension='SOURCES')

        # _LDFLAGS specific to an executable or a library.

        self.__compound_ldflags = CompoundListManager(unique=False, extension='LDFLAGS')

        # _LIBADD for compound objects.

        self.__compound_libadd = CompoundListManager(unique=True, extension='LIBADD')

        # _LDADD for compound objects.

        self.__compound_ldadd = CompoundListManager(unique=True, extension='LDADD')
        
        # _DEPENDENCIES for compound objects.

        self.__compound_dependencies = CompoundListManager(unique=True, extension='DEPENDENCIES')
        
        # AM_CPPFLAGS. includepath and commandline macros make their
        # way into AM_CPPFLAGS. we maintain them separately because
        # they have different overriding semantics.

        self.__includepath = []
        self.__have_includedir = {}

        self.__cmdlinemacros = {}

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

        self.__dir_primary = {}

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
        
        self.__install_directories = {'': Makefile_am.DirectoryDefinition(dirname=None)}

        # TESTS_ENVIRONMENT. a dictionary (string->string) that
        # contains the environment for test programs.

        self.__tests_environment = {}

        # BUILT_SOURCES. list of files that must be built before
        # everything else is built.

        self.__built_sources = makefile.Set(name='BUILT_SOURCES', values=[], mitigate=True)

        # hook-targets to be made after the local (module) thing is
        # over. see the "all-local:" and "clean-local:" hook target
        # documentation in the automake manual.

        self.__all_local = makefile.Rule(targets=['all-local'])
        self.__clean_local = makefile.Rule(targets=['clean-local'])
        self.__install_data_local = makefile.Rule(targets=['install-data-local'])
        self.__distclean_local = makefile.Rule(targets=['distclean-local'])
        self.__mostlyclean_local  = makefile.Rule(targets=['mostlyclean-local'])
        self.__maintainer_clean_local = makefile.Rule(targets=['maintainer-clean-local'])

        pass

    def add_line(self, line): self.__lines.append(line)

    def add_lines(self, lines): self.__lines.extend(lines)

    
    def automake_options(self): return self.__automake_options
    def add_automake_options(self, option): self.__automake_options.add(option)

    def subdirs(self): return self.__subdirs
    def add_subdir(self, subdir): self.__subdirs.append(subdir)

    def elements(self): return self.__elements
    def add_element(self, e): self.__elements.append(e)

    def extra_dist(self): return self.__extra_dist
    def add_extra_dist(self, name): self.__extra_dist.add(name)

    def add_mostlycleanfiles(self, name): self.__mostlycleanfiles.add(name)

    def add_cleanfiles(self, name): self.__cleanfiles.add(name)

    def distcleanfiles(self): return self.__distcleanfiles
    def add_distcleanfiles(self, name): self.__distcleanfiles.add(name)

    def maintainercleanfiles(self): return self.__maintainercleanfiles
    def add_maintainercleanfiles(self, name): self.__maintainercleanfiles.add(name)

    def am_cflags(self): return self.__am_cflags
    def add_am_cflags(self, f): self.__am_cflags.add(f)

    def am_cxxflags(self): return self.__am_cxxflags
    def add_am_cxxflags(self, f): self.__am_cxxflags.add(f)

    def add_am_lflags(self, f): self.__am_lflags.add(f)

    def add_am_yflags(self, f): self.__am_yflags.add(f)

    def compound_sources(self, compound_name):
        return self.__compound_sources.list(compound_name)
    def add_compound_sources(self, compound_name, source):
        self.__compound_sources.add(compound_name, source)
        pass

    def compound_ldflags(self, compound_name):
        return self.__compound_ldflags.list(compound_name)
    def add_compound_ldflags(self, compound_name, flag):
        self.__compound_ldflags.add(compound_name, flag)
        pass

    def compound_libadd(self, compound_name):
        return self.__compound_libadd.list(compound_name)
    def add_compound_libadd(self, compound_name, lib):
        self.__compound_libadd.add(compound_name, lib)
        pass

    def compound_ldadd(self, compound_name):
        return self.__compound_ldadd.list(compound_name)
    def add_compound_ldadd(self, compound_name, lib):
        self.__compound_ldadd.add(compound_name, lib)
        pass

    def compound_dependencies(self, compound_name):
        return self.__compound_dependencies.list(compound_name)
    def add_compound_dependencies(self, compound_name, dependency):
        self.__compound_dependencies.add(compound_name, dependency)
        pass

    def includepath(self): return self.__includepath
    def add_includepath(self, d):
        dirs = d.split()
        for dir in dirs:
            if not self.__have_includedir.has_key(dir):
                self.__includepath.append(dir)
                self.__have_includedir[dir] = 1
                pass
            pass
        pass

    def cmdlinemacros(self):
        return self.__cmdlinemacros
    def add_cmdlinemacro(self, m, value=None):

        if self.__cmdlinemacros.has_key(m):
            if self.__cmdlinemacros[m] != value:
                raise Error("Conflicting definitions of macro "+m+": "+\
                            str(self.__cmdlinemacros[m])+" and "+str(value))
        self.__cmdlinemacros[m] = value
        pass

    def install_directories(self):
        return self.__install_directories
    def define_install_directory(self, symbolicname, dirname):
        assert not self.__install_directories.has_key(symbolicname), symbolicname+' already defined'
        self.__install_directories[symbolicname] = Makefile_am.DirectoryDefinition(dirname=dirname)
        pass
    def add_to_install_directory(self, symbolicname, family, files):
        dirdef = self.__install_directories.get(symbolicname)
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

        if not self.__dir_primary.has_key(key):
            self.__dir_primary[key] = []
            pass

        if filename in self.__dir_primary[key]:
            raise Error('Duplicate addition of "'+filename+' to "'+key+'"')
        self.__dir_primary[key].append(filename)
        pass

    def dir_primary(self, dir, primary):

        # insane sanity checks

        assert dir.find('_')<0, "dir_primary(): dir cannot contain '_'"
        assert primary.find('_')<0, "dir_primary(): primary cannot contain '_'"

        # compose variable

        key = '_'.join([dir, primary])

        if not self.__dir_primary.has_key(key):
            return []

        return self.__dir_primary[key]

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

    def noinst_headers(self): return self.dir_primary('noinst', 'HEADERS')
    def add_noinst_header(self, header):
        self.add_dir_primary('noinst', 'HEADERS', header)
        pass

    def add_noinst_script(self, scriptname):
        self.add_dir_primary('noinst', 'SCRIPTS', scriptname)
        pass

    def tests_environment(self): return self.__tests_environment        
    def add_tests_environment(self, name, value):
        assert type(name) is types.StringType
        assert type(value) is types.StringType
        self.__tests_environment[name] = value
        pass

    def add_built_sources(self, filename):
        self.__built_sources.add(filename)
        pass

    def all_local(self): return self.__all_local
    def add_all_local(self, hook):
        self.__all_local.add_prerequisite(hook)
        pass
    def clean_local(self): return self.__clean_local
    def add_clean_local(self, hook):
        self.__clean_local.add_prerequisite(hook)
        pass
    def install_data_local(self): return self.__install_data_local
    def add_install_data_local(self, hook):
        self.__install_data_local.add_prerequisite(hook)
        pass
    def distclean_local(self): return self.__distclean_local
    def add_distclean_local(self, hook):
        self.__distclean_local.add_prerequisite(hook)
        pass
    def mostlyclean_local(self): return self.__mostlyclean_local
    def add_mostlyclean_local(self, hook):
        self.__mostlyclean_local.add_prerequisite(hook)
        pass
    def maintainer_clean_local(self): return self.__maintainer_clean_local
    def add_maintainer_clean_local(self, hook):
        self.__maintainer_clean_local.add_prerequisite(hook)
        pass

    def lines(self):
        lines = ['# DO NOT EDIT! This file was automatically generated',
                 '# by Confix version '+const.CONFIX_VERSION,
                 '']

        # AUTOMAKE_OPTIONS
        lines.extend(self.__automake_options.lines())

        # SUBDIRS

        lines.extend(self.__subdirs.lines())

        # Free Makefile elements

        for e in self.__elements:
            lines.extend(e.lines())
            pass

        # EXTRA_DIST, MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES,
        # and MAINTAINERCLEANFILES

        lines.extend(self.__extra_dist.lines())
        lines.extend(self.__mostlycleanfiles.lines())
        lines.extend(self.__cleanfiles.lines())
        lines.extend(self.__distcleanfiles.lines())
        lines.extend(self.__maintainercleanfiles.lines())
        lines.append('')

        # AM_{C,CXX,L,Y}FLAGS, straightforwardly.

        lines.extend(self.__am_cflags.lines())
        lines.extend(self.__am_cxxflags.lines())
        lines.extend(self.__am_lflags.lines())
        lines.extend(self.__am_yflags.lines())

        # AM_CPPFLAGS. it is supposed to contain include paths and
        # macros.

        am_cppflags = makefile.List(name='AM_CPPFLAGS', values=self.__includepath, mitigate=True)
        for m in self.__cmdlinemacros.iterkeys():
            macro = '-D' + m
            if self.__cmdlinemacros[m] is not None:
                macro = macro + '=' + self.__cmdlinemacros[m]
                pass
            am_cppflags.append(macro)
            pass
        lines.extend(am_cppflags.lines())
 
        # primaries

        for dp in self.__dir_primary.iterkeys():
            assert len(self.__dir_primary[dp])
            lines.extend(makefile.List(name=dp, values=self.__dir_primary[dp], mitigate=False).lines())
            pass

        # compound-sources and such
        lines.extend(self.__compound_sources.lines())
        lines.extend(self.__compound_ldflags.lines())
        lines.extend(self.__compound_libadd.lines())
        lines.extend(self.__compound_ldadd.lines())
        lines.extend(self.__compound_dependencies.lines())

        # install directories
        for symbolicname, dirdef in self.__install_directories.iteritems():
            if symbolicname != '':
                lines.extend(makefile.List(name=symbolicname+'dir',
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
                lines.extend(makefile.List(name=the_symname+'_'+family,
                                           values=dirdef.files(family),
                                           mitigate=True)
                             .lines())
                pass
            pass
        
        # register automatic tests and set their environment

        test_tmp = self.dir_primary('check', 'PROGRAMS')
        count = 0
        for prog in test_tmp:
            prog += "$(EXEEXT)"
            test_tmp[count] = prog
            count += 1
            pass

        tests = test_tmp + \
                self.dir_primary('check', 'SCRIPTS')
        if len(tests):
            lines.extend(makefile.List(name='TESTS', values=tests, mitigate=True).lines())
            if len(self.__tests_environment):
                lines.extend(makefile.List(name='TESTS_ENVIRONMENT',
                                           values=[k+'='+self.__tests_environment[k] \
                                                   for k in self.__tests_environment.iterkeys()],
                                           mitigate=True)
                             .lines())
                pass
            pass

        # BUILT_SOURCES
        lines.extend(self.__built_sources.lines())

        # the registered local-hooks.

        lines.extend(self.__all_local.lines())
        lines.extend(self.__clean_local.lines())
        lines.extend(self.__install_data_local.lines())
        lines.extend(self.__distclean_local.lines())
        lines.extend(self.__mostlyclean_local.lines())
        lines.extend(self.__maintainer_clean_local.lines())

        # code directly contributed by my files.

        lines.append('')
        lines.extend(self.__lines)

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
            ret.extend(makefile.List(name=compound_name+'_'+self.extension_,
                                     values=list.list(),
                                     mitigate=True)
                       .lines())
            pass
        return ret
    pass
