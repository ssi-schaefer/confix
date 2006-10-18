# $Id: builder.py,v 1.4 2006/06/21 12:20:10 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

from dependency import Provide_IDL, Require_IDL
from buildinfo import BuildInfo_IDL_NativeLocal
import libconfix.core.helper

from libconfix.buildable_single import BuildableSingle
from libconfix.core.require import Require
import libconfix.helper_c

import os, re

class IDLBuilder(BuildableSingle):

    """ Not a Buildable in a sense that it gets built by a compiler to
    produce object code. Rather, "building" an IDL file involves such
    things as installing (providing) it into certain locations - and
    the terms "providing" and "installing" are especially important
    with Confix.

    This class is essentially a copy of BuildableHeader. Forgive me.
    I couldn't find a way that was viable enough to pull it together
    (other than abusing the header file support of L{the enclosing
    module<modbuild.BuildableModule>}, and various C helper
    functions).

    """

    # provide-modes

    PROVIDE_PUBLIC = 0
    PROVIDE_PACKAGE = 1
    PROVIDE_GUESS = 2
    PROVIDE_NOTATALL = 3

    def __init__(self,
                 dir,
                 filename,
                 lines):

        self.install_path_ = None
        self.provide_mode_ = None

        BuildableSingle.__init__(self,
                                 dir=dir,
                                 filename=filename,
                                 lines=lines)

        # remember the #includes for later use (we generate require
        # objects, and we generate a buildinfo object that carries
        # them). fortunately IDL is similar to C in that it uses the C
        # preprocessor for includes, so we can peruse helper_c.

        self.includes_ = libconfix.helper_c.extract_requires(lines)

        # if no install path was explicitly given, determine one
        # myself.

        if self.install_path_ is None:
            # search lines for a namespace. if one is found, our
            # install path is the namespace (or the concatenation of
            # nested namespaces). if none is found, the file is
            # installed directly into <prefix>/include.

            paths = self.parse_modules_(lines)

            if len(paths) > 1:
                raise Error(self.fullname() + ': error: '
                            'found multiple modules, ' + ', '.join(['::'.join(p) for p in paths]))

            install_path = ''
            if len(paths):
                for p in paths[0]:
                    install_path = os.path.join(install_path, p)

            self.install_path_ = install_path
            pass
        pass

    def provide_mode(self): return self.provide_mode_
    def install_path(self): return self.install_path_
    def set_install_path(self, p): self.install_path_ = p

    def set_provide_mode(self, provide_mode):

        assert provide_mode in [IDLBuilder.PROVIDE_PUBLIC,
                                IDLBuilder.PROVIDE_PACKAGE,
                                IDLBuilder.PROVIDE_GUESS,
                                IDLBuilder.PROVIDE_NOTATALL]
        self.provide_mode_ = provide_mode

##     def consume_fileproperty(self, name, value):

##         if name == FileProperties.PROVIDE_MODE:
##             if type(value) is not types.StringType:
##                 raise Error(self.name()+': file property "'+name+'" '
##                             'must be one of "public", "package", or "guess" '
##                             '(was "'+value+'")')
##             if value == 'public': self.provide_mode_ = IDLBuilder.PROVIDE_PUBLIC
##             elif value == 'package': self.provide_mode_ = IDLBuilder.PROVIDE_PACKAGE
##             elif value == 'guess': self.provide_mode_ = IDLBuilder.PROVIDE_GUESS
##             else:
##                 raise Error(self.name()+': file property "'+name+'" '
##                             'must be one of "public", "package", or "guess" '
##                             '(was "'+value+'")')

##         if name == FileProperties.INSTALL_PATH:
##             if type(value) is not types.StringType:
##                 raise Error(self.name()+': file property "'+name+'" must be a string')
##             self.install_path_ = value

##         BuildableSingle.consume_fileproperty(self, name, value)

    def validate(self):

        BuildableSingle.validate(self)

        # if we don't have an install path yet, we can do nothing but
        # install ourselves into $(includedir) directly.

        if not self.install_path_:
            self.install_path_ = ''

        # see how we will be providing ourselves to other modules. if
        # we were told to guess, we provide ourselves package-locally
        # if the file name starts with an underline. else, we install
        # the file publicly.

        if self.provide_mode_ in [None, IDLBuilder.PROVIDE_GUESS]:
            self.provide_mode_ = self.filename().startswith('_') and \
                                 IDLBuilder.PROVIDE_PACKAGE or \
                                 IDLBuilder.PROVIDE_PUBLIC
            pass

        external_name = os.path.join(self.install_path(), self.filename())
        internal_name = self.filename()

        if self.provide_mode_ == IDLBuilder.PROVIDE_PACKAGE:
            self.add_package_provide(Provide_IDL(external_name))
        elif self.provide_mode_ == IDLBuilder.PROVIDE_PUBLIC:
            self.add_public_provide(Provide_IDL(external_name))
        elif self.provide_mode_ == IDLBuilder.PROVIDE_NOTATALL:
            pass
        else: assert 0

        if external_name != internal_name:
            self.add_internal_provide(Provide_IDL(internal_name))
            
        for inc in self.includes_:
            self.add_require(Require_IDL(filename=inc,
                                         found_in=os.path.join(self.dir(), self.filename()),
                                         urgency=Require.URGENCY_WARN))
            pass
        
        self.add_buildinfo(
            BuildInfo_IDL_NativeLocal(filename=os.path.join(self.install_path(),
                                                            self.filename()),
                                      includes=self.includes_))

    def contribute_makefile_am(self, buildmod):

        BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

        buildmod.makefile_am().add_extra_dist(self.filename())

        buildmod.file_installer().add_private_header(
            filename=self.filename(),
            dir=self.install_path())

        if self.provide_mode_ == IDLBuilder.PROVIDE_PUBLIC:
            buildmod.file_installer().add_public_header(
                filename=self.filename(),
                dir=self.install_path())
            pass
        pass

    re_beg_mod_ = re.compile(r'^\s*module(.*){')
    re_beg_mod_named_ = re.compile(r'^\s*(\w+)')
    re_end_mod_ = re.compile(r'^\s*}\s*;?\s*//.*(end of|/)\s*module')

    def parse_modules_(self, lines):

        stack_growth = 0
        stack = []
        found_modules = []

        lineno = 0
        for l in lines:
            lineno = lineno + 1
            m = IDLBuilder.re_beg_mod_.search(l)
            if m:
                n = IDLBuilder.re_beg_mod_named_.search(m.group(1))
                mod_name = n and n.group(1) or ''
                stack.append(mod_name)
                stack_growth = 1
                continue

            m = IDLBuilder.re_end_mod_.search(l)            
            if m:
                if len(stack) == 0:
                    raise Error(self.fullname() + ':' + str(lineno) + ': error: '
                                'end of module found though none was begun')
                if stack_growth == 1 and len(stack[-1]) > 0:
                    found_modules.append(stack[0:]) # copy, not just ref
                del stack[-1]
                stack_growth = 0
                continue

        if len(stack):
            raise Error(self.fullname()+': error: '
                        'module \''+'::'.join(stack)+'\' was opened but not closed '
                        '(remember, you have to close it with a line like \'} // /module\')')

        return found_modules
    pass
