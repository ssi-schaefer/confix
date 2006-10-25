# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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
import types

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

from setup import Setup
from builder import BuilderSet
from package import Package
from local_node import LocalNode
from installed_package import InstalledPackage
from edgefinder import EdgeFinder
from filebuilder import FileBuilder
import readonly_prefixes

class LocalPackage(Package):

    def __init__(self, rootdirectory, setups):
        self.name_ = None
        self.version_ = None
        self.rootdirectory_ = rootdirectory

        self.setups_ = setups

        self.digraph_ = None
        self.local_nodes_ = None

        # the (contents of) configure.ac and acinclude.m4 we will be
        # writing
        self.configure_ac_ = Configure_ac()
        self.acinclude_m4_ = ACInclude_m4()

        # read package definition file
        pkgdeffile = self.rootdirectory_.find([const.CONFIX2_PKG])
        if pkgdeffile is None:
            raise Error(const.CONFIX2_PKG+' missing in '+os.sep.join(self.rootdirectory_.abspath()))
        InterfaceExecutor(iface_pieces=[PackageInterfaceProxy(package=self)]).execute_file(pkgdeffile)
        if self.name_ is None:
            raise Error(const.CONFIX2_PKG+': package name has not been set')
        if self.version_ is None:
            raise Error(const.CONFIX2_PKG+': package version has not been set')

        # setup rootbuilder.
        self.rootbuilder_ = DirectoryBuilder(directory=rootdirectory)
        self.rootbuilder_.set_owners(parentbuilder=None, package=self)
        
        # slurp in Confix2.dir which will act as the rootbuilder's
        # configurator object. the setup objects will be asked to
        # contribute to the configurator object's interface.
        try:
            confix2_dir_file = rootdirectory.get(const.CONFIX2_DIR)
            if confix2_dir_file is None:
                raise Error(const.CONFIX2_DIR+' missing in '+os.sep.join(rootdirectory.abspath()))
            if not isinstance(confix2_dir_file, File):
                raise Error(os.sep.join(confix2_dir_file.abspath())+' is not a file')
            confix2_dir = Confix2_dir(file=confix2_dir_file)
            self.rootbuilder_.set_configurator(confix2_dir)
        except Error, e:
            raise Error('Cannot initialize package in '+'/'.join(rootdirectory.abspath()), [e])

        # setup our autoconf auxiliary directory. this a regular
        # builder by itself, but plays a special role for us because
        # we use it to put, well, auxiliary files in.
        dir = self.rootdirectory_.find([const.AUXDIR])
        if dir is None:
            dir = Directory()
            self.rootdirectory_.add(name=const.AUXDIR, entry=dir)
            pass
        self.auxdir_ = AutoconfAuxDirBuilder(directory=dir)
        self.rootbuilder_.add_builder(self.auxdir_)

        # setup the rootbuilder and auxdir. be careful to use
        # self.setups_ instead of the __init__ parameter setups -- the
        # config file may have changed it under the hood.
        for dir in [self.rootbuilder_, self.auxdir_]:
            for setup in self.setups_:
                setup.setup_directory(directory_builder=dir)
                pass
            pass
        
        pass

    def __str__(self):
        return 'LocalPackage:'+str(self.name_)
    
    def name(self):
        return self.name_
    def version(self):
        return self.version_

    def rootdirectory(self):
        return self.rootdirectory_

    def setups(self):
        return self.setups_

    def configure_ac(self):
        return self.configure_ac_
    def acinclude_m4(self):
        return self.acinclude_m4_

    def rootbuilder(self):
        return self.rootbuilder_

    def digraph(self):
        return self.current_digraph_

    def boil(self, external_nodes):
        builders = self.__collect_builders()
        nodes = set()
        depinfo_per_node = {}

        # remember those builders who have already been configure()d.
        builders_where_configure_has_been_called = set()

        while True:
            something_new = False
            
            # Enlarge builders so long as changes occur. If changes have
            # occurred, remember that.

            loop_count = 0
            while True:
                loop_count += 1
                if loop_count > 1000:
                    raise Error('Enlarge-loop entered for a ridiculously large number of times '
                                '(some Builder must be misbehaving)')

                # before we can do anything meaningful with a builder,
                # we must configure it (but only once)
                for b in builders:
                    if b in builders_where_configure_has_been_called:
                        continue
                    b.configure()
                    builders_where_configure_has_been_called.add(b)
                    pass
                for b in builders:
                    b.enlarge()
                    pass

                # re-collect our builders, and see if anything has
                # changed in the current run.
                prev_builders = builders
                builders = self.__collect_builders()
                if prev_builders.is_equal(builders):
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

            if not something_new:
                return

            # something seems to be new. go calculate the dependency
            # graph.
            all_nodes = nodes.union(set(external_nodes))
            self.current_digraph_ = DirectedGraph(nodes=all_nodes, edgefinder=EdgeFinder(all_nodes))

            # let the nodes communicate with each other.
            for n in nodes:
                n.node_relate_managed_builders(digraph=self.current_digraph_)
                pass

            pass
        pass

    def output(self):

        # distribute the package configuration file
        self.rootbuilder_.makefile_am().add_extra_dist(const.CONFIX2_PKG)

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
        self.rootbuilder_.output()

        # write my configure.ac and acinclude.m4
        
        configure_ac = self.rootdirectory_.find(['configure.ac'])
        if configure_ac is None:
            configure_ac = self.rootdirectory_.add(name='configure.ac', entry=File())
        else:
            configure_ac.truncate()
            pass
        configure_ac.add_lines(self.configure_ac_.lines())

        acinclude_m4 = self.rootdirectory_.find(['acinclude.m4'])
        if acinclude_m4 is None:
            acinclude_m4 = self.rootdirectory_.add(name='acinclude.m4', entry=File())
        else:
            acinclude_m4.truncate()
            pass
        acinclude_m4.add_lines(self.acinclude_m4_.lines())
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
        self.configure_ac_.set_packagename(self.name())
        self.configure_ac_.set_packageversion(self.version())

        # we require autoconf 2.52 because it has (possibly among
        # others) AC_HELP_STRING(), and can go into subsubdirs from
        # the toplevel.

        self.configure_ac_.set_minimum_autoconf_version('2.52')

        # we never pass AC_DEFINE'd macros on the commandline

        self.configure_ac_.add_ac_config_headers('config.h')
        pass

    def output_options_(self):
        # our minimum required automake version is 1.9 
        self.rootbuilder_.makefile_am().add_automake_options('1.9')

        # enable dist'ing in the following formats
        self.rootbuilder_.makefile_am().add_automake_options('dist-bzip2')
        self.rootbuilder_.makefile_am().add_automake_options('dist-shar')
        self.rootbuilder_.makefile_am().add_automake_options('dist-zip')

        # the ubiquitous readonly-prefixes: add the configure option
        # and stuff.
        self.configure_ac_.add_paragraph(
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

        graph = algorithm.subgraph(digraph=self.current_digraph_,
                                   nodes=subdir_nodes)
        
        for dirnode in toposort.toposort(digraph=graph, nodes=subdir_nodes):
            assert isinstance(dirnode, DirectoryBuilder)
            relpath = dirnode.directory().relpath(self.rootdirectory_)
            if len(relpath):
                dirstr = '/'.join(relpath)
            else:
                dirstr = '.'
                pass
            self.rootbuilder_.makefile_am().add_subdir(dirstr)
            self.configure_ac().add_ac_config_files('/'.join([dirstr, 'Makefile']))
            pass

        pass

    def output_repo_(self):
        # write package description file. add stuff to Makefile.am
        # that takes care to install it. put it into the dist-package.

        repofilename = self.name() + '.repo'
        repofile = self.rootdirectory_.find([repofilename])
        if repofile is None:
            repofile = self.rootdirectory_.add(name=repofilename, entry=File())
        else:
            repofile.truncate()
            pass

        PackageFile(file=repofile).dump(package=self.install())

        self.rootbuilder_.makefile_am().define_install_directory(
            symbolicname='confixrepo',
            dirname=repo_automake.dir_for_automake())
        self.rootbuilder_.makefile_am().add_to_install_directory(
            symbolicname='confixrepo',
            family='DATA',
            files=[repofilename])
        self.rootbuilder_.makefile_am().add_extra_dist(
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

        self.configure_ac_.set_unique_file_in_srcdir('/'.join(unique_file.relpath(self.rootdirectory_)))
        pass

    def __collect_builders(self):
        builders = BuilderSet()
        self.__collect_builders_recursive(self.rootbuilder_, builders)
        return builders

    def __collect_builders_recursive(self, builder, found):
        found.add(builder)
        if isinstance(builder, DirectoryBuilder):
            for b in builder.builders():
                self.__collect_builders_recursive(b, found)
                pass
            pass
        pass

    pass

class PackageDefinition:
    def __init__(self):
        self.name_ = None
        self.version_ = None
        pass
    def set_name(self, name):
        self.name_ = name
        pass
    def set_version(self, version):
        self.version_ = version
        pass
    def name(self):
        return self.name_
    def version(self):
        return self.version_
    pass

class PackageInterfaceProxy(InterfaceProxy):
    def __init__(self, package):
        InterfaceProxy.__init__(self)

        self.package_ = package

        self.add_global('PACKAGE_NAME', getattr(self, 'PACKAGE_NAME'))
        self.add_global('PACKAGE_VERSION', getattr(self, 'PACKAGE_VERSION'))
        self.add_global('ADD_SETUP', getattr(self, 'ADD_SETUP'))
        self.add_global('SETUPS', getattr(self, 'SETUPS'))
        
        pass

    def PACKAGE_NAME(self, name):
        if type(name) is not types.StringType:
            raise Error('PACKAGE_NAME(): argument must be a string')
        self.package_.name_ = name
        pass

    def PACKAGE_VERSION(self, version):
        if type(version) is not types.StringType:
            raise Error('PACKAGE_VERSION(): argument must be a string')
        self.package_.version_ = version
        pass

    def ADD_SETUP(self, setup):
        if not isinstance(setup, Setup):
            raise Error('ADD_SETUP(): argument must be a Setup object')
        self.package_.setups_.append(setup)
        pass

    def SETUPS(self, setups):
        if type(setups) not in [types.ListType, types.TupleType]:
            raise Error('SETUPS(): parameter must by a list')
        for s in setups:
            if not isinstance(s, Setup):
                raise Error('SETUPS(): all list members must be Setup objects')
            pass
        self.package_.setups_ = setups
        pass
        
    pass
