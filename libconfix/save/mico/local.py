# $Id: local.py,v 1.1 2005/12/20 15:39:58 jfasch Exp $

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

from libconfix.plugins.idl.dependency import \
     Require_IDL
from libconfix.plugins.idl.buildinfo import \
     BuildInfo_IDL_NativeLocal, \
     BuildInfo_IDL_NativeInstalled
import libconfix.plugins.idl.helper

from libconfix.paragraph import OrderedParagraphSet, Paragraph
from libconfix.buildable_single import BuildableSingle
from libconfix.buildable_h import BuildableHeader
from libconfix.buildable_cxx import BuildableCXX
from libconfix.require_h import Require_CInclude
from libconfix.require import Require
import libconfix.helper_configure_in
import libconfix.readonly_prefixes
import libconfix.helper_c
import libconfix.const
import libconfix.debug

import os

class LocalMicoIDLGenerator(BuildableSingle):

    # idl --codegen-c++ --relative-paths --any --typecode -I /home/jfasch/compile/wamas-nightly/plugin-mico-test/confix_include localinterface.idl

    def __init__(self, dir, filename, lines):
        BuildableSingle.__init__(self, dir=dir, filename=filename, lines=lines)

        # the file we use as a witness to watch the IDL compiler's
        # side effect of generating its output files.

        self.witness_file_ = filename + '.witness'

        # builders for our generated files, plus a flag (we must
        # generate only once).

        base, ext = os.path.splitext(os.path.basename(filename))
        self.generated_h_ = BuildableHeader(dir=self.dir(),
                                            filename=base+'.h',
                                            lines=[])
        self.generated_h_.set_install_path(
            libconfix.plugins.idl.helper.install_path(lines=lines, filename=self.fullname()))
        self.generated_cxx_ = BuildableCXX(dir=self.dir(),
                                           filename=base+'.cc',
                                           lines=[])
        self.generated_ = False

        # both of the builders require CORBA.h.

        require_corba_h = Require_CInclude(filename='CORBA.h',
                                           found_in=os.path.join(self.dir(), self.filename()),
                                           urgency=Require.URGENCY_WARN)
        self.generated_h_.add_require(require_corba_h)
        self.generated_cxx_.add_require(require_corba_h)

        # the IDL file's #include<>s make dependencies for both the
        # IDL compiler and the C++ compiler.

        includes = libconfix.helper_c.extract_requires(lines)

        for inc in includes:
            self.add_require(
                Require_IDL(filename=inc,
                            found_in=os.path.join(self.dir(), self.filename()),
                            urgency=Require.URGENCY_WARN))

            base, ext = os.path.splitext(inc)
            c_inc = base + '.h'
            require = Require_CInclude(filename=c_inc,
                                       found_in=c_inc+' (generated from '+filename+')',
                                       urgency=Require.URGENCY_ERROR)
            self.generated_h_.add_require(require)
            self.generated_cxx_.add_require(require)
            pass

        # build information I collect from fellow modules that happen
        # to carry IDL files.

        self.using_native_local_idl_ = False
        self.using_native_installed_idl_ = True

        pass

    def generate_buildables(self):
        if self.generated_:
            return []
        else:
            self.generated_ = True
            return [self.generated_h_, self.generated_cxx_]
        pass

    def gather_build_info(self, modules):
        for m in modules:
            for bi in m.buildinfos():
                if isinstance(bi, BuildInfo_IDL_NativeLocal):
                    self.using_native_local_idl_ = True
                    pass
                elif isinstance(bi, BuildInfo_IDL_NativeInstalled):
                    self.using_native_installed_idl_ = True
                    pass
                pass
            pass
        pass

    def reset_build_infos(self):
        self.using_native_local_idl_ = False
        self.using_native_installed_idl_ = False
        pass

    def contribute_makefile_am(self, buildmod):
        buildmod.makefile_am().add_built_sources(self.generated_h_.filename())
        buildmod.makefile_am().add_built_sources(self.generated_cxx_.filename())

        buildmod.makefile_am().add_lines(libconfix.helper_automake.format_rule(
            targets=[self.generated_h_.filename(), self.generated_cxx_.filename()],
            prerequisites=[self.witness_file_]))
        buildmod.makefile_am().add_extra_dist(self.witness_file_)

        incpath = []
        if self.using_native_local_idl_:
            incpath.append(os.path.join('-I$(top_builddir)', libconfix.const.LOCAL_INCLUDE_DIR))
            pass
        if self.using_native_installed_idl_:
            incpath.append('-I$(includedir)')
            incpath.append(readonly_prefixes.incpath_subst)
            pass

        buildmod.makefile_am().add_lines(libconfix.helper_automake.format_rule(
            targets=[self.witness_file_],
            prerequisites=[self.filename()],
            commands=['idl --codegen-c++ --relative-paths '+' '.join(incpath)+' $(srcdir)/'+self.filename()
                      ]))
