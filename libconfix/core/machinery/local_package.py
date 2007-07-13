# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from setup import Setup
from package import Package
from local_node import LocalNode
from installed_package import InstalledPackage
from edgefinder import EdgeFinder
from filebuilder import FileBuilder
from require import Require
from resolve_error import NotResolved
import readonly_prefixes

from libconfix.core.digraph import algorithm
from libconfix.core.digraph import toposort
from libconfix.core.automake import repo_automake
from libconfix.core.automake.auxdir import AutoconfAuxDirBuilder
from libconfix.core.automake.configure_ac import Configure_ac 
from libconfix.core.automake.acinclude_m4 import ACInclude_m4 
from libconfix.core.digraph.digraph import DirectedGraph
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File, FileState
from libconfix.core.repo.package_file import PackageFile
from libconfix.core.utils import const
from libconfix.core.utils.error import Error
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.hierarchy.confix2_dir import Confix2_dir
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder

import os
import types

class LocalPackage(Package):

    class InfiniteLoopError(Error):
        def __init__(self):
            Error.__init__(self,
                           'Enlarge-loop entered for a ridiculously large number of times '
                           '(some Builder must be misbehaving)')
            pass
        pass

    def __init__(self, rootdirectory, setups):
        self.__name = None
        self.__version = None
        self.__rootdirectory = rootdirectory

        self.__setups = setups

        self.__current_digraph = None

        # the (contents of) configure.ac and acinclude.m4 we will be
        # writing
        self.__configure_ac = Configure_ac()
        self.__acinclude_m4 = ACInclude_m4()

        # read package definition file
        pkgdeffile = self.__rootdirectory.find([const.CONFIX2_PKG])
        if pkgdeffile is None:
            raise Error(const.CONFIX2_PKG+' missing in '+os.sep.join(self.__rootdirectory.abspath()))
        InterfaceExecutor(iface_pieces=[PackageInterfaceProxy(object=self)]).execute_file(pkgdeffile)
        if self.__name is None:
            raise Error(const.CONFIX2_PKG+': package name has not been set')
        if self.__version is None:
            raise Error(const.CONFIX2_PKG+': package version has not been set')

        try:
            # create our root builder, but only if we have a
            # Confix2.dir file. (hmm: I don't believe that we should
            # absolutely insist in having Confix2.dir - the mere fact
            # that this is the root directory of the package should
            # suffice.)
            confix2_dir_file = rootdirectory.get(const.CONFIX2_DIR)
            if confix2_dir_file is None:
                raise Error(const.CONFIX2_DIR+' missing in '+os.sep.join(rootdirectory.abspath()))
            if not isinstance(confix2_dir_file, File):
                raise Error(os.sep.join(confix2_dir_file.abspath())+' is not a file')
            self.__rootbuilder = DirectoryBuilder(directory=rootdirectory)
            self.__rootbuilder.add_builder(Confix2_dir(file=confix2_dir_file))
        except Error, e:
            raise Error('Cannot initialize package in '+'/'.join(rootdirectory.abspath()), [e])

        # setup our autoconf auxiliary directory. this a regular
        # builder by itself, but plays a special role for us because
        # we use it to put, well, auxiliary files in.
        dir = self.__rootdirectory.find([const.AUXDIR])
        if dir is None:
            dir = Directory()
            self.__rootdirectory.add(name=const.AUXDIR, entry=dir)
            pass
        self.__auxdir = AutoconfAuxDirBuilder(directory=dir)
        self.__rootbuilder.add_builder(self.__auxdir)

        # now's the time to make everyone aware that we're no fun
        # anymore.
        self.__rootbuilder.initialize(package=self)

        pass

    def __str__(self):
        return 'LocalPackage:'+str(self.__name)
    
    def name(self):
        return self.__name
    def set_name(self, name):
        assert self.__name is None
        self.__name = name
        pass
    def version(self):
        return self.__version
    def set_version(self, version):
        assert self.__version is None
        self.__version = version
        pass

    def rootdirectory(self):
        return self.__rootdirectory

    def setups(self):
        return self.__setups
    def add_setup(self, s):
        self.__setups.append(s)
        pass
    def set_setups(self, ss):
        self.__setups = ss[:]
        pass
    def get_initial_builders(self):
        """
        Called by DirectoryBuilder objects that are just being
        initialized, to get initial builders and interface proxies.
        """
        ret = []
        for s in self.__setups:
            ret.extend(s.initial_builders())
            pass
        return ret

    def configure_ac(self):
        return self.__configure_ac
    def acinclude_m4(self):
        return self.__acinclude_m4

    def rootbuilder(self):
        return self.__rootbuilder

    def digraph(self):
        return self.__current_digraph

    def boil(self, external_nodes):
        builders = self.__collect_builders()

        nodes = set()
        depinfo_per_node = {}

        while True:
            something_new = False
            
            # Enlarge builders so long as changes occur. If changes have
            # occurred, remember that.

            loop_count = 0
            while True:
                loop_count += 1
                if loop_count > 1000:
                    raise self.InfiniteLoopError()

                prev_force_enlarge_count = 0
                for b in builders:
                    prev_force_enlarge_count += b.force_enlarge_count()
                    pass                    

                # doit baby!
                # ----------
                for b in builders:
                    b.enlarge()
                    pass
                    
                # re-collect our builders. continue enlarging if
                # somebody forces us to without necessarily
                # contributing anything meaningful, of if we have new
                # builders.
                prev_builders = builders
                builders = self.__collect_builders()

                cur_force_enlarge_count = 0
                for b in builders:
                    cur_force_enlarge_count += b.force_enlarge_count()
                    pass
                if prev_force_enlarge_count < cur_force_enlarge_count:
                    continue
                
                if self.__equal_builders(prev_builders, builders):
                    builders = prev_builders
                    break

                something_new = True
                pass

            # re-collect current nodes and sort their dependency info
            # by the node's responsible builders.
            prev_nodes = nodes
            nodes = set()
            for b in builders:
                if isinstance(b, LocalNode):
                    if b not in prev_nodes:
                        something_new = True
                        pass
                    nodes.add(b)
                    # empty cache from previous run.
                    b.recollect_dependency_info()
                    pass
                pass

            # if the nodes themselves haven't changed, their
            # dependency information might have.
            if not something_new:
                for n in nodes:
                    if n.node_dependency_info_changed():
                        something_new = True
                        break
                    pass
                pass

            # still nothing new. see if everybody is happy.
            if not something_new:
                if self.__edgefinder is not None:
                    self.__edgefinder.raise_unresolved()
                    pass
                return

            # something seems to be new. go calculate the dependency
            # graph.
            all_nodes = nodes.union(set(external_nodes))
            self.__edgefinder = EdgeFinder(nodes=all_nodes)
            self.__current_digraph = DirectedGraph(
                nodes=all_nodes,
                edgefinder=self.__edgefinder)

            # let the nodes communicate with each other.
            for n in nodes:
                n.node_relate_managed_builders(digraph=self.__current_digraph)
                pass

            pass
        pass

    def output(self):

        # distribute the package configuration file
        self.__rootbuilder.makefile_am().add_extra_dist(const.CONFIX2_PKG)

        # we will be writing two files in the package's root
        # directory. configure.ac is our responsbility - we will have
        # to create it etc.. the other file, Makefile.am, is not our
        # responsbility, but that of our rootbuilder; we only use it
        # to put our stuff in (SUBDIRS, for example).

        self.output_stock_autoconf_()
        self.output_options_()
        self.output_subdirs_()
        self.output_repo_()
        self.output_unique_file_()

        # recursively write the package's output
        self.__rootbuilder.output()

        # write my configure.ac and acinclude.m4
        
        configure_ac = self.__rootdirectory.find(['configure.ac'])
        if configure_ac is None:
            configure_ac = self.__rootdirectory.add(name='configure.ac', entry=File())
        else:
            configure_ac.truncate()
            pass
        configure_ac.add_lines(self.__configure_ac.lines())

        acinclude_m4 = self.__rootdirectory.find(['acinclude.m4'])
        if acinclude_m4 is None:
            acinclude_m4 = self.__rootdirectory.add(name='acinclude.m4', entry=File())
        else:
            acinclude_m4.truncate()
            pass
        acinclude_m4.add_lines(self.__acinclude_m4.lines())
        pass

    def install(self):
        installed_nodes = []
        for b in self.__collect_builders():
            if isinstance(b, LocalNode):
                installed_nodes.append(b.install())
                pass
            pass
        return InstalledPackage(
            name=self.name(),
            version=self.version(),
            nodes=installed_nodes)
    
    def output_stock_autoconf_(self):
        self.__configure_ac.set_packagename(self.name())
        self.__configure_ac.set_packageversion(self.version())

        # we require autoconf 2.52 because it has (possibly among
        # others) AC_HELP_STRING(), and can go into subsubdirs from
        # the toplevel.

        self.__configure_ac.set_minimum_autoconf_version('2.52')

        # we never pass AC_DEFINE'd macros on the commandline

        self.__configure_ac.add_ac_config_headers('config.h')
        pass

    def output_options_(self):
        # our minimum required automake version is 1.9 
        self.__rootbuilder.makefile_am().add_automake_options('1.9')

        # enable dist'ing in the following formats
        self.__rootbuilder.makefile_am().add_automake_options('dist-bzip2')
        self.__rootbuilder.makefile_am().add_automake_options('dist-shar')
        self.__rootbuilder.makefile_am().add_automake_options('dist-zip')

        # the ubiquitous readonly-prefixes: add the configure option
        # and stuff.
        self.__configure_ac.add_paragraph(
            paragraph=readonly_prefixes.commandline_option_paragraph,
            order=Configure_ac.OPTIONS)
        pass

    def output_subdirs_(self):

        # there is mention of our subdirectories in both the toplevel
        # Makefile.am and configure.ac.

        # arrange to compose the SUBDIRS variable of the package root
        # directory ('.') and all the other directories in the
        # package.
        
        # SUBDIRS has to be topologically correct. sort out all nodes
        # that correspond to subdirectories of the package. from the
        # global digraph, make a subgraph with those nodes. compute
        # the topological order, and from that list, generate the
        # output.

        subdir_nodes = set()
        for b in self.__collect_builders():
            if isinstance(b, LocalNode):
                assert isinstance(b, DirectoryBuilder)
                subdir_nodes.add(b)
                pass
            pass

        graph = algorithm.subgraph(digraph=self.__current_digraph,
                                   nodes=subdir_nodes)
        
        for dirnode in toposort.toposort(digraph=graph, nodes=subdir_nodes):
            assert isinstance(dirnode, DirectoryBuilder)
            relpath = dirnode.directory().relpath(self.__rootdirectory)
            if len(relpath):
                dirstr = '/'.join(relpath)
            else:
                dirstr = '.'
                pass
            self.__rootbuilder.makefile_am().add_subdir(dirstr)
            self.configure_ac().add_ac_config_files('/'.join([dirstr, 'Makefile']))
            pass

        pass

    def output_repo_(self):
        # write package description file. add stuff to Makefile.am
        # that takes care to install it. put it into the dist-package.

        repofilename = self.name() + '.repo'
        repofile = self.__rootdirectory.find([repofilename])
        if repofile is None:
            repofile = self.__rootdirectory.add(name=repofilename, entry=File())
        else:
            repofile.truncate()
            pass

        PackageFile(file=repofile).dump(package=self.install())

        self.__rootbuilder.makefile_am().define_install_directory(
            symbolicname='confixrepo',
            dirname=repo_automake.dir_for_automake())
        self.__rootbuilder.makefile_am().add_to_install_directory(
            symbolicname='confixrepo',
            family='DATA',
            files=[repofilename])
        self.__rootbuilder.makefile_am().add_extra_dist(
            name=repofilename)
        
        pass

    def output_unique_file_(self):
        
        # AC_CONFIG_SRCDIR (for paranoia and sanity checks): we need
        # one unique file in the tree, as a meaningful argument to
        # AC_CONFIG_SRCDIR.

        goodfile = notsogoodfile = None
        for b in self.__collect_builders():
            if not isinstance(b, FileBuilder):
                continue
            if b.file().state() == FileState.VIRTUAL:
                continue
            goodfile = None
            notsogoodfile = None
            if b.file().name() in [const.CONFIX2_PKG, const.CONFIX2_DIR]:
                notsogoodfile = b.file()
            else:
                goodfile = b.file()
                break
            pass
        if goodfile:
            unique_file = goodfile
        elif notsogoodfile:
            unique_file = notsogoodfile
        else:
            raise Error('Not even one file handled by any submodule of '
                        'package '+self.name()+"; "
                        "probably the current working directory "
                        "("+os.getcwd()+") is not "
                        "the package root directory?")

        self.__configure_ac.set_unique_file_in_srcdir('/'.join(unique_file.relpath(self.__rootdirectory)))
        pass

    def __collect_builders(self):
        builders = []
        self.__collect_builders_recursive(self.__rootbuilder, builders)
        return builders

    def __collect_builders_recursive(self, builder, found):
        assert isinstance(found, list)
        found.append(builder)
        if isinstance(builder, DirectoryBuilder):
            for b in builder.builders():
                self.__collect_builders_recursive(b, found)
                pass
            pass
        pass

    def __equal_builders(self, lhs_builders, rhs_builders):
        assert type(lhs_builders) is type(rhs_builders) is list
        if len(lhs_builders) != len(rhs_builders):
            return False
        # out of luck: have to compare element-wise
        lookup = set(lhs_builders)
        for b in rhs_builders:
            if b not in lookup:
                return False
            pass
        return True
    pass

class PackageInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object=object)

        self.add_global('PACKAGE_NAME', getattr(self, 'PACKAGE_NAME'))
        self.add_global('PACKAGE_VERSION', getattr(self, 'PACKAGE_VERSION'))
        self.add_global('ADD_SETUP', getattr(self, 'ADD_SETUP'))
        self.add_global('SETUPS', getattr(self, 'SETUPS'))
        
        pass

    def PACKAGE_NAME(self, name):
        if type(name) is not types.StringType:
            raise Error('PACKAGE_NAME(): argument must be a string')
        self.object().set_name(name)
        pass

    def PACKAGE_VERSION(self, version):
        if type(version) is not types.StringType:
            raise Error('PACKAGE_VERSION(): argument must be a string')
        self.object().set_version(version)
        pass

    def ADD_SETUP(self, setup):
        if not isinstance(setup, Setup):
            raise Error('ADD_SETUP(): argument must be a Setup object')
        self.object().add_setup(setup)
        pass

    def SETUPS(self, setups):
        if type(setups) not in [types.ListType, types.TupleType]:
            raise Error('SETUPS(): parameter must by a list')
        for s in setups:
            if not isinstance(s, Setup):
                raise Error('SETUPS(): all list members must be Setup objects')
            pass
        self.object().set_setups(setups)
        pass
        
    pass
