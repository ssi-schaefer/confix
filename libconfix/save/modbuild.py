# $Id: modbuild.py,v 1.125 2006/07/04 14:36:48 jfasch Exp $

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
import types
import time

import const
import core.debug
import core.helper
from core.depindex import ProvideMap
from paragraph import ParagraphSet, OrderedParagraphSet
from buildable import Buildable, DependencyInformation
from buildable_single import BuildableSingle
from core.error import Error
from fileprops import FilePropertiesSet
from modbase import ModuleBase
from modbuildprops import BuildableModuleProperties
from buildable_mgr import BuildableManager
from modinst import InstalledModule
from makefile_py import Makefile_py
from core.provide import Provide
from pseudo_registry import PseudoHandWrittenFileRegistry
from core.require import Require
from makefile_am import Makefile_am
from core.marshalling import Unmarshallable
from buildinfoset import BuildInformationSet
from marshalling import Unmarshallable
from installer import FileInstallerFactory

class BuildableModule(ModuleBase, Unmarshallable):

    """ A BuildableModule object represents a directory containing
    buildable files of some sort. BuildableModule objects manage the
    files in their directory, through
    L{buildable<buildable.Buildable>} objects. The individual files in
    the directory report dependency, include, and other information to
    their BuildableModule supervisor. The BuildableModule then reports
    some of this information back to its parent L{package
    <package.Package>} object.

    The detailed list of responsibilities is similar to that of the
    Package; this is because Package delegates much of its work to the
    BuildableModule objects it manages. It is partly dictated by the
    way Package generates the L{dependency
    graph<digraph.digraph.DirectedGraph>}; see L{there<package.Package>}
    for a detailed explanation. BuildableModule's responsibilities are
    more fine grained though. """

    def __init__(self,
                 dir,
                 use_libtool,
                 makefile_am,
                 write_makefile_am,
                 packagename,
                 localname,

                 file_installer_factory=None
                 ):

        ModuleBase.__init__(self)

        self.packagename_ = packagename
        self.localname_ = localname
        
        # The directory I am responsible for.

        self.dir_ = dir

        # a flag that tells me if I should generate output that builds
        # libtool libraries. boolean semantics, of course.

        self.use_libtool_ = use_libtool

        # an object I use for installing files

        if file_installer_factory is None:
            self.file_installer_factory_ = FileInstallerFactory(
                use_bulk_install=False,
                configure_in=None,
                auxdir=None,
                source_auxdir=None)
        else:
            self.file_installer_factory_ = file_installer_factory
            pass

        self.file_installer_ = self.file_installer_factory_.create()

        # Submodules that I manage. These are not in any way related
        # to me except that I eventually create them.

        self.submodules_ = []
        
        # the Buildable objects I manage

        self.buildables_ = []

        # a good friend of mine who manages my buildables.

        self.buildablemgr_ = BuildableManager(global_mgr=BuildableManager.instance)        

        # argh: document that. better yet, refactor it away :-)

        self.buildmodprops_ = BuildableModuleProperties()

        # per-filename properties

        self.fileproperties_ = FilePropertiesSet()

        # dependency information, including package internal provide
        # object that our base class never sees.

        self.depinfo_ = DependencyInformation()

        # build information that I have, in addition to what my
        # buildables have
        self.direct_buildinfos_ = BuildInformationSet()

        # argh. remove this bullshit soon.

        self.featuremacro_name_ = None
        self.featuremacro_description_ = ''

        # our Makefile.am writer object.

        assert makefile_am
        self.makefile_am_ = makefile_am
        self.write_makefile_am_ = write_makefile_am

        # function definitions that will go into the package's
        # acinclude.m4
        
        self.acinclude_m4_ = ParagraphSet()
        
        # configure.in contributions

        self.configure_in_ = OrderedParagraphSet()

        # our Makefile.py and module description file go into
        # EXTRA_DIST so that they will be in the source package.

        if os.path.isfile(os.path.join(self.dir(), const.MAKEFILE_PY)):
            self.makefile_am().add_extra_dist(const.MAKEFILE_PY)

        # 'make maintainer-clean' should remove the file we generate

        self.makefile_am().add_maintainercleanfiles('Makefile.am') # in confix2
        self.makefile_am().add_maintainercleanfiles('Makefile.in') # in confix2

        # buildables may register arbitrary output files which they
        # append lines to. I take care to write these file only if
        # they have changed. the plan is to take this as a preliminary
        # stage to (1) pseudo-handwritten file, and to (2) writing
        # build instructions for other build tools than automake.

        # format: dictionary {

        #      "filename (only basename, without any path)": [lines] }

        self.pseudo_handwritten_files_ = {}

        # names of the files in self.dir_ that should be ignored when
        # we determine buildables.

        self.ignore_direntries_ = [const.MAKEFILE_PY]

        # FIXME: remove this bad hack ASAP. it is only needed anymore
        # (as of 2006-04-18) by the salomon pdl plugin.
        self.makefile_am_.set_file_installer(self.file_installer_)

        pass

    def __str__(self): return 'BuildableModule '+'.'.join(self.fullname())

    def packagename(self): return self.packagename_

    def set_packagename(self, name):
        assert self.packagename_ is None
        self.packagename_ = name
        pass

    def fullname(self):
        assert self.packagename_ is not None, 'Module '+'.'.join(self.localname_)+': no packagename set'
        return [self.packagename_] + self.localname_

    def localname(self):
        return self.localname_

    def file_installer(self):
        return self.file_installer_

    def file_installer_factory(self):
        return self.file_installer_factory_

    def provides(self):
        return self.depinfo_.provides()

    def add_provide(self, p):
        self.depinfo_.add_provide(p)
        pass

    def requires(self):
        return self.depinfo_.requires()
    
    def add_require(self, r):
        self.depinfo_.add_require(r)
        pass

    def add_buildinfo(self, b):
        self.direct_buildinfos_.add(b)
        pass
    def buildinfos(self):

        """ Return all build information that a user of mine might be
        interested in. "All" is: my own local build information I
        have, plus the build information of all my buildables. """
        
        if self.__dict__.has_key('buildinfo_cache_') and \
               self.buildinfo_cache_['num_last_buildables'] == len(self.buildables_):
            return self.buildinfo_cache_['buildinfos']

        ret_buildinfos = BuildInformationSet()
        ret_buildinfos.merge(self.direct_buildinfos_)
        for b in self.buildables_:
            ret_buildinfos.merge(b.buildinfos())
            pass

        self.buildinfo_cache_ = {
            'num_last_buildables': len(self.buildables_),
            'buildinfos': ret_buildinfos}

        return ret_buildinfos

    def get_featuremacro(self):
        return (self.featuremacro_name_,
                self.featuremacro_description_)
    def set_featuremacro(self, macroname, description):
        self.featuremacro_name_ = macroname
        self.featuremacro_description_ = description

    def buildable_manager(self): return self.buildablemgr_

    def fileproperties(self): return self.fileproperties_

    def add_buildable(self, b):
        """
        Add a Buildable object to our list of things to manage.

        @type  b: L{Buildable <buildable.Buildable>}
        @param b: The Buildable object to add.
        """

        assert isinstance(b, Buildable)
        for bu in self.buildables_:
            if b.name() == bu.name():
                raise Error(self.dir() + ': cannot add buildable ' + b.name() + ' '
                            '(of type '+b.__class__.__name__+') because it is already managed '
                            '(of type '+bu.__class__.__name__+')')
        self.buildables_.append(b)

    def buildables(self):

        return self.buildables_

    def add_ignore_file(self, file):

        self.ignore_direntries_.append(file)

    def buildmodprops(self):

        return self.buildmodprops_

    def use_libtool(self):

        return self.use_libtool_

    def makefile_am(self): return self.makefile_am_

    def add_acinclude_m4(self, paragraph):
        self.acinclude_m4_.add(paragraph)
        pass

    def add_configure_in(self, paragraph, order):
        self.configure_in_.add(paragraph=paragraph, order=order)
        pass

    def scan(self):

        # have our BuildableManager guess buildables from the
        # directory contents. make sure that the BuildableManager does
        # not accidentally see pseudo-handwritten files that were
        # created by a previous confix run.

        if 1:
            previous = PseudoHandWrittenFileRegistry(
                dir=self.dir(),
                filename=const.PSEUDO_HANDWRITTEN_LIST_FILENAME)
            previous.load()

            self.buildables_.extend(self.buildablemgr_.create_from_dir(
                dir=self.dir_,
                ignore_files=self.ignore_direntries_+previous.get_registered_files()))


        # discover any submodules, and scan() them, recursively.

        error_list = []

        assert os.path.isdir(self.dir())
        for entry in os.listdir(self.dir()):
            if entry in self.ignore_direntries_: continue
            subdir = os.path.normpath( # because toplevel module's dir is '.'
                os.path.join(self.dir(), entry))
            if not os.path.isdir(subdir):
                continue
            if os.path.isfile(os.path.join(subdir, const.MAKEFILE_PY)):
                submod = BuildableModule(
                    packagename=self.packagename(),
                    localname=self.localname() + [entry],
                    dir=subdir,
                    use_libtool=self.use_libtool_,
                    makefile_am=Makefile_am(subdir),
                    write_makefile_am=True,
                    file_installer_factory=self.file_installer_factory_)
                try:
                    makefile_py = Makefile_py(dir=subdir, module=submod, package=None)
                    makefile_py.execute()
                    if not makefile_py.ignore_as_submodule():
                        submod.scan()
                        self.submodules_.append(submod)
                except Error, e:
                    error_list.append(Error('Cannot scan module in directory '+subdir, [e]))
                
        if len(error_list):
            raise Error('There were errors creating/scanning submodules of '+self.dir(), error_list)

    def validate(self):

        for b in self.buildables_:
            if isinstance(b, BuildableSingle):
                p = self.fileproperties_.get_by_filename_or_type(filename=b.filename(), buildable_type=b.__class__)
                b.consume_fileproperties(p)

        # cluster our buildables, creating a new set of buildables as
        # we go.

        self.buildables_ = self.buildablemgr_.create_clusters(buildables=self.buildables_,
                                                              module=self)

        for b in self.buildables_:
            b.validate()

    def submodules(self): return self.submodules_

    def add_submodule(self, m): self.submodules_.append(m)

    def recursive_submodules(self):

        ret = self.submodules_[:]
        for m in self.submodules_:
            ret.extend(m.recursive_submodules())
        return ret

    def world(self, modules):

        """ This is a chance for a BuildableModule object to get an
        idea of the outside world, just before all modules begin to
        talk to each other as part of the resolving process. Even more
        so, this is a chance for the BuildableModule's
        L{Buildable<buildable.Buildable>} objects. A common usage of
        this knowledge is to generate dependency information, based on
        what they see.

        @type modules: list of modules

        @param modules: all modules that are considered for the
        dependency graph

        """

        for b in self.buildables_:
            b.world(modules)
            pass
        pass

    def gather_build_info(self, modules):
        for b in self.buildables():
            b.gather_build_info(modules)
            pass
        pass

    def gather_dependency_info(self):

        """ Ask our buildables for dependency information. This is
        their chance to request the use of other modules during the
        build of this one. A buildable does this by adding an
        appropriate L{require <require.Require>} object to the calling
        module. Also, here's the chance for buildables to advertise
        themselves for use by other modules; this is done by adding an
        appropriate L{provide <provide.Provide>} object to the calling
        module. """

        core.debug.trace(['depinfo'], 'BuildableModule('+'.'.join(self.fullname())+'): '
                    'asking my buildables for dependency information')

        num_di_before = self.depinfo_.size()
        new_depinfo = self.depinfo_
        self.depinfo_ = DependencyInformation()

        for b in self.buildables():
            new_depinfo.add(b.get_dependency_info())
            assert new_depinfo.size() >= num_di_before
            pass

        core.debug.trace(['depinfo'], 'Done gathering dependency info')
        core.debug.trace(['depinfo', 'performance'], 'Remove internal require objects: '
                    ''+'.'.join(self.fullname())+', '+time.ctime())

        # eliminate Require objects that are resolved internally, in
        # order for them to not molest the resolving process
        # unnecessarily.

        internal_provide_map = ProvideMap(permissive=False)
        
        for p in \
                new_depinfo.provides() + \
                new_depinfo.internal_provides():
            internal_provide_map.add(p, self)
            pass

        removed = []

        for r in new_depinfo.requires():
            found_nodes = internal_provide_map.find_match(r)
            if len(found_nodes):
                removed.append(r)
                continue
            self.depinfo_.add_require(r)
            pass

##         for p in new_depinfo.public_provides():
##             self.depinfo_.add_public_provide(p)
##             pass
##         for p in new_depinfo.package_provides():
##             self.depinfo_.add_package_provide(p)
##             pass

        for p in new_depinfo.provides():
            self.depinfo_.add_provide(p)
            pass

        core.debug.trace(['depinfo'], 'Removed requires:\n  '+'\n  '.join([str(r) for r in removed]))
        core.debug.trace(['depinfo'], 'Requires:\n  '+'\n  '.join([str(r) for r in self.depinfo_.requires()]))

        core.debug.trace(['depinfo', 'performance'], 'Done  internal require objects, '+time.ctime())
        pass

    def size_of_dependency_info(self):
        return self.depinfo_.size()

    def gather_configure_in(self):
        ret = OrderedParagraphSet()
        ret.update(self.configure_in_)
        for b in self.buildables():
            ret.update(b.gather_configure_in())
            pass
        return ret

    def gather_acinclude_m4(self):
        ret = ParagraphSet()
        ret.update(self.acinclude_m4_)
        for b in self.buildables():
            ret.update(b.gather_acinclude_m4())
            pass
        return ret

    def gather_handled_files(self):

        ret = []
        for b in self.buildables_:
            ret.extend(b.gather_handled_files())

        if len(ret) == 0:

            # no files here in this module. presumably we are only
            # generating files from other, foreign, files. anyway,
            # rather than returning nothing, we return our Makefile.py
            # which we are sure we have.

            ret.append(const.MAKEFILE_PY)

        return ret

    def reset_build_infos(self):
        for b in self.buildables_:
            b.reset_build_infos()
            pass
        pass

    def output(self):

        """ Write an output Makefile.am file describing the build
        instructions for the buildable objects in this
        BuildableModule.

        Write pseudo-handwritten files that Buildable objects may have
        registered. """

        for b in self.buildables():
            b.contribute_makefile_am(buildmod=self)
            pass

        # install headers

        self.makefile_am().add_line('')
        self.file_installer_.output(buildmod=self)

        # write Makefile.am

        if self.write_makefile_am_:
            self.makefile_am().output()

        # write additional files.

        self.write_pseudo_handwritten_files()

    def dir(self): return self.dir_

    def add_pseudo_handwritten_file(self, filename):

        if not self.pseudo_handwritten_files_.has_key(filename):
            self.pseudo_handwritten_files_[filename] = []

    def add_lines_to_pseudo_handwritten_file(self, filename, lines):

        assert self.pseudo_handwritten_files_.has_key(filename)
        self.pseudo_handwritten_files_[filename].extend(lines)

    def install(self):

        """ Create an installed incarnation of ourself. That
        incarnation contains

           - our public dependency information (that is, not what is
             only seen inside our package).

           - installed incarnations of our buildinfos """

        # argh. have to remove this cruft soon.
        (fname, fdesc) = self.get_featuremacro()

        # create "installed" incarnations of our BuildInformation
        # objects.
        inst_bi = BuildInformationSet()
        for bi in self.buildinfos():
            inst_bi.add(bi.install())
            pass

        return InstalledModule(
            fullname=self.fullname(),
            provides=self.depinfo_.provides(),
            requires=self.depinfo_.requires(),
            buildinfos=inst_bi,
            featuremacro_name=fname,
            featuremacro_description=fdesc)

    def install_header_public(self, filename, install_path):
        self.file_installer_.add_public_header(filename=filename, dir=install_path)
        pass

    def install_header_private(self, filename, install_path):
        self.file_installer_.add_private_header(filename=filename, dir=install_path)
        pass

    def write_pseudo_handwritten_files(self):

        # see what pseudo-handwritten files were created by a previous
        # confix run. synchronize those with what we will be writing
        # in this run (i.e. remove those which won't be written
        # anymore). write updated registry.

        previous = PseudoHandWrittenFileRegistry(
            dir=self.dir(),
            filename=const.PSEUDO_HANDWRITTEN_LIST_FILENAME)

        current = PseudoHandWrittenFileRegistry(
            dir=self.dir(),
            filename=const.PSEUDO_HANDWRITTEN_LIST_FILENAME)

        previous.load()

        for fn in self.pseudo_handwritten_files_.keys():
            current.register_file(fn)
        
        current.synchronize_dir_content(previous)

        current.dump()

        # write the pseudo-handwritten files from this confix run.

        for fn in self.pseudo_handwritten_files_.keys():
            core.helper.write_lines_to_file_if_changed(
                os.path.join(self.dir(), fn),
                self.pseudo_handwritten_files_[fn])
            pass
        pass
    pass
