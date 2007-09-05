# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery import readonly_prefixes
from libconfix.core.utils import const
import libconfix.core.utils.helper

from base import CBaseBuilder
from buildinfo import \
     BuildInfo_CIncludePath_NativeLocal, \
     BuildInfo_CIncludePath_NativeInstalled, \
     BuildInfo_CIncludePath_External, \
     BuildInfo_CommandlineMacros, \
     BuildInfo_CFLAGS

import helper

class CompiledCBuilder(CBaseBuilder):

    MAIN_PROPERTY_NAME = 'MAIN'
    
    def __init__(self, file):
        CBaseBuilder.__init__(self, file=file)
        self.__init_buildinfo()

        self.__exename = None

        # tri-state: None - haven't looked yet, True, False
        self.__is_main = None
        pass

    def exename(self):
        return self.__exename

    def set_exename(self, name):
        assert self.__exename is None
        self.__exename = name
        pass

    def is_main(self):
        if self.__is_main is None:
            while True:
                if self.__exename is not None:
                    self.__is_main = True
                    break
                prop_main = self.file().get_property(self.MAIN_PROPERTY_NAME)
                if prop_main is not None:
                    self.__is_main = libconfix.core.utils.helper.read_boolean(prop_main)
                    break
                if helper.search_main(self.file().lines()):
                    self.__is_main = True
                    pass
                break
            pass
        return self.__is_main

    def cmdlinemacros(self):
        return self.__cmdlinemacros
    def cflags(self):
        return self.__cflags
    def external_include_path(self):
        return self.__external_include_path

    def native_local_include_dirs(self):
        return self.__native_local_include_dirs

    def buildinfo_includepath_native_installed(self):
        return self.__buildinfo_includepath_native_installed

    def relate(self, node, digraph, topolist):
        CBaseBuilder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                    if bi.include_dir() is None:
                        self.__have_locally_installed_includes = True
                    else:
                        key = '.'.join(bi.include_dir())
                        if key not in self.__have_native_local_include_dirs:
                            self.__have_native_local_include_dirs.add(key)
                            self.__native_local_include_dirs.insert(0, bi.include_dir())
                            pass
                        pass
                    continue
                if isinstance(bi, BuildInfo_CIncludePath_NativeInstalled):
                    self.__buildinfo_includepath_native_installed = True
                    continue
                if isinstance(bi, BuildInfo_CIncludePath_External):
                    incpath = bi.incpath()
                    key = '.'.join(incpath)
                    if not key in self.__have_external_include_path:
                        self.__external_include_path.insert(0, incpath)
                        self.__have_external_include_path.add(key)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CommandlineMacros):
                    for (k, v) in bi.macros().iteritems():
                        self.__insert_cmdlinemacro(k, v)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CFLAGS):
                    self.__cflags.extend(bi.cflags())
                    continue
                pass
            pass
        pass

    def output(self):
        CBaseBuilder.output(self)

        # native includes of the same package come first
        if len(self.__native_local_include_dirs) > 0:
            for d in self.__native_local_include_dirs:
                self.parentbuilder().makefile_am().add_includepath('-I'+'/'.join(['$(top_srcdir)']+d))
                pass
            pass
        if self.__have_locally_installed_includes:
            self.parentbuilder().makefile_am().add_includepath('-I'+'/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR]))
            pass
        # native includes of other packages (i.e., native installed
        # includes) come next.
        if self.__buildinfo_includepath_native_installed:
            self.parentbuilder().makefile_am().add_includepath(
                '-I$(includedir)')
            self.parentbuilder().makefile_am().add_includepath(
                '$('+readonly_prefixes.incpath_var+')')
            pass
        # external includes.
        for p in self.__external_include_path:
            for item in p:
                self.parentbuilder().makefile_am().add_includepath(item)
                pass
            pass
        # commandline macros
        for macro, value in self.__cmdlinemacros.iteritems():
            self.parentbuilder().makefile_am().add_cmdlinemacro(macro, value)
            pass
        # cflags
        for cflag in self.__cflags:
            self.parentbuilder().makefile_am().add_am_cflags(cflag)
            pass
        pass

    def iface_pieces(self):
        return CBaseBuilder.iface_pieces(self) + [CompiledCBuilderInterfaceProxy(object=self)]

    def __init_buildinfo(self):
        # a list of directories in the local package that have to be
        # added to the include path. (we are only adding them once,
        # thus the have_... set.) Note that these are the include
        # directories from the source tree only. 
        self.__native_local_include_dirs = []
        self.__have_native_local_include_dirs = set()

        # a flag that signals us that we have to add to the include
        # path the directory where the locally installed headers are.
        self.__have_locally_installed_includes = False

        # a flag that indicates that there are installed header files
        # being used (and thus the public include directory (or
        # whatever the backend's notion thereof) hs to be added to the
        # include path).
        self.__buildinfo_includepath_native_installed = False

        # macro definitions for the compiler's command line.
        self.__cmdlinemacros = {}

        # more compiler commandline options.
        self.__cflags = []

        # include path for external modules. this is a list of lists,
        # of the form

        # [['-I/dir1'],
        #  ['-I/this/dir/include', '-I/that/dir/include']]

        # each list has been distributed to us by one module, and we
        # must not change the order inside the individual lists - they
        # may be significant, and the distributing modules surely
        # don't expect us to mess with the order.

        # the complete list is accompanied with a set which serves us
        # to sort out duplicates from the beginning.
        
        self.__external_include_path = []
        self.__have_external_include_path = set()

        pass

    def __insert_cmdlinemacro(self, key, value):
        if self.__cmdlinemacros.has_key(key):
            existing_value = self.__cmdlinemacros[key]
            if existing_value != value:
                raise Error(os.sep.join(self.file().relpath())+': '
                            'conflicting values for macro "'+key+'": '
                            '"'+existing_value+'"/"'+value+'"')
            return
        self.__cmdlinemacros[key] = value
    
    pass

class CompiledCBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object=object)
        self.add_global('EXENAME', getattr(self, 'EXENAME'))
        pass
    def EXENAME(self, name):
        self.object().set_exename(name)
        pass
    pass
