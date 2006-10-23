# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

from libconfix.core.utils import const
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core import readonly_prefixes
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
        # FIXME (redesign me?): CBaseBuilder's ctor takes care of
        # executing the interface code, thereby eventually manipulating
        # self's exename_ attribute. we have to take care that that
        # attribute is present before the ctor runs. (this is a major
        # violation of the "never get active in the ctor" principle.)
        self.__exename = None

        CBaseBuilder.__init__(self, file=file)
        self.__init_buildinfo()

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
                self.__is_main = helper.search_main(self.file().lines())
                break
            pass
        return self.__is_main

    def cmdlinemacros(self):
        return self.cmdlinemacros_
    def cflags(self):
        return self.cflags_
    def external_include_path(self):
        return self.external_include_path_
        
    def buildinfo_includepath_native_local(self):
        return self.buildinfo_includepath_native_local_

    def buildinfo_includepath_native_installed(self):
        return self.buildinfo_includepath_native_installed_

    def relate(self, node, digraph, topolist):
        CBaseBuilder.relate(self, node, digraph, topolist)
        self.__init_buildinfo()
        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_CIncludePath_NativeLocal):
                    self.buildinfo_includepath_native_local_ += 1
                    continue
                if isinstance(bi, BuildInfo_CIncludePath_NativeInstalled):
                    self.buildinfo_includepath_native_installed_ += 1
                    continue
                if isinstance(bi, BuildInfo_CIncludePath_External):
                    incpath = bi.incpath()
                    key = '.'.join(incpath)
                    if not key in self.have_external_include_path_:
                        self.external_include_path_.insert(0, incpath)
                        self.have_external_include_path_.add(key)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CommandlineMacros):
                    for (k, v) in bi.macros().iteritems():
                        self.__insert_cmdlinemacro(k, v)
                        pass
                    continue
                if isinstance(bi, BuildInfo_CFLAGS):
                    self.cflags_.extend(bi.cflags())
                    continue
                pass
            pass
        pass

    def output(self):
        CBaseBuilder.output(self)

        # native includes of the same packages come first
        if self.buildinfo_includepath_native_local_ > 0:
            self.parentbuilder().makefile_am().add_includepath(
                '-I$(top_builddir)/'+const.LOCAL_INCLUDE_DIR)
            pass
        # native includes of other packages (i.e., native installed
        # includes) come next.
        if self.buildinfo_includepath_native_installed_ > 0:
            self.parentbuilder().makefile_am().add_includepath(
                '-I$(includedir)')
            self.parentbuilder().makefile_am().add_includepath(
                readonly_prefixes.incpath_subst)
            pass
        # external includes.
        for p in self.external_include_path_:
            for item in p:
                self.parentbuilder().makefile_am().add_includepath(item)
                pass
            pass
        # commandline macros
        for macro, value in self.cmdlinemacros_.iteritems():
            self.parentbuilder().makefile_am().add_cmdlinemacro(macro, value)
            pass
        # cflags
        for cflag in self.cflags_:
            self.parentbuilder().makefile_am().add_am_cflags(cflag)
            pass
        pass

    def iface_pieces(self):
        return CBaseBuilder.iface_pieces(self) + [CompiledCBuilderInterfaceProxy(object=self)]

    def __init_buildinfo(self):
        self.buildinfo_includepath_native_local_ = 0
        self.buildinfo_includepath_native_installed_ = 0
        self.cmdlinemacros_ = {}
        self.cflags_ = []

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
        
        self.external_include_path_ = []
        self.have_external_include_path_ = set()

        pass

    def __insert_cmdlinemacro(self, key, value):
        if self.cmdlinemacros_.has_key(key):
            existing_value = self.cmdlinemacros_[key]
            if existing_value != value:
                raise Error(os.sep.join(self.file().relpath())+': '
                            'conflicting values for macro "'+key+'": '
                            '"'+existing_value+'"/"'+value+'"')
            return
        self.cmdlinemacros_[key] = value
    
    pass

class CompiledCBuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('EXENAME', getattr(self, 'EXENAME'))
        pass
    def EXENAME(self, name):
        self.object_.set_exename(name)
        pass
    pass
