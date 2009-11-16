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

from libconfix.core.machinery.interface import InterfaceProxy
from libconfix.core.utils import const
import libconfix.core.utils.helper

from base import CBaseBuilder
from buildinfo import \
     BuildInfo_CIncludePath_NativeLocal, \
     BuildInfo_CIncludePath_NativeInstalled, \
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

        # maybe somebody has taken for granted that I have or don't
        # have main().
        self.__is_main = None
        self.force_enlarge()
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
                    break
                self.__is_main = False
                break
            pass
        return self.__is_main

    def cmdlinemacros(self):
        """
        Compiler commandline macros (usually passed to the compiler
        like -Dname=value, or -Dname) are tuples of the form (name,
        value). Both are strings, and value can be None if -Dname is
        desired.

        Returns an dictionary {name: value}, where value can be None.
        """
        return self.__cmdlinemacros
    
    def cflags(self):
        """
        Flags for every C-like compilation (which can be C, C++, or
        even Lex and Yacc).

        Returns a list of strings that are passed to the compiler
        literally.
        """
        return self.__cflags

    def native_local_include_dirs(self):
        """
        List of package-local directories that have to put on the
        compiler command line, as include path. In good old tradition,
        this is a list of lists of strings.
        """
        return self.__native_local_include_dirs

    def have_locally_installed_includes(self):
        """
        Are there locally installed headers?
        """
        return self.__have_locally_installed_includes

    def using_native_installed(self):
        return self.__buildinfo_includepath_native_installed

    def relate(self, node, digraph, topolist):
        CBaseBuilder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()
        for n in topolist:
            for bi in n.iter_buildinfos_type(BuildInfo_CIncludePath_NativeLocal):
                if bi.include_dir() is None:
                    self.__have_locally_installed_includes = True
                else:
                    key = '.'.join(bi.include_dir())
                    if key not in self.__have_native_local_include_dirs:
                        self.__have_native_local_include_dirs.add(key)
                        self.__native_local_include_dirs.insert(0, bi.include_dir())
                        pass
                    pass
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_CIncludePath_NativeInstalled):
                self.__buildinfo_includepath_native_installed = True
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_CommandlineMacros):
                for (k, v) in bi.macros().iteritems():
                    self.__insert_cmdlinemacro(k, v)
                    pass
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_CFLAGS):
                self.__cflags.extend(bi.cflags())
                pass
            pass
        pass

    def iface_pieces(self):
        return CBaseBuilder.iface_pieces(self) + [CompiledCBuilderInterfaceProxy(builder=self)]

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
    
    pass

class CompiledCBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)
        self.__builder = builder
        self.add_global('EXENAME', getattr(self, 'EXENAME'))
        pass
    def EXENAME(self, name):
        self.__builder.set_exename(name)
        pass
    pass
