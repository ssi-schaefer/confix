# $Id: buildable_h.py,v 1.51 2006/06/21 12:20:11 jfasch Exp $

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
import re
import types

from buildable_c_base import BuildableCBase
from buildable_mgr_bases import BuildableCreator
from provide_h import Provide_CInclude
from fileprops import FileProperties
from core.error import Error
from buildinfo_common import BuildInfo_CIncludePath_NativeLocal
import buildinfo_common
import plugins.c.namespace

class BuildableHeaderCreator(BuildableCreator):
    def create_from_file(self, dir, filename, lines):
        if self.is_valid_ext(filename):
            return BuildableHeader(
                dir=dir,
                filename=filename,
                lines=lines)
        return None

    def is_valid_ext(self, filename):
        return filename.endswith('.h') or filename.endswith('.hpp')

class BuildableHeader(BuildableCBase):

    """ Not a Buildable in a sense that it gets built by a compiler to
    produce object code. Rather, "building" a header file involves
    such things as installing (providing) it into certain locations -
    and the terms "providing" and "installing" are especially
    important with Confix. """

    # provide-modes

    PROVIDE_PUBLIC = 0
    PROVIDE_PACKAGE = 1
    PROVIDE_GUESS = 2
    PROVIDE_NOTATALL = 3

    def __init__(self,
                 dir,
                 filename,
                 lines,
                 provide_mode=PROVIDE_GUESS):

        """
        
        @type dir: string

        @param dir: directory name, relative from the package root
        directory

        @type filename: string

        @param filename: the header file's name


        @param provide_mode: selects how our provide object is handed
        out to our module, and what install rules to inject into the
        module's Makefile.am.

          - PROVIDE_PUBLIC: the provide object is handed out publicly;
            that is, even the installed incarnation of the module will
            have it. Install rules are generated for both the public
            location ($(includedir)), and the package-local location.

          - PROVIDE_PACKAGE: the header file is only made visible
            package-locally, and so is the provide object. The
            installed module will not contain a provide object.

          - PROVIDE_GUESS: guess whether the effective provide-mode
            will be PROVIDE_PUBLIC or PROVIDE_PACKAGE. Currently,
            files that start with '_' are PROVIDE_PACKAGE, all other
            are PROVIDE_PUBLIC.

          - PROVIDE_NOTATALL: nothing is done at all, the file is left
            alone. No provide object is generated, the file is not
            installed. This has the effect that the file is only seen
            during the compilation of the module.

            Setting this provide mode makes sense when a module builds
            executables. This prevents it from building libraries, and
            therefore it does not make sense at all to install any
            header files - they are considered part of the
            implementation of the executables, and by no means an
            interface. Alas, the
            L{buildables<buildable_exe.BuildableExecutable>} that are
            responsible for the executables set PROVIDE_NOTATALL for
            all header files in their module.

        @type provide_mode: integer

        """

        self.install_path_ = None
        self.provide_mode_ = None
        self.set_provide_mode(provide_mode)

        BuildableCBase.__init__(self,
                                dir=dir,
                                filename=filename,
                                lines=lines,
                                search_for_main=False)

        # if no install path was explicitly set in th ebuildable iface
        # (which is evaluated by BuildableCBase), determine one
        # myself.

        if self.install_path_ is None:

            # search lines for a namespace. if one is found, our
            # install path is the namespace (or the concatenation of
            # nested namespaces). if none is found, the file is
            # installed directly into <prefix>/include.

            paths = plugins.c.namespace.find_namespaces(lines)

            if len(paths) > 1:
                raise Error(self.fullname() + ': error: '
                            'found multiple namespaces, ' + ', '.join(['::'.join(p) for p in paths]))
            elif len(paths) == 1:
                self.install_path_ = '/'.join(paths[0])
            else:
                self.install_path_ = ''

    def __repr__(self):
        return self.__class__.__name__ + ' ' + self.name()

    def provide_mode(self): return self.provide_mode_
    def install_path(self): return self.install_path_
    def set_install_path(self, p): self.install_path_ = p

    def set_provide_mode(self, provide_mode):

        assert provide_mode in [BuildableHeader.PROVIDE_PUBLIC,
                                BuildableHeader.PROVIDE_PACKAGE,
                                BuildableHeader.PROVIDE_GUESS,
                                BuildableHeader.PROVIDE_NOTATALL]
        self.provide_mode_ = provide_mode

    def consume_fileproperty(self, name, value):

        # overloaded from the base class. though we may have seen the
        # word 'main' in the file, we know that we do not want a
        # header file to be considered the main() of an executable.

        if name in [FileProperties.MAIN, FileProperties.EXENAME]:
            raise Error(self.name()+' cannot have property '+name)

        if name == FileProperties.PROVIDE_MODE:
            if type(value) is not types.StringType:
                raise Error(self.name()+': file property "'+name+'" '
                            'must be one of "public", "package", or "guess" '
                            '(was "'+value+'")')
            if value == 'public': self.provide_mode_ = BuildableHeader.PROVIDE_PUBLIC
            elif value == 'package': self.provide_mode_ = BuildableHeader.PROVIDE_PACKAGE
            elif value == 'guess': self.provide_mode_ = BuildableHeader.PROVIDE_GUESS
            else:
                raise Error(self.name()+': file property "'+name+'" '
                            'must be one of "public", "package", or "guess" '
                            '(was "'+value+'")')

        if name == FileProperties.INSTALL_PATH:
            if type(value) is not types.StringType:
                raise Error(self.name()+': file property "'+name+'" must be a string')
            self.install_path_ = value

        BuildableCBase.consume_fileproperty(self, name, value)

    def validate(self):

        # if we don't have an install path yet, we can do nothing but
        # install ourselves into $(includedir) directly.

        if not self.install_path_:
            self.install_path_ = ''

        # see how we will be providing ourselves to other modules. if
        # we were told to guess, we provide ourselves package-locally
        # if the file name starts with an underline. else, we install
        # the file publicly.

        if self.provide_mode_ in [None, BuildableHeader.PROVIDE_GUESS]:
            self.provide_mode_ = self.filename().startswith('_') and \
                                 BuildableHeader.PROVIDE_PACKAGE or \
                                 BuildableHeader.PROVIDE_PUBLIC

        # now that we filled in the missing pieces of information, do
        # some meaningful things.

        external_name = os.path.join(self.install_path(), self.filename())# copied to plugins.c.h
        internal_name = self.filename()# copied to plugins.c.h

##         if self.provide_mode_ == BuildableHeader.PROVIDE_PACKAGE:
##             self.add_package_provide(Provide_CInclude(external_name))
##         elif self.provide_mode_ == BuildableHeader.PROVIDE_PUBLIC:
##             self.add_public_provide(Provide_CInclude(external_name))
##         elif self.provide_mode_ == BuildableHeader.PROVIDE_NOTATALL:
##             pass
##         else: assert 0

        self.add_provide(Provide_CInclude(external_name))# copied to plugins.c.h
# copied to plugins.c.h
        # we are always providing ourselves to other buildables in the# copied to plugins.c.h
        # same module. the difference between this and providing to# copied to plugins.c.h
        # other modules (package-local, or public) is that the file is# copied to plugins.c.h
        # included by others AS-IS. that is, while other modules# copied to plugins.c.h
        # include it like <x/y/file.h>, the local files include it# copied to plugins.c.h
        # like "file.h".# copied to plugins.c.h
# copied to plugins.c.h
        if external_name != internal_name:# copied to plugins.c.h
            self.add_internal_provide(Provide_CInclude(internal_name))# copied to plugins.c.h

        # this is a boilerplate kind of thing which every
        # BuildableHeader does the same way, and the objects do not
        # differ in any way. so we use a singleton, rather than
        # instantiating a new object for every single fart.

        self.add_buildinfo(buildinfo_common.buildinfo_cincludepath_nativelocal)

        BuildableCBase.validate(self)

    def contribute_makefile_am(self, buildmod):

        # perform the basic C stuff, using our base class

        BuildableCBase.contribute_makefile_am(self, buildmod=buildmod)

        # make the file visible to fellow modules in the same
        # package. they should see the file the same way as foreign
        # modules would see it after installation. for example, if the
        # file was to be visible as #include <x/y/file.h> after
        # installation, we'd have to arrange for it to be visible the
        # same way from a fellow module.

        # attention, we may have to install generated files, and the
        # location they live in is different from that of regular
        # (hand-written) files: regular files live in
        # '@srcdir@'. generated files live in '@builddir@' (which is a
        # synonym for '.' - the directory that 'make' is in during
        # compilation).

        buildmod.file_installer().add_private_header(
            filename=self.filename(),
            dir=self.install_path())

        # if our file is to be publicly visible, we tell our module to
        # make it so.
        
        if self.provide_mode_ == BuildableHeader.PROVIDE_PUBLIC:
            buildmod.file_installer().add_public_header(
                filename=self.filename(),
                dir=self.install_path())
            pass
        pass
    pass


# moved to plugins.c.namespace.find_namespaces

## _re_beg_ns = re.compile(r'^\s*namespace(.*){')
## _re_beg_ns_named = re.compile(r'^\s*(\w+)')
## _re_end_ns = re.compile(r'^\s*}\s*;?\s*//.*(end of|/)\s*namespace')

## def _namespaces(filename, lines):

##     stack_growth = 0
##     stack = []
##     found_namespaces = []

##     lineno = 0
##     for l in lines:
##         lineno = lineno + 1
##         m = _re_beg_ns.search(l)
##         if m:
##             n = _re_beg_ns_named.search(m.group(1))
##             ns_name = n and n.group(1) or ''
##             stack.append(ns_name)
##             stack_growth = 1
##             continue

##         m = _re_end_ns.search(l)            
##         if m:
##             if len(stack) == 0:
##                 raise Error(filename + ':' + str(lineno) + ': error: '
##                             'end of namespace found though none was begun')
##             if stack_growth == 1 and len(stack[-1]) > 0:
##                 found_namespaces.append(stack[0:]) # copy, not just ref
##             del stack[-1]
##             stack_growth = 0
##             continue

##     if len(stack):
##         raise Error(filename+': error: '
##                     'namespace \''+'::'.join(stack)+'\' was opened but not closed '
##                     '(remember, you have to close it with a line like \'} // /namespace\')')

##     return found_namespaces
