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

from dependency import \
     Require_IDL, \
     Provide_IDL
from buildinfo import \
     BuildInfo_IDL_NativeLocal, \
     BuildInfo_IDL_NativeInstalled

from libconfix.core.machinery.dependency_utils import DependencyInformation
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.machinery.require import Require
from libconfix.core.utils.error import Error

import libconfix.plugins.c.helper

from libconfix.plugins.automake.out_automake import find_automake_output_builder

import re
import os

class IDLBuilder(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        self.__includes = []
        self.__install_path = []
        pass

    def shortname(self):
        return 'IDL.Builder'

    def initialize(self, package):
        super(IDLBuilder, self).initialize(package)
        
        lines = self.file().lines()

        # remember the #includes for later use (we generate require
        # objects, and we generate a buildinfo object that carries
        # them). fortunately IDL is similar to C in that it uses the C
        # preprocessor for includes, so we can use the C plugin for
        # that.

        self.__includes = [i for i in libconfix.plugins.c.helper.iter_includes(lines)]

        # search lines for a namespace. if one is found, our install
        # path is the namespace (or the concatenation of nested
        # namespaces). if none is found, the file is installed
        # directly into <prefix>/include.
        
        paths = self.parse_modules_(lines)
        if len(paths) > 1:
            raise Error(os.sep.join(self.file().relpath(self.package().rootdirectory())) + ': error: '
                        'found multiple modules, ' + ', '.join(['::'.join(p) for p in paths]))
        if len(paths):
            for p in paths[0]:
                self.__install_path.append(p)
                pass
            pass

        self.add_buildinfo(
            BuildInfo_IDL_NativeLocal(filename='/'.join(self.__install_path + [self.file().name()]),
                                      includes=self.__includes))
        pass

    def dependency_info(self):
        ret = DependencyInformation()
        ret.add(super(IDLBuilder, self).dependency_info())

        external_name = '/'.join(self.__install_path + [self.file().name()])
        internal_name = self.file().name()

        ret.add_provide(Provide_IDL(external_name))
        if external_name != internal_name:
            ret.add_internal_provide(Provide_IDL(internal_name))
            pass
            
        for inc in self.__includes:
            ret.add_require(Require_IDL(filename=inc,
                                         found_in='/'.join(self.file().relpath(self.package().rootdirectory())),
                                         urgency=Require.URGENCY_WARN))
            pass
        return ret

    def install_path(self):
        return self.__install_path

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
                    raise Error('/'.join(self.file().relpath(self.package().rootdirectory())) + ':' + \
                                str(lineno) + ': error: '
                                'end of module found though none was begun')
                if stack_growth == 1 and len(stack[-1]) > 0:
                    found_modules.append(stack[0:]) # copy, not just ref
                del stack[-1]
                stack_growth = 0
                continue

        if len(stack):
            self.__install_path = []
            pass

        return found_modules
    pass
