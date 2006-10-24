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

import types

from libconfix.core.digraph import reached_from
from libconfix.core.digraph.digraph import Edge, DirectedGraph
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.depindex import ProvideMap
from libconfix.core.machinery.depinfo import DependencyInformation
from libconfix.core.machinery.setup import Setup
from libconfix.core.utils.error import Error

from h import HeaderBuilder
from dependency import Provide_CInclude

class GraphInstaller(Builder):
    def __init__(self):
        Builder.__init__(self)

        # dictionary filename -> installdir
        self.entry_points_ = {}

        # remember these until it gets to write output. dict filename
        # -> installdir
        self.installed_files_ = {}

        pass

    def installpath_of_headerfile(self, filename):
        return self.installed_files_.get(filename)

    def add_entry_point(self, filename, dir):
        assert type(dir) in [types.ListType]

        if self.entry_points_.has_key(filename):
            raise Error('Duplicate entry point: '+filename)

        self.entry_points_[filename] = dir
        pass

    def dependency_info(self):
        ret = DependencyInformation()

        # clear output information
        self.installed_files_ = {}

        # let base class do its job
        ret.add(super(GraphInstaller, self).dependency_info())

        # first pass: index header files
        header_index = ProvideMap(permissive=False)
        for b in self.parentbuilder().builders():
            if not isinstance(b, HeaderBuilder):
                continue
            header_index.add(provide=Provide_CInclude(filename=b.file().name()),
                             node=b)
            pass

        # second pass: find edges, build graph
        edges = []
        nodes = []
        for b in self.parentbuilder().builders():
            if not isinstance(b, HeaderBuilder):
                continue
            nodes.append(b)
            for r in b.dependency_info().requires():
                matching_builder = header_index.find_match(require=r)
                assert len(matching_builder) <= 1
                if len(matching_builder) == 1:
                    edges.append(Edge(tail=b, head=matching_builder[0]))
                    pass
                pass
            pass
        headergraph = DirectedGraph(nodes=nodes, edges=edges)

        # handle our subgraph nodes
        for filename, installdir in self.entry_points_.iteritems():
            entry_node = None
            for b in headergraph.nodes():
                if b.file().name() == filename:
                    entry_node = b
                    break
                pass
            else:
                raise Error('Entry point '+filename+' not found')

            subgraph = reached_from.reached_from(digraph=headergraph, entrypoints=[entry_node])

            for header in subgraph.nodes():
                self.installed_files_[header.file().name()] = installdir
                ret.add_internal_provide(Provide_CInclude(header.file().name()))
                ret.add_provide(Provide_CInclude('/'.join(installdir+[header.file().name()])))
                pass
            pass

        return ret

    def output(self):
        super(graphinstaller, self).output()
        for filename, installdir in self.installed_files_.iteritems():
            self.parentbuilder().file_installer().add_public_header(filename=filename, dir=installdir)
            self.parentbuilder().file_installer().add_private_header(filename=filename, dir=installdir)
            pass
        pass

    pass

class GraphInstallerInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('INSTALLED_HEADER_ENTRYPOINT', getattr(self, 'INSTALLED_HEADER_ENTRYPOINT'))
        pass

    def INSTALLED_HEADER_ENTRYPOINT(self, filename, dir):
        self.object_.add_entry_point(filename=filename, dir=dir)
        pass
    pass

class GraphInstallerSetup(Setup):
    def setup_directory(self, directory_builder):
        super(GraphInstallerSetup, self).setup_directory(directory_builder)

        installer = GraphInstaller()

        directory_builder.add_builder(installer)

        if directory_builder.configurator() is not None:
            directory_builder.configurator().add_method(
                GraphInstallerInterfaceProxy(object=installer))
            pass
        pass
    pass
