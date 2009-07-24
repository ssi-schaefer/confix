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

# jjj remove this >>> 
## from libconfix.plugins.automake.file_installer import FileInstaller
## from libconfix.plugins.automake.makefile_am import Makefile_am
# jjj remove this <<<

from libconfix.core.digraph import toposort
from libconfix.core.filesys.vfs_directory import VFSDirectory
from libconfix.core.filesys.file import File
from libconfix.core.machinery.builderset import BuilderSet
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
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import os

class DirectoryBuilder(EntryBuilder, LocalNode):

    def __init__(self, directory):
        assert isinstance(directory, VFSDirectory)

        EntryBuilder.__init__(
            self,
            entry=directory)
        
        self.__directory = directory        

        # the builders that I maintain, compositely.
        self.__regular_builders = BuilderSet()

        # builders that generate directory-wide output, such as
        # automake's Makefile.am. I maintain them as separate set of
        # builders because others use them to dump their stuff in, and
        # only when all is done they can write output.
        self.__backend_dirbuilders = BuilderSet()

        # a list of interface proxy objects that are added initially
        # by the different setup objects. we only keep them for future
        # use by any Confix2.dir objects.
        self.__interfaces = []

        # jjjj
##         # the (contents of the) Makefile.am we will be writing on
##         # output()
##         self.__makefile_am = Makefile_am()

##         # a helper that we use to install files intelligently (well,
##         # more or less so).
##         self.__file_installer = FileInstaller()

        self.__pseudo_handwritten_mgr = PseudoHandWrittenFileManager(directory)

        # initialize collected dependency information
        self.__init_dep_info()

        pass

    def short_description(self):
        return '.'.join([self.package().name()]+self.directory().relpath(self.package().rootdirectory()))

    def initialize(self, package):
        """
        Recursively initialize self and the children.
        """
        assert package, self
        # first of all, ask the package to configure me. I have to do
        # this before initializing anything - else, if I initialize
        # myself too early, then adding a builder will trigger
        # initializing it, and I will end up trying to initialize it
        # twice (which is letal)
        package.setup().setup(dirbuilder=self)

        # now's the time
        super(DirectoryBuilder, self).initialize(package=package)
        assert self.package() is not None # initialize() should have done that.

        # then, initialize my builders, recursively. copy the initial
        # list because it may change under the hood.
        builders = []
        for b in self.__regular_builders.iter_builders():
            builders.append(b)
            pass
        for b in self.__backend_dirbuilders.iter_builders():
            builders.append(b)
            pass
        
        for b in builders:
            assert not b.is_initialized(), 'self: '+str(self)+', builder: '+str(b)
            b.initialize(package=self.package())
            # verify that initialize() has reached the Builder base
            # class
            assert b.is_initialized(), b
            pass
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

    # jjj
##     def makefile_am(self):
##         return self.__makefile_am

##     def remove_me_jjj_file_installer(self):
##         return self.__file_installer

    def iter_builders(self):
        for b in self.__backend_dirbuilders.iter_builders():
            yield b
            pass
        for b in self.__regular_builders.iter_builders():
            yield b
            pass
        pass

    def add_builder(self, b):
        self.__regular_builders.add_builder(b)
        self.__init_builder(b)
        pass

    def remove_builder(self, b):
        self.__regular_builders.remove_builder(b)
        b.set_parentbuilder(None)
        pass

    def add_backend_dirbuilder(self, b):
        self.__backend_dirbuilders.add_builder(b)
        self.__init_builder(b)
        pass

    def find_entry_builder(self, path):
        """
        Convenience method: find an entry builder that manages an
        entry object with the relative path 'path'. Return None if
        none is found.
        """
        assert type(path) in (list, tuple), path
        tmp_path = path[:]
        if len(tmp_path) == 0:
            return self
        entryname = tmp_path.pop(0)
        for b in self.iter_builders():
            if isinstance(b, DirectoryBuilder) and b.directory().name() == entryname:
                if len(tmp_path) == 0:
                    return b
                else:
                    return b.find_entry_builder(tmp_path)
                pass
            if isinstance(b, FileBuilder) and b.file().name() == entryname:
                if len(tmp_path) == 0:
                    return b
                else:
                    raise Error('Found FileBuilder ('+str(b)+') and rest of path ('+tmp_path+') remains')
                pass
            pass
        return None

    def interfaces(self):
        return self.__interfaces

    def add_interface(self, interface):
        self.__interfaces.append(interface)
        pass

    def output(self):
        EntryBuilder.output(self)

        # jjjj
##         # 'make maintainer-clean' should remove the file we generate
        
##         self.__makefile_am.add_maintainercleanfiles('Makefile.am')
##         self.__makefile_am.add_maintainercleanfiles('Makefile.in')

        # let our builders write their output, recursively
        for b in self.__regular_builders.iter_builders():
            b.output()
            assert b.base_output_called() == True, str(b)
            pass

        # jjjj
##         # the file installer is a little helper that relieves our
##         # builders from having to care of how files are installed. our
##         # builders use it to format their install wishes down to our
##         # Makefile.am. so, basically, what I want to say is that we
##         # have to flush the file installer into self.__makefile_am
##         # *after* flushing the builders, and before flushing
##         # self.__makefile_am

##         # prepare the raw file object, and wrap a Makefile_am instance
##         # around it.

##         self.__file_installer.output(makefile_am=self.__makefile_am)

##         # finally, write our Makefile.am.
        
##         mf_am = self.__directory.find(['Makefile.am'])
##         if mf_am is None:
##             mf_am = File()
##             self.__directory.add(name='Makefile.am', entry=mf_am)
##         else:
##             mf_am.truncate()
##             pass

##         mf_am.add_lines(self.__makefile_am.lines())

        for b in self.__backend_dirbuilders.iter_builders():
            b.output()
            pass
        
        pass
     
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

        for b in self.__node_managed_builders():
            builder_dependency_info = b.dependency_info()
            assert builder_dependency_info is not None, str(b)
            assert b.base_dependency_info_called(), str(b)

            # we provide these anyway, so add them immediately
            self.__provides.merge(builder_dependency_info.provides())

            # index all provides, to sort out the requires later on.
            for p in builder_dependency_info.provides():
                internal_provides.add(p, self)
                pass
            for p in builder_dependency_info.internal_provides():
                internal_provides.add(p, self)
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

    def __node_managed_builders(self):
        yield self
        for b in self.iter_builders():
            if not isinstance(b, Node):
                yield b
                pass
            pass
        pass

    def node_relate_managed_builders(self, digraph):
        topolist = toposort.toposort(digraph=digraph, nodes=[self])
        assert topolist[-1] is self
        topolist = topolist[0:-1]

        for b in self.__node_managed_builders():
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
        for b in self.iter_builders():
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

    def __init_builder(self, b):
        b.set_parentbuilder(self)

        # if I am initialized, then I must ensure that any builder is
        # initialized before anybody can get his hands on it.
        if self.is_initialized():
            assert self.package(), self
            if not b.is_initialized():
                b.initialize(package=self.package())
                assert b.is_initialized(), b
                pass
            pass
        pass
        

    pass
