# $Id: buildable.py,v 1.38 2006/06/21 11:06:49 jfasch Exp $

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

import core.debug

from core.require import Require
from buildinfo_common import BuildInfo_Configure_in, BuildInfo_ACInclude_m4
from paragraph import Paragraph, ParagraphSet, OrderedParagraphSet
from core.depinfo import DependencyInformation
from core.buildinfoset import BuildInformationSet
from core.marshalling import Unmarshallable

class Buildable(Unmarshallable):

    """ Objects of type Buildable participate in the build process in
    many ways. Their main responsibility is to generate build
    instructions for their type of output, and to a great part they
    achieve that task by talking to other objects.

    For one, most objects of this type are L{single-file
    objects<buildable_single.BuildableSingle>}. These objects are
    responsible for guiding a file through its build. As such, they
    see the source code of that file and can parse it for L{dependency
    information<require.Require>}.

    For another, some objects of this type are composite objects of
    some kind, and contribute build information to other
    buildables. They do this through the use of
    L{<buildinfo.BuildInformation>} objects that they register with
    their managing L{module<modbuild.BuildableModule>}. See
    L{BuildableLibrary<buildable_library.BuildableLibrary>} for a
    buildable type that is both responsible for building a library
    from a set of compiled object files, and that is responsible for
    telling other buildables how to use that library. """

    def __init__(self, name, dir):

        """ Create a new buildable object with the given name, located
        in the given directory.

        @type  name: string

        @param name: The name of the new object. This should ideally
        be unique within the buildable's containing L{module
        <modbase.ModuleBase>}.

        @type  dir: string

        @param dir: The directory where this buildable is
        located. This is a relative path from the package's root
        source directory. """

        self.name_ = name
        self.dir_ = dir
        self.validated_ = 0
        self.dep_info_ = DependencyInformation()
        self.buildinfos_ = BuildInformationSet()

        # this is information we receive from our fellow modules in
        # the dependency graph.

        self.foreign_configure_in_ = OrderedParagraphSet()
        self.foreign_acinclude_m4_ = ParagraphSet()

        # this is information we have gathered locally

        self.local_configure_in_ = OrderedParagraphSet()
        self.local_acinclude_m4_ = ParagraphSet()
        
    def name(self):

        """ Get this buildable object's name.

        @rtype: string
        @return: The name of this object.
        """

        return self.name_

    def dir(self):
        """
        Get the directory in which the buildable lives. (This is the same as the
        owning module's directory.)

        @rtype: string
        @return: The buildable's directory.
        """

        assert self.dir_ is not None
        return self.dir_

    def add_require(self, r):
        self.dep_info_.add_require(r)

    def add_requires(self, r):

        self.dep_info_.add_requires(r)
        pass

    def add_provide(self, p):
        self.dep_info_.add_provide(p)

    def add_public_provide(self, p):
        core.debug.warn('Buildable.add_public_provide(): use add_provide()')
        self.add_provide(p)

    def add_package_provide(self, p):
        core.debug.warn('Buildable.add_package_provide(): use add_provide()')
        self.add_provide(p)

    def add_internal_provide(self, p):

        self.dep_info_.add_internal_provide(p)

    def add_buildinfo(self, b):
        self.buildinfos_.add(b)
        pass
    def buildinfos(self):
        return self.buildinfos_

    def add_local_configure_in(self, paragraph, order):
        self.local_configure_in_.add(paragraph=paragraph, order=order)
        pass

    def add_local_acinclude_m4(self, paragraph):
        self.local_acinclude_m4_.add(paragraph)
        pass

    def add_foreign_configure_in(self, paragraph, order):
        self.foreign_configure_in_.add(paragraph=paragraph, order=order)
        pass

    def add_foreign_acinclude_m4(self, paragraph):
        self.foreign_acinclude_m4_.add(paragraph)
        pass

    def validate(self):

        """ Called after the initial scanning work is done. To be
        overloaded by derived classes, and by derived classes of
        derived classes, and so on.

        B{Caution}: in overloading implementations, be sure to call
        the overloaded bases class method, so that all classes in the
        inheritance chain get the opportunity to do their work. """

        self.validated_ = 1

    def validated(self): return self.validated_

    def world(self, modules):

        """ A chance to look at all modules which are considered for
        the dependency graph, just before the modules will be talking
        to each other to build the graph. """

        pass

    def gather_build_info(self, modules):
        for m in modules:
            for bi in m.buildinfos():
                if isinstance(bi, BuildInfo_Configure_in):
                    self.add_foreign_configure_in(paragraph=Paragraph(lines=bi.lines()),
                                                  order=bi.order())
                elif isinstance(bi, BuildInfo_ACInclude_m4):
                    self.add_foreign_acinclude_m4(paragraph=Paragraph(lines=bi.lines()))
                    pass
                pass
            pass
        pass

    def reset_build_infos(self):

        self.foreign_configure_in_ = OrderedParagraphSet()
        self.foreign_acinclude_m4_ = ParagraphSet()

    def gather_handled_files(self):

        """ When the L{package <package.Package>} writes the
        configure.in file, it needs as input to the AC_CONFIG_SRCDIR
        macro one unique file which is present in the source
        tree. (The purpose of this macro is to perform sanity checks,
        and among other things it asserts that the file is present.)
        Anyway, this method is here for no other purpose than to
        satisfy AC_CONFIG_SRCDIR.

        @return: a list of filenames. Most of the time this list
        contain at most one item, but, for the sake of generality ...

        """

        return []

    def contribute_makefile_am(self, buildmod):

        """ This ends the game. Everything which is relevant for the
        build is in place, the dependency graph has settled, and we
        are ready to write down build instructions into the L{module's
        <modbuild.BuildableModule>} Makefile.am. """

        assert self.validated_, self.name()
        pass

    def get_dependency_info(self):
        return self.dep_info_

    def gather_configure_in(self):

        """ Just like L{contribute_makefile_am}, but for the L{package's
        <package.Package>} configure.in instead. """

        ret = OrderedParagraphSet()
        ret.update(self.local_configure_in_)
        ret.update(self.foreign_configure_in_)
        return ret

    def gather_acinclude_m4(self):

        """ Just like L{contribute_makefile_am}, but for the L{package's
        <package.Package>} acinclude.m4 instead. """

        return self.local_acinclude_m4_ + self.foreign_acinclude_m4_

    def generate_buildables(self):

        """ Generate (that is, return) a (possibly empty) list of
        buildables. This the primary building block of generated
        files, such as .c and .h files that are generated by Lex or
        Yacc source files. """

        return []
