# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2010 Joerg Faschingbauer

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

from .setup import Setup
from .setup import CompositeSetup
from .package import Package
from .installed_package import InstalledPackage
from .edgefinder import EdgeFinder
from .filebuilder import FileBuilder
from .require import Require
from .resolve_error import NotResolved
from .interface import InterfaceProxy
from .interface import InterfaceExecutor
from .repo import PackageFile

from libconfix.core.digraph import algorithm
from libconfix.core.digraph import toposort
from libconfix.core.digraph.digraph import DirectedGraph
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.utils import const
from libconfix.core.utils.error import Error
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

        self.__setup = None

        if setups:
            self.__set_setup(setups)
            pass

        self.__current_digraph = None

        # our directory builders, sorted topologically for output by
        # our backends.
        self.__topo_directories = None

        # read package definition file
        pkgdeffile = self.__rootdirectory.find([const.CONFIX2_PKG])
        if pkgdeffile is None:
            raise Error(const.CONFIX2_PKG+' missing in '+os.sep.join(self.__rootdirectory.abspath()))
        InterfaceExecutor(iface_pieces=[PackageInterfaceProxy(package=self)]).execute_file(pkgdeffile)
        if self.__name is None:
            raise Error(const.CONFIX2_PKG+': package name has not been set')
        if self.__version is None:
            raise Error(const.CONFIX2_PKG+': package version has not been set')

        if self.__setup is None:
            raise Error('No setup has been given; use SETUP() in Confix2.pkg')

        # create our root builder
        self.__rootbuilder = DirectoryBuilder(directory=rootdirectory)

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

    def setup(self):
        return self.__setup
    def set_setup(self, s):
        self.__set_setup(s)
        pass

    def rootbuilder(self):
        return self.__rootbuilder

    def topo_directories(self):
        """
        Returns a toplogically sorted list of directory builder
        objects. Valid only during the output phase, once dependency
        calculation is complete.
        """
        assert self.__topo_directories is not None
        return self.__topo_directories

    def repofilename(self):
        """
        The name of the package's repo file.
        """
        return self.name() + '.repo'

    def digraph(self):
        return self.__current_digraph

    def boil(self, external_nodes):
        """
        Resolve everything we got, propagate build information
        backwards across the edges.

        external_nodes is an iterable of repo nodes.
        """
        loop_count = 0

        while True:
            loop_count += 1
            if loop_count > 1000:
                raise self.InfiniteLoopError()

            something_changed = self.__do_enlarge()
            if something_changed:
                continue

            do_next_round = False

            directory_builders = []
            for b in self.iter_builders():
                if not isinstance(b, DirectoryBuilder):
                    continue
                directory_builders.append(b)
                b.recollect_dependency_info()
                if b.node_dependency_info_changed():
                    do_next_round = True
                    pass
                pass

            if do_next_round:
                self.__current_digraph = None
                continue

            if self.__current_digraph:
                break

            all_nodes = directory_builders + list(external_nodes)
            self.__current_digraph = DirectedGraph(
                nodes=all_nodes,
                edgefinder=EdgeFinder(nodes=all_nodes))

            for n in directory_builders:
                n.node_relate_managed_builders(digraph=self.__current_digraph)
                pass

            pass

        self.__current_digraph.edgefinder().raise_unresolved()
        pass

    def output(self):
        self.__topo_directories = self.__sort_subdirs()

        # generate the package's repo file.
        repofilename = self.repofilename()
        repofile = self.__rootdirectory.find([repofilename])
        if repofile is None:
            repofile = self.__rootdirectory.add(name=repofilename, entry=File())
        else:
            repofile.truncate()
            pass

        PackageFile(file=repofile).dump(package=self.install())

        # recursively write the package's output
        self.__rootbuilder.output()
 
        pass

    def install(self):
        installed_nodes = []
        for b in self.iter_builders():
            if isinstance(b, DirectoryBuilder):
                installed_nodes.append(b.install())
                pass
            pass
        return InstalledPackage(
            name=self.name(),
            version=self.version(),
            nodes=installed_nodes)

    def iter_builders(self):
        """
        Returns an iterator over all builder objects that are
        maintained by this package. Use it when you do not intend to
        modify the set of builders when iterating.
        """
        yield self.__rootbuilder
        for builder in self.__rootbuilder.iter_builders_recursive():
            yield builder
            pass
        pass

    def __do_enlarge(self):
        """
        Enlarge our current set of builders by calling
        Builder.enlarge() on each.

        @return True if something has changed, False otherwise.
        """

        # copy them out because we will be changing the set once we
        # call enlarge on each builder.
        builders = [b for b in self.iter_builders()]

        prev_builder_props = {}
        for b in builders:
            prev_builder_props[b] = b.force_enlarge_count()
            pass

        for b in builders:
            try:
                b.enlarge()
            except Error as e:
                raise Error("Builder "+b.shortname()+" of "+b.parentbuilder().shortname()+" encountered an error", [e])
            pass

        for b in self.iter_builders():
            prev_enlarge_count = prev_builder_props.get(b)
            if prev_enlarge_count is None:
                # this is a new builder
                return True
            if prev_enlarge_count < b.force_enlarge_count():
                # b forced repetition
                return True
            pass

        return False

    def __sort_subdirs(self):
        # sort subdirectories topologically for our backends.
        subdir_nodes = set()
        for b in self.iter_builders():
            if isinstance(b, DirectoryBuilder):
                subdir_nodes.add(b)
                pass
            pass
        graph = algorithm.subgraph(digraph=self.__current_digraph,
                                   nodes=subdir_nodes)
        return toposort.toposort(digraph=graph, nodes=subdir_nodes)

    def __set_setup(self, s):
        assert self.__setup is None
        if isinstance(s, Setup):
            self.__setup = s
        elif type(s) in (list, tuple):
            self.__setup = CompositeSetup(s)
        else:
            assert False
            pass
        pass

    pass

class PackageInterfaceProxy(InterfaceProxy):
    def __init__(self, package):
        InterfaceProxy.__init__(self)

        self.__package = package

        self.add_global('PACKAGE_NAME', getattr(self, 'PACKAGE_NAME'))
        self.add_global('PACKAGE_VERSION', getattr(self, 'PACKAGE_VERSION'))
        self.add_global('SETUP', getattr(self, 'SETUP'))
        
        pass

    def PACKAGE_NAME(self, name):
        if type(name) is not bytes:
            raise Error('PACKAGE_NAME(): argument must be a string')
        self.__package.set_name(name)
        pass

    def PACKAGE_VERSION(self, version):
        if type(version) is not bytes:
            raise Error('PACKAGE_VERSION(): argument must be a string')
        self.__package.set_version(version)
        pass

    def SETUP(self, setup):
        if not isinstance(setup, Setup) and type(setup) not in [list, tuple]:
            raise Error('SETUP(): parameter must by a list or a Setup object')
        self.__package.set_setup(setup)
        pass
        
    pass

