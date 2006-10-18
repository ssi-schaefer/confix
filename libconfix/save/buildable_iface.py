# $Id: buildable_iface.py,v 1.27 2006/03/22 15:03:54 jfasch Exp $

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

from core.error import Error
from buildable_single import BuildableSingle
from fileprops import FileProperties
from core.require import Require
from plugins.c.dependency import Require_CInclude
from core.require_symbol import Require_Symbol
import helper_configure_in
import core.helper

class BuildableInterface:
    def __init__(self, buildable):

        assert isinstance(buildable, BuildableSingle), \
               'Cannot employ a BuildableInterface from anything composite'

        self.context_ = {

            'BUILDABLE_': buildable,

            # the require objects my functions may add

            'REQUIRES_': [],

            # per-file properties the user sets explicitly

            'FILE_PROPERTIES_': FileProperties(),

            # some constants we export and document

            'AC_BOILERPLATE': helper_configure_in.ORDER_BOILERPLATE,
            'AC_OPTIONS': helper_configure_in.ORDER_OPTIONS,
            'AC_PROGRAMS': helper_configure_in.ORDER_PROGRAMS,
            'AC_LIBRARIES': helper_configure_in.ORDER_LIBRARIES,
            'AC_HEADERS': helper_configure_in.ORDER_HEADERS,
            'AC_TYPEDEFS_AND_STRUCTURES': helper_configure_in.ORDER_TYPEDEFS_AND_STRUCTURES,
            'AC_FUNCTIONS': helper_configure_in.ORDER_FUNCTIONS,
            'AC_OUTPUT': helper_configure_in.ORDER_OUTPUT,
            
            'REQUIRED': Require.URGENCY_ERROR,
            'WELCOMED': Require.URGENCY_WARN,
            'BLUNZN': Require.URGENCY_DONTCARE
            }

        # compile my functions

        exec _funcs in self.context_

    def execute(self, lines):
        code = '\n'.join(lines) + '\n'
        try:
            exec code in self.context_
        except Exception, e:
            raise Error('Error executing code block', [e])

    def requires(self):
        return self.context_['REQUIRES_']

    def fileproperties(self):
        return self.context_['FILE_PROPERTIES_']


_funcs = """

import types

import libconfix.helper
from libconfix.core.require import Require
from libconfix.core.error import Error
from libconfix.plugins.c.dependency import Require_CInclude
from libconfix.core.require_symbol import Require_Symbol
from libconfix.fileprops import FileProperties
from libconfix.buildinfo_common import BuildInfo_Configure_in, BuildInfo_ACInclude_m4
from libconfix.paragraph import Paragraph

def REQUIRE_H(filename, urgency=Require.URGENCY_DONTCARE): # copied to plugins.c.base
 # copied to plugins.c.base
    global REQUIRES_, BUILDABLE_ # copied to plugins.c.base
 # copied to plugins.c.base
    if not filename: # copied to plugins.c.base
        raise Error("REQUIRE_H(): need a non-null 'filename' parameter") # copied to plugins.c.base
 # copied to plugins.c.base
    if type(filename) is not types.StringType: # copied to plugins.c.base
        raise Error("REQUIRE_H(): 'filename' parameter must be a string") # copied to plugins.c.base
 # copied to plugins.c.base
    if len(filename)==0: # copied to plugins.c.base
        raise Error("REQUIRE_H(): need a non-zero 'filename' parameter") # copied to plugins.c.base
 # copied to plugins.c.base
    if not urgency in [Require.URGENCY_DONTCARE, Require.URGENCY_WARN, # copied to plugins.c.base
                       Require.URGENCY_ERROR]: # copied to plugins.c.base
        raise Error('REQUIRE_H(): urgency must be one of REQUIRED, WELCOMED, BLUNZN') # copied to plugins.c.base
 # copied to plugins.c.base
    REQUIRES_.append(Require_CInclude( # copied to plugins.c.base
        filename=filename, # copied to plugins.c.base
        found_in=BUILDABLE_.filename(), # copied to plugins.c.base
        urgency=urgency)) # copied to plugins.c.base

def REQUIRE_SYMBOL(symbol, urgency=Require.URGENCY_DONTCARE): # copied to core.builder
 # copied to core.builder
    global REQUIRES_ # copied to core.builder
 # copied to core.builder
    if not symbol: # copied to core.builder
        raise Error("REQUIRE_SYMBOL(): need a non-null 'symbol' parameter") # copied to core.builder
 # copied to core.builder
    if type(symbol) is not types.StringType: # copied to core.builder
        raise Error("REQUIRE_SYMBOL(): 'symbol' parameter must be a string") # copied to core.builder
 # copied to core.builder
    if not symbol or len(symbol)==0: # copied to core.builder
        raise Error("REQUIRE_SYMBOL(): need a non-zero 'symbol' parameter") # copied to core.builder
 # copied to core.builder
    if not urgency in [Require.URGENCY_DONTCARE, Require.URGENCY_WARN, # copied to core.builder
                       Require.URGENCY_ERROR]: # copied to core.builder
        raise Error('REQUIRE_SYMBOL(): urgency must be one of REQUIRED, WELCOMED, BLUNZN') # copied to core.builder
 # copied to core.builder
    REQUIRES_.append(Require_Symbol( # copied to core.builder
        symbol=symbol, # copied to core.builder
        found_in=BUILDABLE_.filename(), # copied to core.builder
        urgency=urgency)) # copied to core.builder

def FILE_PROPERTIES(   # conflict: a copy is in core.filebuilder
    properties   # conflict: a copy is in core.filebuilder
    ):   # conflict: a copy is in core.filebuilder
   # conflict: a copy is in core.filebuilder
    global FILE_PROPERTIES_   # conflict: a copy is in core.filebuilder
   # conflict: a copy is in core.filebuilder
    if properties is None:   # conflict: a copy is in core.filebuilder
        raise Error("FILE_PROPERTIES(): 'properties' parameter cannot be None")   # conflict: a copy is in core.filebuilder
   # conflict: a copy is in core.filebuilder
    if not type(properties) is types.DictionaryType:   # conflict: a copy is in core.filebuilder
        raise Error("FILE_PROPERTIES(): 'properties' parameter must be a dictionary")   # conflict: a copy is in core.filebuilder
   # conflict: a copy is in core.filebuilder
    try:   # conflict: a copy is in core.filebuilder
        FILE_PROPERTIES_.update(FileProperties(properties=properties))   # conflict: a copy is in core.filebuilder
    except Error, e:   # conflict: a copy is in core.filebuilder
        raise Error("FILE_PROPERTIES(): error setting properties")   # conflict: a copy is in core.filebuilder

def MAIN(main=1):

    try:
        b = libconfix.core.helper.read_boolean(main)
    except Error, e:
        raise Error("MAIN(): parameter 'main' must be a boolean value")

    FILE_PROPERTIES({'MAIN': main})

def EXENAME(name):

    if type(name) is not types.StringType:
        raise EXENAME("EXENAME(): parameter 'main' must be a string")

    FILE_PROPERTIES({'EXENAME': name})

def CONFIGURE_IN(
    lines,
    order,
    id=None,
    propagate_only=False):

    global BUILDABLE_

    if not propagate_only:
        BUILDABLE_.add_local_configure_in(
            order=order,
            paragraph=Paragraph(lines))
        pass

    BUILDABLE_.add_buildinfo(BuildInfo_Configure_in(
        lines=lines,
        order=order))

def ACINCLUDE_M4(
    lines,
    id=None,
    propagate_only=False):

    global BUILDABLE_

    libconfix.core.debug.warn(os.path.join(BUILDABLE_.dir(), BUILDABLE_.filename())+": "
                         "ACINCLUDE_M4(): 'id' is deprecated and ignored")

    if not propagate_only:
        BUILDABLE_.add_acinclude_m4(paragraph=Paragraph(lines))
        pass

    BUILDABLE_.add_buildinfo(BuildInfo_ACInclude_m4(lines=lines))

"""
