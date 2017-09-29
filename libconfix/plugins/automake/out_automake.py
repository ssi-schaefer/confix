# Copyright (C) 2009 Joerg Faschingbauer

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

from makefile_am import Makefile_am
from file_installer import FileInstaller
from buildinfo import BuildInfo_Configure_in
from buildinfo import BuildInfo_ACInclude_m4

from libconfix.plugins.automake import readonly_prefixes
from libconfix.plugins.automake import repo_automake
from libconfix.plugins.automake.configure_ac import Configure_ac 
from libconfix.plugins.automake.acinclude_m4 import ACInclude_m4 

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.file import FileState
from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.hierarchy import confix_admin
from libconfix.core.utils import const
from libconfix.core.utils import helper
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils.error import Error

import os

def find_automake_output_builder(dirbuilder):
    """
    Find the directory's dedicated automake output builder.
    """
    for b in dirbuilder.iter_builders():
        if type(b) is AutomakeBackendOutputBuilder:
            return b
        pass
    else:
        assert False
        pass
    pass

class AutomakeBackendOutputBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)

        # only the package root directory will have configure.ac and
        # acinclude.m4. we will allocate them once we know where we
        # are.
        self.__configure_ac = None
        self.__acinclude_m4 = None

        # any directory has a Makefile.am ...
        self.__makefile_am = Makefile_am()
        # ... and helper that we use to install files intelligently
        # (well, more or less so).
        self.__file_installer = FileInstaller()
        

        # a flag to generate other builders only once.
        self.__bursted = False
        
        pass

    def configure_ac(self):
        assert self.__configure_ac is not None
        return self.__configure_ac
    def acinclude_m4(self):
        assert self.__acinclude_m4 is not None
        return self.__acinclude_m4
    def makefile_am(self):
        return self.__makefile_am
    def file_installer(self):
        return self.__file_installer

    def locally_unique_id(self):
        return str(self.__class__)

    def initialize(self, package):
        super(AutomakeBackendOutputBuilder, self).initialize(package)
        if self.parentbuilder() is package.rootbuilder():
            self.__configure_ac = Configure_ac()
            self.__acinclude_m4 = ACInclude_m4()
        else:
            top_automake_output_builder = find_automake_output_builder(package.rootbuilder())
            self.__configure_ac = top_automake_output_builder.configure_ac()
            self.__acinclude_m4 = top_automake_output_builder.acinclude_m4()
            pass
        pass

    def enlarge(self):
        if self.__bursted:
            return
        self.__bursted = True

        # if in the toplevel directory, setup our autoconf auxiliary
        # directory. this a regular builder by itself, but plays a
        # special role for us because we use it to put, well,
        # auxiliary files in.
        if self.parentbuilder() is self.package().rootbuilder():
            # create the directory hierarchy if necessary.
            admin_dir_builder = confix_admin.add_confix_admin(self.package())
            automake_dir = admin_dir_builder.directory().get('automake')
            if automake_dir is None:
                automake_dir = admin_dir_builder.directory().add(name='automake', entry=Directory())
                pass

            automake_dir_builder = admin_dir_builder.add_builder(AutoconfAuxDirBuilder(directory=automake_dir))
            pass
        pass

    def relate(self, node, digraph, topolist):
        super(AutomakeBackendOutputBuilder, self).relate(node=node, digraph=digraph, topolist=topolist)

        for n in topolist:
            for bi in n.iter_buildinfos_type(BuildInfo_Configure_in):
                self.configure_ac().add_paragraph(
                    paragraph=Paragraph(lines=bi.lines(), md5=bi.md5()),
                    order=bi.order())
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_ACInclude_m4):
                self.acinclude_m4().add_paragraph(
                    paragraph=Paragraph(lines=bi.lines(), md5=bi.md5()))
                pass
            pass
        pass

    def output(self):
        super(AutomakeBackendOutputBuilder, self).output()
        
        # 'make maintainer-clean' should remove the files we generate
        self.makefile_am().add_maintainercleanfiles('Makefile.am')
        self.makefile_am().add_maintainercleanfiles('Makefile.in')
        
        # dump file_installer's knowledge into Makefile.am
        self.file_installer().output(makefile_am=self.__makefile_am)

        # distribute the package configuration file, but only if it is
        # part of the physical package structure.
        if self.parentbuilder() is self.package().rootbuilder():
            confix2_pkg = self.package().rootdirectory().get(const.CONFIX2_PKG)
            if not confix2_pkg.is_overlayed():
                self.makefile_am().add_extra_dist(const.CONFIX2_PKG)
                pass
            pass

        self.configure_ac().set_packagename(self.package().name())
        self.configure_ac().set_packageversion(self.package().version())

        # we require autoconf 2.52 because it has (possibly among
        # others) AC_HELP_STRING(), and can go into subsubdirs from
        # the toplevel.
        self.configure_ac().set_minimum_autoconf_version('2.52')

        # we never pass AC_DEFINE'd macros on the commandline. rather,
        # we put everything in config.h.
        self.configure_ac().add_ac_config_headers('config.h')


        # our minimum required automake version is 1.9
        self.makefile_am().add_automake_options('1.9')


        # enable dist'ing in the following formats
        self.makefile_am().add_automake_options('dist-bzip2')
        self.makefile_am().add_automake_options('dist-zip')


        # the ubiquitous readonly-prefixes: add the configure option
        # and stuff.
        self.configure_ac().add_paragraph(
            paragraph=readonly_prefixes.commandline_option_paragraph,
            order=Configure_ac.OPTIONS)


        # register subdirectories with our toplevel Makefile.am.
        if self.parentbuilder() is self.package().rootbuilder():
            for dirnode in self.package().topo_directories():
                assert isinstance(dirnode, DirectoryBuilder)
                relpath = dirnode.directory().relpath(self.package().rootdirectory())
                if len(relpath):
                    dirstr = '/'.join(relpath)
                    self.makefile_am().add_subdir(dirstr)
                    self.configure_ac().add_ac_config_files('/'.join(relpath+['Makefile']))
                else:
                    dirstr = '.'
                    self.makefile_am().add_subdir(dirstr)
                    self.configure_ac().add_ac_config_files('Makefile')
                    pass
                pass
            pass


        # piggy-back the repo install on automake.
        if self.parentbuilder() is self.package().rootbuilder():
            self.makefile_am().define_install_directory(
                symbolicname='confixrepo',
                dirname=repo_automake.dir_for_automake())
            self.makefile_am().add_to_install_directory(
                symbolicname='confixrepo',
                family='DATA',
                files=[self.package().repofilename()])
            self.makefile_am().add_extra_dist(
                name=self.package().repofilename())
            pass

        # AC_CONFIG_SRCDIR (for paranoia and sanity checks): we need
        # one unique file in the tree, as a meaningful argument to
        # AC_CONFIG_SRCDIR.
        if True:
            goodfile = notsogoodfile = None

            for b in self.package().iter_builders():
                if not isinstance(b, FileBuilder):
                    continue
                if b.file().is_overlayed():
                    # we won't put files from an overlay into the
                    # package since automake and friends won't be able
                    # to find them.
                    continue
                if isinstance(b.file(), File) and b.file().state() == FileState.VIRTUAL:
                    # also, there may be "virtual" files around (but
                    # only if the file's a "real" file) which we
                    # cannot put into a package. (boy, this sucks!)
                    continue

                if b.file().name() not in [const.CONFIX2_PKG, const.CONFIX2_DIR]:
                    goodfile = b.file()
                    break
                notsogoodfile = b.file()
                pass
        
            if goodfile:
                unique_file = goodfile
            elif notsogoodfile:
                unique_file = notsogoodfile
            else:
                raise Error('Not even one file handled by any submodule of '
                            'package '+self.package().name()+"; "
                            "probably the current working directory "
                            "("+os.getcwd()+") is not "
                            "the package root directory?")

            self.configure_ac().set_unique_file_in_srcdir('/'.join(unique_file.relpath(self.package().rootdirectory())))

            pass


        # add Confix2.dir to the distribution package - but only if it
        # is part of the physical package structure
        confix2_dir_file = self.parentbuilder().directory().find([const.CONFIX2_DIR])
        if confix2_dir_file is not None and not confix2_dir_file.is_overlayed():
            self.__makefile_am.add_extra_dist(const.CONFIX2_DIR)
            pass


        # finally: if I am in the toplevel directory, write
        # configure.ac and acinclude.m4
        if self.parentbuilder() is self.package().rootbuilder():
            configure_ac_file = self.package().rootdirectory().find(['configure.ac'])
            if configure_ac_file is None:
                configure_ac_file = self.package().rootdirectory().add(name='configure.ac', entry=File())
            else:
                configure_ac_file.truncate()
                pass
            configure_ac_file.add_lines(self.configure_ac().lines())

            acinclude_m4_file = self.package().rootdirectory().find(['acinclude.m4'])
            if acinclude_m4_file is None:
                acinclude_m4_file = self.package().rootdirectory().add(name='acinclude.m4', entry=File())
            else:
                acinclude_m4_file.truncate()
                pass
            acinclude_m4_file.add_lines(self.__acinclude_m4.lines())
            pass

        # finally: write Makefile.am
        if True:
            mf_am = self.parentbuilder().directory().find(['Makefile.am'])
            if mf_am is None:
                mf_am = File()
                self.parentbuilder().directory().add(name='Makefile.am', entry=mf_am)
            else:
                mf_am.truncate()
                pass
            mf_am.add_lines(self.__makefile_am.lines())
            pass

        pass

    pass


class AutoconfAuxDirBuilder(DirectoryBuilder):
    def __init__(self, directory):
        DirectoryBuilder.__init__(self, directory=directory)
        pass

    def output(self):
        super(AutoconfAuxDirBuilder, self).output()
        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        automake_output_builder.configure_ac().set_ac_config_aux_dir(
            '/'.join(self.directory().relpath(self.package().rootdirectory())))
        pass

    def eat_file(self, sourcename, mode):
        basename = os.path.basename(sourcename)
        lines = helper.lines_of_file(sourcename)
        destfile = self.directory().find([basename])
        if destfile is None:
            destfile = self.directory().add(
                name=basename,
                entry=File(mode=mode, lines=lines))
        else:
            destfile.truncate()
            destfile.add_lines(lines)
            pass
        automake_output_builder = find_automake_output_builder(self.parentbuilder())
        automake_output_builder.makefile_am().add_extra_dist(basename)
        pass

    pass
