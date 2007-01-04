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

from libconfix.core.automake.file_installer import FileInstaller
from libconfix.core.automake.makefile_am import Makefile_am
from libconfix.core.digraph import toposort
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.buildinfoset import BuildInformationSet
from libconfix.core.machinery.dependencyset import DependencySet
from libconfix.core.machinery.depindex import ProvideMap
from libconfix.core.machinery.entrybuilder import EntryBuilder
from libconfix.core.machinery.installed_node import InstalledNode
from libconfix.core.machinery.local_node import LocalNode
from libconfix.core.machinery.node import Node
from libconfix.core.machinery.provide import Provide
from libconfix.core.machinery.provide_string import Provide_String
from libconfix.core.machinery.pseudo_handwritten import PseudoHandWrittenFileManager
from libconfix.core.machinery.require import Require
from libconfix.core.machinery.require_string import Require_String
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

from iface import DirectoryBuilderInterfaceProxy

class DirectoryBuilder(EntryBuilder, LocalNode):

    class DuplicateBuilderError(Error):
        def __init__(self, existing_builder, new_builder):
            Error.__init__(self, msg='Duplicate builder: existing "'+str(existing_builder)+'", new "'+str(new_builder)+'"')
            pass
        pass
    
    def __init__(self,
                 directory,
                 configurator):
        assert isinstance(directory, Directory)

        EntryBuilder.__init__(
            self,
            entry=directory)
        
        self.__directory = directory        
        self.__configurator = configurator

        # the builders that I maintain, compositely. a dictionary that
        # maps from the locally unique builder IDs to the builders
        # themselves.
        self.__builders = {}
        
        # names of files and directories that are to be ignored
        self.__ignored_entries = set()

        # the (contents of the) Makefile.am we will be writing on
        # output()
        self.__makefile_am = Makefile_am()

        # a helper that we use to install files intelligently (well,
        # more or less so).
        self.__file_installer = FileInstaller()

        self.__pseudo_handwritten_mgr = PseudoHandWrittenFileManager(directory)

        # initialize collected dependency information
        self.__init_dep_info()

        pass

    def shortname(self):
        ret = 'Hierarchy.DirectoryBuilder('
        if self.directory().parent():
            ret += self.directory().name()
        else:
            ret += '<root>'
            pass
        ret += ')'
        return ret

    def directory(self):
        return self.entry()

    def makefile_am(self):
        return self.__makefile_am

    def file_installer(self):
        return self.__file_installer

    def add_ignored_entries(self, names):
        self.__ignored_entries |= set(names)
        pass

    def entries(self):
        ret = []
        for name, entry in self.directory().entries():
            if name not in self.__ignored_entries:
                ret.append((name, entry))
                pass
            pass
        return ret

    def builders(self):
        return self.__builders.values()

    def add_builder(self, b):
        b.set_parentbuilder(self)
        id = b.locally_unique_id()
        existing_builder = self.__builders.get(id)
        if existing_builder:
            raise DuplicateBuilderError(existing_builder=existing_builder, new_builder=b)
        self.__builders[id] = b
        pass

    def add_builders(self, builderlist):
        for b in builderlist:
            self.add_builder(b)
            pass
        pass

    def remove_builder(self, b):
        id = b.locally_unique_id()
        assert self.__builders.has_key(id)
        del self.__builders[id]
        pass

    def configurator(self):
        return self.__configurator

    def configure(self):
        super(DirectoryBuilder, self).configure()
        # have my configurator fiddle with me
        if self.__configurator is not None:
            self.__configurator.configure_directory()
            pass
        pass

    def output(self):
        EntryBuilder.output(self)
        
        # 'make maintainer-clean' should remove the file we generate
        
        self.__makefile_am.add_maintainercleanfiles('Makefile.am')
        self.__makefile_am.add_maintainercleanfiles('Makefile.in')

        # let our builders write their output, recursively
        for b in self.__builders.itervalues():
            b.output()
            assert b.base_output_called() == True, str(b)
            pass

        # ... comment needed badly ...
        prev_registry_file = self.__directory.get(const.PSEUDO_HANDWRITTEN_LIST_FILENAME)
        # what to do here?
        # ...

        # the file installer is a little helper that relieves our
        # builders from having to care of how files are installed. our
        # builders use it to format their install wishes down to our
        # Makefile.am. so, basically, what I want to say is that we
        # have to flush the file installer into self.__makefile_am
        # *after* flushing the builders, and before flushing
        # self.__makefile_am

        # prepare the raw file object, and wrap a Makefile_am instance
        # around it.

        self.__file_installer.output(makefile_am=self.__makefile_am)

        # finally, write our Makefile.am.
        
        mf_am = self.__directory.find(['Makefile.am'])
        if mf_am is None:
            mf_am = File()
            self.__directory.add(name='Makefile.am', entry=mf_am)
        else:
            mf_am.truncate()
            pass

        mf_am.add_lines(self.__makefile_am.lines())

        pass
     
    def iface_pieces(self):
        return EntryBuilder.iface_pieces(self) + \
               [DirectoryBuilderInterfaceProxy(directory_builder=self)]

    # Node

    def recollect_dependency_info(self):
        self.__prev_provides = self.__provides
        self.__prev_requires = self.__requires

        self.__init_dep_info()
        
        # collect dependency information. we sort out requires that
        # are resolved internally (i.e. within our builders).
        
        # collect build information.

        internal_provides = ProvideMap(permissive=False)
        requires = DependencySet(klass=Require, string_klass=Require_String)

        for b in self.node_managed_builders():
            builder_dependency_info = b.dependency_info()
            assert builder_dependency_info is not None, str(b)
            assert b.base_dependency_info_called(), str(b)

            # we provide these anyway, so add them immediately
            self.__provides.merge(builder_dependency_info.provides())

            # index all provides, to sort out the requires later on.
            for p in builder_dependency_info.provides():
                internal_provides.add(p, 666)
                pass
            for p in builder_dependency_info.internal_provides():            
                internal_provides.add(p, 666)
                pass
            requires.merge(builder_dependency_info.requires())

            pass

        # add require objects that are not internally resolved to the
        # node's dependency info.
        for r in requires:
            found_nodes = internal_provides.find_match(r)
            if len(found_nodes) == 0:
                self.__requires.add(r)
                pass
            pass
        pass

    def node_dependency_info_changed(self):
        return not (self.__prev_provides.is_equal(self.__provides) and \
                    self.__prev_requires.is_equal(self.__requires))

    def node_managed_builders(self):
        ret = [self]
        for b in self.__builders.itervalues():
            if not isinstance(b, Node):
                ret.append(b)
                pass
            pass
        return ret

    def node_relate_managed_builders(self, digraph):
        topolist = toposort.toposort(digraph=digraph, nodes=[self])
        assert topolist[-1] is self
        topolist = topolist[0:-1]
        for b in self.node_managed_builders():
            b.relate(node=self, digraph=digraph, topolist=topolist)
            assert b.base_relate_called(), str(b)
            pass
        pass

    def provides(self):
        return self.__provides
        pass
    
    def requires(self):
        return self.__requires

    def buildinfos(self):
        ret = BuildInformationSet()
        ret.merge(EntryBuilder.buildinfos(self))
        for b in self.__builders.itervalues():
            if not isinstance(b, Node):
                ret.merge(b.buildinfos())
                pass
            pass
        return ret

    def install(self):
        return InstalledNode(
            name=self.__directory.relpath(self.package().rootdirectory()),
            provides=[p for p in self.__provides],
            requires=[r for r in self.__requires],
            buildinfos=[b.install() for b in self.buildinfos()])

    def create_pseudo_handwritten_file(self, filename):
        return self.__pseudo_handwritten_mgr.create_file(filename)

    def __init_dep_info(self):
        self.__provides = DependencySet(klass=Provide, string_klass=Provide_String)
        self.__requires = DependencySet(klass=Require, string_klass=Require_String)
        pass
    
    pass
