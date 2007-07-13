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

import os
import types

from libconfix.core.utils.error import Error
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core.automake.buildinfo import \
     BuildInfo_Configure_in, \
     BuildInfo_ACInclude_m4

from libconfix.core.iface.proxy import InterfaceProxy

from depinfo import DependencyInformation
from provide import Provide
from provide_string import Provide_String
from provide_callable import Provide_Callable
from provide_symbol import Provide_Symbol
from require import Require
from require_symbol import Require_Symbol
from require_callable import Require_Callable
from buildinfoset import BuildInformationSet

class Builder(object):
    def __init__(self):
        self.__parentbuilder = None
        self.__package = None

        self.__dependency_info = DependencyInformation()

        self.__buildinfos = BuildInformationSet()

        self.__force_enlarge_count = 0

        # flags to ensure that every derived builder's methods have
        # called their immediate base's methods that they overload,
        # and that the chain did reach the base of all builders.
        self.__base_enlarge_called = False
        self.__base_dependency_info_called = False
        self.__base_relate_called = False
        self.__base_output_called = False
        
        pass

    def __str__(self):
        ret = str(self.__class__)
        if self.__parentbuilder is None:
            ret += '(no parent, id='+str(id(self))+')'
        else:
            ret += '('+str(self.__parentbuilder)+')'
            pass
        return ret

    def shortname(self):
        return str(self)

    def locally_unique_id(self):
        """
        A unique, opaque identifier that is supposed to distinguish
        this builder from its brothers in the same directory. Used
        primarily to spot bugs that result from creating the same
        builder twice. To be implemented by derived classes.
        """
        assert False, 'abstract: implement '+str(self.__class__)+'.locally_unique_id()'
        pass
    
    def package(self):
        return self.__package

    def parentbuilder(self):
        return self.__parentbuilder
    def set_parentbuilder(self, parentbuilder):
        self.__parentbuilder = parentbuilder
        pass

    def force_enlarge(self):
        """
        Force one more round.
        """
        self.__force_enlarge_count += 1
        pass
    def force_enlarge_count(self):
        return self.__force_enlarge_count

    def add_require(self, r):
        self.__dependency_info.add_require(r)
        pass
    def add_provide(self, p):
        self.__dependency_info.add_provide(p)
        pass
    def add_internal_provide(self, p):
        self.__dependency_info.add_internal_provide(p)
        pass

    def dependency_info(self):
        self.__base_dependency_info_called = True
        return self.__dependency_info

    def add_buildinfo(self, b):
        self.__buildinfos.add(b)
        pass

    def is_initialized(self):
        """
        See initialize().
        """
        return self.__package is not None

    def initialize(self, package):
        """
        Initialize the builder object; called once in an object's
        lifetime.

        The base class implementation does nothing but remembering the
        package. Derived classes may implement something complicated
        like parsing their file's content for confix calls, or
        searching for C++ namespace definitions, or whatnot.

        It a derived class implements this method, however, it must
        make sure that it hands the call upwards the inheritance
        chain; else, it won't see the package being set.
        """
        assert not self.is_initialized(), self
        self.__package = package
        pass
    
    def buildinfos(self):
        return self.__buildinfos
    
    def enlarge(self):
        self.__base_enlarge_called = True
        pass
    
    def relate(self, node, digraph, topolist):
        self.__base_relate_called = True

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_Configure_in):
                    self.package().configure_ac().add_paragraph(
                        paragraph=Paragraph(lines=bi.lines(), md5=bi.md5()),
                        order=bi.order())
                    continue
                if isinstance(bi, BuildInfo_ACInclude_m4):
                    self.package().acinclude_m4().add_paragraph(
                        paragraph=Paragraph(lines=bi.lines(), md5=bi.md5()))
                    continue
                pass
            pass
        pass

    def node(self):
        return None
    
    def output(self):
        self.__base_output_called = True
        pass

    def iface_pieces(self):
        return [BuilderInterfaceProxy(object=self)]

    # these are mainly for use by test programs, and serve no real
    # functionality
    def base_dependency_info_called(self):
        if self.__base_dependency_info_called:
            self.__base_dependency_info_called = False
            return True
        return False
    def base_enlarge_called(self):
        if self.__base_enlarge_called:
            self.__base_enlarge_called = False
            return True
        return False
    def base_relate_called(self):
        if self.__base_relate_called:
            self.__base_relate_called = False
            return True
        return False
    def base_output_called(self):
        if self.__base_output_called:
            self.__base_output_called = False
            return True
        return False
    
    pass

class BuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object=object)

        # the most basic ones
        self.add_global('PARENTBUILDER', getattr(self, 'PARENTBUILDER'))
        self.add_global('PACKAGE', getattr(self, 'PACKAGE'))

        # PROVIDE, PROVIDE_SYMBOL, and associated flag values
        self.add_global('URGENCY_IGNORE', Require.URGENCY_IGNORE)
        self.add_global('URGENCY_WARN', Require.URGENCY_WARN)
        self.add_global('URGENCY_ERROR', Require.URGENCY_ERROR)
        self.add_global('REQUIRED', Require.URGENCY_ERROR) # backward compat with 1.5
        self.add_global('EXACT_MATCH', Provide_String.EXACT_MATCH)
        self.add_global('PREFIX_MATCH', Provide_String.PREFIX_MATCH)
        self.add_global('GLOB_MATCH', Provide_String.GLOB_MATCH)
        self.add_global('AUTO_MATCH', Provide_String.AUTO_MATCH)

        self.add_global('PROVIDE', getattr(self, 'PROVIDE'))
        self.add_global('REQUIRE', getattr(self, 'REQUIRE'))
        self.add_global('PROVIDE_SYMBOL', getattr(self, 'PROVIDE_SYMBOL'))
        self.add_global('REQUIRE_SYMBOL', getattr(self, 'REQUIRE_SYMBOL'))
        self.add_global('PROVIDE_CALLABLE', getattr(self, 'PROVIDE_CALLABLE'))
        self.add_global('REQUIRE_CALLABLE', getattr(self, 'REQUIRE_CALLABLE'))

        # BUILDINFORMATION
        self.add_global('BUILDINFORMATION', getattr(self, 'BUILDINFORMATION'))

        # CONFIGURE_AC, ACINCLUDE_M4, and associated flag values
        self.add_global('LOCAL', BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL)
        self.add_global('PROPAGATE', BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE)
        self.add_global('AC_BOILERPLATE', Configure_ac.BOILERPLATE)
        self.add_global('AC_OPTIONS', Configure_ac.OPTIONS)
        self.add_global('AC_PROGRAMS', Configure_ac.PROGRAMS)
        self.add_global('AC_LIBRARIES', Configure_ac.LIBRARIES)
        self.add_global('AC_HEADERS', Configure_ac.HEADERS)
        self.add_global('AC_TYPEDEFS_AND_STRUCTURES', Configure_ac.TYPEDEFS_AND_STRUCTURES)
        self.add_global('AC_FUNCTIONS', Configure_ac.FUNCTIONS)
        self.add_global('AC_OUTPUT', Configure_ac.OUTPUT)

        self.add_global('CONFIGURE_AC', getattr(self, 'CONFIGURE_AC'))
        self.add_global('ACINCLUDE_M4', getattr(self, 'ACINCLUDE_M4'))        
        
        pass

    def PARENTBUILDER(self):
        return self.object().parentbuilder()
    def PACKAGE(self):
        return self.object().package()

    def PROVIDE(self, provide):
        if not isinstance(provide, Provide):
            raise Error('PROVIDE(): argument must be of type '+str(Provide)+' (was '+str(provide)+')')
        self.object().add_provide(provide)
        pass

    def REQUIRE(self, require):
        if not isinstance(require, Require):
            raise Error('REQUIRE(): argument must be of type '+str(Require))
        self.object().add_require(require)
        pass

    def PROVIDE_SYMBOL(self, symbol, match=Provide_String.EXACT_MATCH):
        if not symbol or len(symbol) == 0:
            raise Error('PROVIDE_SYMBOL(): need a non-zero symbol parameter')
        if not match in [Provide_String.EXACT_MATCH, Provide_String.PREFIX_MATCH, Provide_String.GLOB_MATCH]:
            raise Error('PROVIDE_SYMBOL(): match must be one of EXACT_MATCH, PREFIX_MATCH, GLOB_MATCH')
        self.object().add_provide(Provide_Symbol(symbol=symbol, match=match))
        pass

    def REQUIRE_SYMBOL(self, symbol, urgency=Require.URGENCY_IGNORE):
        if not symbol or len(symbol)==0:
            raise Error('REQUIRE_SYMBOL(): need a non-zero symbol parameter')
        if not urgency in [Require.URGENCY_IGNORE, Require.URGENCY_WARN, Require.URGENCY_ERROR]:
            raise Error('REQUIRE_SYMBOL(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
        self.object().add_require(Require_Symbol(
            symbol,
            found_in=[str(self.object())],
            urgency=urgency))
        pass

    def PROVIDE_CALLABLE(self, name):
        if not name or len(name) == 0:
            raise Error('PROVIDE_CALLABLE(): need a non-zero name parameter')
        self.object().add_provide(Provide_Callable(exename=name))
        pass

    def REQUIRE_CALLABLE(self, name, urgency=Require.URGENCY_IGNORE):
        if not name or len(name)==0:
            raise Error('REQUIRE_CALLABLE(): need a non-zero name parameter')
        if not urgency in [Require.URGENCY_IGNORE, Require.URGENCY_WARN, Require.URGENCY_ERROR]:
            raise Error('REQUIRE_SYMBOL(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
        self.object().add_require(Require_Callable(
            exename=name,
            found_in=[str(self.object())],
            urgency=urgency))
        pass

    def BUILDINFORMATION(self, buildinfo):
        self.object().add_buildinfo(buildinfo)
        pass

    AC_BUILDINFO_TRANSPORT_LOCAL = 0
    AC_BUILDINFO_TRANSPORT_PROPAGATE = 1
    def CONFIGURE_AC(self, lines, order, flags=None):
        if type(order) not in [types.IntType or types.LongType]:
            raise Error('CONFIGURE_AC(): "order" parameter must be an integer')
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.object().package().configure_ac().add_paragraph(
                paragraph=Paragraph(lines=lines),
                order=order)
            pass
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.object().add_buildinfo(BuildInfo_Configure_in(
                lines=lines,
                order=order))
            pass
        pass

    def ACINCLUDE_M4(self, lines, flags=None):
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.object().package().acinclude_m4().add_paragraph(
                paragraph=Paragraph(lines=lines))
            pass
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.object().add_buildinfo(BuildInfo_ACInclude_m4(
                lines=lines))
            pass
        pass
    pass
