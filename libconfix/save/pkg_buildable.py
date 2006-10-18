# $Id: pkg_buildable.py,v 1.32 2006/07/04 14:36:48 jfasch Exp $

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
import sys
import types
from sets import Set

import core.debug
import helper_automake
import helper_pickle
import core.helper
import const
import repo_automake
import readonly_prefixes
import helper_configure_in
from repo_composite import CompositePackageRepository
from repo_local import LocalPackageRepository
from repofile import RepositoryFile
from package import Package
from pkg_installed import InstalledPackage
from configure_in import Configure_in
from core.error import Error
from modbuild import BuildableModule
from buildable import Buildable
from modbase import ModuleBase
from digraph.digraph import DirectedGraph
from digraph.toposort import toposort
from core.edgefinder import EdgeFinder
from makefile_py import Makefile_py
from makefile_am import Makefile_am
from acinclude_m4 import ACInclude_m4
from paragraph import Paragraph
from core.depinfo import DependencyInformation
from auxdir import AutoconfAuxDir
from installer import FileInstallerFactory

class BuildablePackage(Package):

    """ An object of class Package is the entry point for
    instrumenting a source tree. Its responsibilities are,

      - Scanning the source tree.

        This involves everything which is needed to get an initial
        grasp of the package's contents.
        
          - The package's toplevel Makefile.py is read, and its content
            is assimilated.
  
          - From the package's root directory, the source tree is
            searched for directories containing a C{Makefile.py}
            file. These directories are wrapped into
            L{module<modbuild.BuildableModule>} objects and added to the
            list of modules that are managed by the package.
  
          - The L{modules<modbuild.BuildableModule>} that have been
            found are initialized. This is done by invoking their
            respective C{scan()}.
     
        Nothing is done in this step to establish relationships
        between modules.
  
      - Resolving dependencies.

        In this step a L{dependency graph<digraph.digraph.DirectedGraph>}
        is built. This graph is used later to compute a correct build
        order for the modules that are maintained by the package. The
        calculation is done repeatedly, until no more changes are
        seen. One iteration involves the following steps.

          1. The modules are told to gather dependency
             information. That is, they have to state what they
             L{require<require.Require>} and what they
             L{provide<provide.Provide>}.

          2. The requires and provides are matched against each
             other. A match makes for an edge in the L{dependency
             graph<digraph.digraph.DirectedGraph>}. See there for how the
             computation is done.

          3. Once the graph is built, a topological sort is performed
             for each of the modules that are maintained by the
             package. This yields a preliminary dependency list for
             each module.

          4. Each managed module is then supplied with build
             information.

        In step 4, a module is augmented with information. It is
        possible that this information contains things that make the
        module require things that it has not required yet when the
        current iteration began. It is equally possible that new
        things are provided by the module. If this happens, this means
        that the dependency graph must be calculated again as there
        were possible changes in the set of edges. So, the calculation
        is done in a loop until no module reports a change in its
        dependencies anymore.
    
      - Output

        Write the toplevel C{Makefile.am}, C{configure.in}, and
        C{acinclude.m4} files. Tell every managed module to write its
        own C{Makefile.am} file.

        """

    def __init__(self,
                 confix_scriptdir,
                 dir,
                 use_bulk_install,
                 use_kde_hack,
                 print_timings,
                 name = None,
                 version = None,
                 use_libtool = False,
                 global_requires = []):

        """ Create a new package in the given directory, scanning the
        directory tree for potential modules. Build {modules
        <ModuleBase>} where appropriate.

        @type  dir: string
        @param dir: The directory to use as the root of the package source tree.

        @type  name: string
        @param name: The name to use for the package, if it is not
          None. Otherwise confix uses the name found on the command
          line, or from the root source directory's Makefile.py.

        @type  version: string
        @param version: The version to use for the package, if it is
          not None. Otherwise confix uses the name found on the
          command line, or from the root source directory's
          Makefile.py. If neither of these are defined, then confix
          uses version '0.0.0'.

        @type  use_libtool: int
        @param use_libtool: A boolean flag that decides whether we
        will be generating output that uses libtool or not.

        @type global_requires: list of Require
        @param global_requires: A list of Require objects which will
        be added to every module managed by the package.

        """

        Package.__init__(self, name=name, version=version)

        self.dir_ = dir
        assert(os.path.isabs(dir))

        self.use_libtool_ = use_libtool
        self.global_requires_ = global_requires[:]

        # package repository where I find packages that contain
        # modules, which finally are the basis of depgraph
        # calculation.

        self.repository_ = None

        # we don't have no depgraph yet. we will build one when we are
        # asked for it.

        self.depgraph_ = None

        # configure.in, acinclude.m4, Makefile.am

        self.configure_in_ = Configure_in()
        self.acinclude_m4_ = ACInclude_m4()
        self.makefile_am_ = Makefile_am('.')

        # create a directory for our auxiliary files (we don't put
        # them in the package root).
        
        self.auxdir_ = AutoconfAuxDir(parentdir=self.dir_, relpath='confix-admin')

        # if we are using the famous KDE configure patching hack
        # (replace ~1 Billion parallel sed instances with one singe
        # perl call), we have to populate the auxdir with the KDE
        # auxiliary scripts.

        if use_kde_hack:
            self.auxdir_.eat_file(sourcename=os.path.join(confix_scriptdir, 'conf.change.pl'),
                                  mode=0755)
            self.auxdir_.eat_file(sourcename=os.path.join(confix_scriptdir, 'config.pl'),
                                  mode=0755)
            pass
        
        # setup file installer factory. this will be passed to every
        # module and will be used by these to create file installer
        # objects.

        self.file_installer_factory_ = FileInstallerFactory(
            configure_in=self.configure_in_,
            auxdir=self.auxdir_,
            source_auxdir=confix_scriptdir,
            use_bulk_install=use_bulk_install)

        # the module object that maintains the toplevel directory. it
        # is None from the beginning, and will be allocated and filled
        # with meaningful stuff in scan()

        # share my Makefile.am writer object with my toplevel module
        # (I am still the owner and responsible for writing that
        # file).

        self.toplevel_module_ = BuildableModule(
            # we do not know our name yet - we have to evaluate
            # Makefile.py first.
            packagename=None,
            
            localname=[],
            dir='.',
            use_libtool=self.use_libtool_,
            makefile_am=self.makefile_am(),
            write_makefile_am=False,
            file_installer_factory=self.file_installer_factory_)

        makefile_py = Makefile_py(dir='.', package=self, module=self.toplevel_module_)
        makefile_py.execute()

        if self.name() is None:
            raise Error('the package name has not been set. '
                        'Use --packagename, or (preferred) '
                        'PACKAGE_NAME() in the toplevel Makefile.py.')

        if self.version() is None:
            debug.warn('the package version has not been set; '
                       'setting it to 0.0.0. '
                       'Use --packageversion, or (preferred) '
                       'PACKAGE_VERSION() in the toplevel Makefile.py.')
            self.set_version_('0.0.0')
            pass

        self.toplevel_module_.set_packagename(self.name())

        pass

        pass

    def depgraph(self):
        return self.depgraph_

    def modules(self):

        """ Implementation of the abstract (sigh - wish I had a true
        language) base class method. Returns the toplevel module and,
        recursively, all of its descendant modules. """

        assert self.toplevel_module_ is not None
        return [self.toplevel_module_] + self.toplevel_module_.recursive_submodules()
        
    def makefile_py_set_name(self, name):

        """ Called when the package's Makefile.py calls
        PACKAGE_NAME(). Takes care of percedence. """

        if self.name() is None:
            self.set_name_(name)
        else:
            core.debug.warn('PACKAGE_NAME(): not setting name to "'+name+'" '
                       'because it is already set to "'+self.name()+'"')

    def makefile_py_set_version(self, version):

        """ Called when the package's Makefile.py calls
        PACKAGE_VERSION(). Takes care of percedence. """

        if self.version() is None:
            self.set_version_(version)
        else:
            core.debug.warn('PACKAGE_VERSION(): not setting version to "'+version+'" '
                       'because it is already set to "'+self.version()+'"')

    def set_repository(self, repo):

        """ Set the package repository that contains packages which in
        turn contain modules that may resolve dependencies of my
        modules.
        
        @type repo: L{repo.PackageRepository}

        @param repo: A package repository

        """

        assert self.repository_ is None
        self.repository_ = repo

    def add_configure_in(self, c):

        self.configure_in_.add_check(c)
        
    def add_acinclude_m4(self, paragraph):

        assert isinstance(paragraph, Paragraph)
        self.acinclude_m4_.add_paragraph(a)

    def makefile_am(self): return self.makefile_am_

    def scan(self):

        self.toplevel_module_.scan()
        modules = self.modules()

        # module names must not conflict with each other

        modnames = Set()
        for m in modules:
            key = '.'.join(m.localname())
            if key in modnames:
                raise Error('Package "'+self.name()+'" has two modules named "'+key+'"')
            modnames.add(key)
            pass

        # we have the concept of "global requires". these are things
        # that every module must pull in. for example, if we are
        # compiling with threading switched on, then we must compile
        # *everything* with threading switched on.

        for m in modules:
            for r in self.global_requires_:
                m.add_require(r)

        # "validate" all my submodules.

        for m in modules:
            m.validate()
            pass
        pass

    def resolve_dependencies(self):

        """ Build the L{dependency graph
        <digraph.digraph.DirectedGraph>} from this package's modules
        and the modules from the packages which are found in the
        package repository. This process involves matching one
        module's L{require <require.Require>} objects against the
        other modules L{provide <provide.Provide>} objects, and, if a
        match occured, creating an edge between them. """

        # compose a list of all modules which must be considered by
        # the dependency graph

        repo = CompositePackageRepository()
        repo.add_repo(LocalPackageRepository(self))
        repo.add_repo(self.repository_)

        depgraph_modules = []
        for p in repo.packages():
            depgraph_modules.extend(p.modules())

        # we calculate the dependency graph repeatedly, until no more
        # changes to the package's dependency information
        # occur. (every time our modules/buildables collect their
        # build info from their successors in the dependency graph,
        # they possibly add more dependency information.)

        # note that changes to the dependency information can occur
        # only additively, so one iteration cannot remove dependency
        # information.

        nth_iteration = 0

        while 1:

            nth_iteration += 1

            # give my modules a chance to extract information from all
            # the modules that can be part of the dependency graph.

            core.debug.trace(['performance'], 'WORLD')

            for m in self.modules():
                m.world(depgraph_modules)

            core.debug.trace(['depinfo'], 'Package: calculating dependency graph (iteration #'+`nth_iteration-1`+')')

            # let the modules initialize their dependency
            # information. (they are not required to have done so yet
            # because this can be costly.)

            core.debug.trace(['depinfo'], 'Package: having modules gather dependency information')

            core.debug.trace(['performance'], 'GATHER DEPINFO')

            previous_num_depinfo = 0
            for m in self.modules():
                previous_num_depinfo += m.size_of_dependency_info()
                pass

            for m in self.modules():
                m.gather_dependency_info()
                pass

            new_num_depinfo = 0
            for m in self.modules():
                new_num_depinfo += m.size_of_dependency_info()
                pass

            core.debug.trace(['depinfo'], 'Package: done with dependency information '
                        '('+str(new_num_depinfo-previous_num_depinfo)+' new objects)')

            if new_num_depinfo == previous_num_depinfo:
                core.debug.trace(['depinfo'], 'Package: no more changes in dependency information; quitting')
                break

            core.debug.trace(['depinfo'], 'Package: dependency graph #'+str(nth_iteration))

            core.debug.trace(['depinfo', 'performance'], 'Package: calculating dependency graph')
            self.depgraph_ = DirectedGraph(nodes=depgraph_modules,
                                           edgefinder=EdgeFinder(nodes=depgraph_modules))
            core.debug.trace(['depinfo', 'performance'], 'Package: done with dependency graph')

            for m in self.modules():
                m.reset_build_infos()
                pass

            core.debug.trace(['performance'], 'DO CONTRIBUTIONS')

            for m in self.modules():
                topomodules = []
                for mod in toposort(digraph=self.depgraph_, node=m):
                    if mod is not m:
                        topomodules.append(mod)
                        pass
                    pass
                m.gather_build_info(modules=topomodules)
                pass

            core.debug.trace(['performance'], 'DONE')
            pass

        # accommodate for the case where no depgraph has been built
        # because there was no dependency information at all in the
        # whole package.

        core.debug.trace(['performance'], 'DEPGRAPH 2')

        if not self.depgraph_:
            self.depgraph_ = DirectedGraph(nodes=depgraph_modules,
                                           edgefinder=EdgeFinder(nodes=depgraph_modules))

    def output(self):

        """ Create output for this package. This will create the
        configure.in and Makefile.am files in the package root
        directory, and it will tell all buildable modules in this
        package to write Makefile.am files giving build instructions
        for their targets.  """

        assert self.depgraph_

        self.makefile_am().add_extra_dist(const.MAKEFILE_PY)

        # molest everyone with auxdir.

        self.auxdir_.output(self.configure_in_)
        self.toplevel_module_.makefile_am().add_subdir(self.auxdir_.relpath())
        self.configure_in_.add_ac_config_files(os.path.join(self.auxdir_.relpath(), 'Makefile'))

        # the toplevel directory's Makefile is always the first in the
        # build because we want to jump into SUBDIRS there. this might
        # not be what the dependency graph wants.

        # check that no attempt will be made to build a submodule
        # before the toplevel module: no submodule must be in the
        # toplevel module's dependency list.

        toplevel_deplist = toposort(digraph=self.depgraph_, node=self.toplevel_module_)
        for m in self.toplevel_module_.recursive_submodules():
            if m in toplevel_deplist:
                raise Error('Toplevel module depends on module '+\
                            '.'.join(m.name())+' which is bad because '
                            'toplevel module has to be built first')

        # write package description file. add stuff to Makefile.am
        # that takes care to install it. put it into the dist-package.

        repofile = self.name() + '.repo'
        RepositoryFile(repofile).dump(self.install())

        reponame = 'confixrepo'
        self.makefile_am().add_lines(
            self.makefile_am().define_directory(symbolicname=reponame,
                                                dirname=repo_automake.dir_for_automake()))
        self.makefile_am().add_dir_primary(dir=reponame, primary='DATA', filename=repofile)

        self.makefile_am().add_extra_dist(repofile)

        # if we have modules other than our toplevel module, add their
        # respective directories to our Makefile.am's SUBDIRS
        # variable. note that we must not add the toplevel module to
        # SUBDIRS.

        # FIXME: self.depgraph_ contains not only modules local to
        # this package, but also all modules of all installed
        # packages. so, in order to determine the build order of the
        # local modules (which is our primary output: "SUBDIRS =
        # ..."), we have to sort out non-local modules in a quite
        # complicated manner. fix this and build a temporary depgraph
        # of only the local modules.

        if 1:
            
            assert self.depgraph_

            allmods = []
            buildmods_lookup = {}
            for m in self.modules():
                allmods.extend(toposort(digraph=self.depgraph_, node=m))
                buildmods_lookup[m] = 1
                pass

            have = {}
            sortedmods = []
            for m in allmods:
                if not buildmods_lookup.has_key(m): continue
                if have.has_key(m): continue
                have[m] = 1
                sortedmods.append(m)

            # fill the toplevel Makefile.am's SUBDIRS. SUBDIRS
            # contains only variables that are set conditionally
            # through automake conditionals which we also add here,
            # together with the Makefile.am code that evaluates
            # them. (goodie: kdevelop's automake import function
            # doesn't know how to deal with SUBDIRS that contain
            # variables, so we provide appropriate hints.)

            for m in sortedmods:
                if m is self.toplevel_module_: continue

                subdir_var = helper_automake.subdir_variable(m.dir())
                subdir_enabled_var = helper_automake.subdir_enabled_variable(m.dir())
                enablename = helper_automake.automake_name('.'.join(m.fullname()))
                subdir_conditional = helper_automake.subdir_conditional('.'.join(m.fullname()))

                # add the subdir's --disable argument. define automake
                # conditional.
                
                self.configure_in_.add_paragraph(
                    order=helper_configure_in.ORDER_OPTIONS,
                    paragraph=Paragraph([
                    'AC_ARG_ENABLE(',
                    '    '+enablename+',',
                    '    AC_HELP_STRING([--disable-'+enablename+']',
                    '                   [Don\'t build directory '+m.dir()+']),',
                    '    [',
                    '    case $enableval in',
                    '        no) '+subdir_enabled_var+'=false;;',
                    '        *) '+subdir_enabled_var+'=true;;',
                    '    esac',
                    '    ],',
                    '    [',
                    '   '+subdir_enabled_var+'=true',
                    '    ])',
                    'AM_CONDITIONAL('+subdir_conditional+',test x$'+subdir_enabled_var+' = xtrue)'
                    ]))

                # conditionally build the subdir. (provide kdevelop
                # hints as we go.)
                
                self.makefile_am().add_lines([
                    'if '+subdir_conditional,
                    subdir_var+' = '+m.dir(),
                    'else',
                    subdir_var+' = ',
                    'endif',
                    '#kdevelop: '+subdir_var + ' = ' + m.dir()
                    ])
                self.makefile_am().add_subdir('$('+helper_automake.subdir_variable(m.dir())+')')

                # define a feature macro that user of the subdir's
                # code may want to respect.

                fmname, fmdesc = m.get_featuremacro()
                if fmname is not None:
                    self.configure_in_.add_paragraph(
                        order=helper_configure_in.ORDER_OPTIONS+1,
                        paragraph=Paragraph([
                        'if test x${'+subdir_enabled_var+'} = xtrue; then',
                        '   AC_DEFINE('+fmname+',1,['+fmdesc+'])',
                        'fi']))

        # let the modules output their stuff, whatever that is

        for m in self.modules():
            m.output()
            pass

        # write auto{make,conf} files

        self.output_configure_in_()
        self.output_makefile_am_()
        self.output_acinclude_m4_()

    def install(self):

        """ Create an installed incarnation of myself. That
        incarnation contains

           - name

           - version

           - use_libtool: a flag that indicates if we were using
             Libtool to build the libraries (this helps us being able
             to issue warnings or errors as early as possible, for
             example when somebody mixes Libtool and non-Libtool
             packages)

           - modules """

        return InstalledPackage(
            name=self.name(),
            version=self.version(),
            modules=[m.install() for m in self.modules()])

    def output_configure_in_(self):

        """ Generate the configure.in file for the package. This
        collects all checks from constituent buildable module objects
        in the package, orders them, and writes them to the output
        configure.in file in the package's root source directory. """

        self.toplevel_checks_()
        self.module_checks_()

        self.configure_in_.output()

    def output_makefile_am_(self):
        # our minimum required automake version is 1.9 
        self.makefile_am().add_automake_option('1.9') # in confix2

        # enable dist'ing in the following formats
        self.makefile_am().add_automake_option('dist-bzip2') # in confix2
        self.makefile_am().add_automake_option('dist-shar') # in confix2
        self.makefile_am().add_automake_option('dist-zip') # in confix2

        self.makefile_am().output()

    def output_acinclude_m4_(self):

        for m in self.modules():
            self.acinclude_m4_.add_paragraphs(m.gather_acinclude_m4())
            pass
        self.acinclude_m4_.output()
        pass

    def toplevel_checks_(self):

        """ Reap checks needed at the top (package) level. """

        self.configure_in_.set_packagename(self.name()) # in confix2
        self.configure_in_.set_packageversion(self.version()) # in confix2 

        # add readonly-prefixes as part of the overall infrastructure.

        self.configure_in_.add_paragraph(
            order=helper_configure_in.ORDER_OPTIONS,
            paragraph=readonly_prefixes.commandline_option_paragraph)

        # AC_CONFIG_SRCDIR (for paranoia and sanity checks): we need
        # one unique file in the tree, as a meaningful argument to
        # AC_CONFIG_SRCDIR.

        unique_file = None
        notsogoodfile = None
        for m in self.modules():
            goodfile = None
            notsogoodfile = None
            files = m.gather_handled_files()
            for f in files:
                if f == const.MAKEFILE_PY:
                    notsogoodfile = os.path.join(m.dir(), f)
                else:
                    goodfile = os.path.join(m.dir(), f)
                    break
            assert goodfile or notsogoodfile
            if goodfile:
                unique_file = goodfile
                break
        if not unique_file:
            unique_file = notsogoodfile

        if not unique_file:
            raise Error('Not even one file handled by any submodule of '
                          'package ' + '.'.join(self.name()) + "; "
                          "probably the current working directory "
                          "("+os.getcwd()+") is not "
                          "the package root directory?")
        
        self.configure_in_.set_unique_file_in_srcdir(unique_file)

        # we require autoconf 2.52 because it has (possibly among
        # others) AC_HELP_STRING(), and can go into subsubdirs from
        # the toplevel.

        self.configure_in_.set_minimum_autoconf_version('2.52') # in confix2

        # we never pass AC_DEFINE'd macros on the commandline

        self.configure_in_.add_ac_config_headers('config.h') # in confix2

        # we let the code know if it is instrumented by confix, just
        # in case somebody wants to know.
        
        self.configure_in_.add_paragraph(
            order=helper_configure_in.ORDER_LIBRARIES,
            paragraph=Paragraph(['AC_DEFINE([USING_CONFIX], 1, [Advertise Confix usage])']))

        self.configure_in_.add_ac_config_files('Makefile')

        for m in self.modules():
            self.configure_in_.add_ac_config_files(os.path.join(m.dir(), 'Makefile'))
            pass
        pass

    def module_checks_(self):

        for m in self.modules():
            self.configure_in_.add_paragraphs(m.gather_configure_in())
            pass
        pass
