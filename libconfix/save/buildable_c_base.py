# $Id: buildable_c_base.py,v 1.44 2006/06/21 11:06:49 jfasch Exp $

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
import dircache
import types

import const
import core.debug
import core.helper
import helper_c
import helper_automake
import readonly_prefixes
from buildable_single import BuildableSingle
from buildable_iface import BuildableInterface
from buildinfo_common import \
     BuildInfo_CIncludePath_NativeLocal, \
     BuildInfo_CIncludePath_NativeInstalled, \
     BuildInfo_CIncludePath_External, \
     BuildInfo_CommandlineMacros
from plugins.c.dependency import Require_CInclude
from fileprops import FileProperties
from core.error import Error

# argh: '$' does not hit doze-like carriage return, but rather leaves
# it at the end of the match.

_re_confix = re.compile('//\s*CONFIX:([^\r\n]*)')

class BuildableCBase(BuildableSingle):

    def __init__(self,
                 dir,
                 filename,
                 lines,
                 search_for_main):

        ########### initialize members

        self.has_main_ = None
        self.exename_ = None

        # are we using a module that is not yet installed? i.e., a
        # fellow module in the same package that is just being built.

        self.using_native_local_module_ = False

        # are we using a module that is installed?

        self.using_native_installed_module_ = False

        # include path for external modules, in reverse order. this is
        # a list of lists, of the form

        # [['-I/dir1'],
        #  ['-I/this/dir/include', '-I/that/dir/include']]

        # each list has been distributed to us by one module, and we
        # must not change the order inside the individual lists - they
        # may be significant, and the distributing modules surely
        # don't expect us to mess with the order.

        # the complete list is accompanied with a dictionary which
        # serves us to sort out duplicates from the beginning.
        
        self.reverse_include_path_external_ = []
        self.have_reverse_include_path_external_ = {}

        # command line macros
        
        self.cmdlinemacros_ = {}

        ########### initialize base class

        BuildableSingle.__init__(self,
                                 dir=dir,
                                 filename=filename,
                                 lines=lines)

        ########### examine the source

        if search_for_main:
            self.has_main_ = helper_c.has_main(lines)

        # see what we are requiring.

        for h_file in helper_c.extract_requires(lines):
            self.add_require(
                Require_CInclude(filename=h_file,
                                 found_in=[os.path.join(self.dir(), self.filename())]))

        # evaluate the buildable-interface

        self.eval_iface_(lines)

    def has_main(self):

        """ If true/false, indicates whether self has the main()
        function defined. If None, we simply do not know; the caller
        should apply a reasonable defautl (whatever that is). """

        return self.has_main_

    def exename(self):

        """ The name of the executable that self is the center of. May
        be None to indicate that we don't care about the executable
        name. """

        return self.exename_

    def consume_fileproperty(self, name, value):

        if name == FileProperties.MAIN:
            try:
                self.has_main_ = core.helper.read_boolean(value)
            except Error, e:
                raise Error("Value of property '"+FileProperties.MAIN+"' "
                            "must be of boolean type", [e])

        elif name == FileProperties.EXENAME:
            if type(value) is not types.StringType:
                raise Error("Value of property '"+FileProperties.EXENAME+"' "
                            "must be a string")
            if len(value) == 0:
                raise Error("Value of property '"+FileProperties.EXENAME+"' "
                            "must not be empty")
            self.exename_ = value

        BuildableSingle.consume_fileproperty(self, name, value)

    def validate(self):

        BuildableSingle.validate(self)

        if self.exename_ and self.has_main_ is not None and self.has_main_ == 0:
            raise Error(os.path.join(self.dir(), self.filename())+': '
                        'cannot have executable name set when no '
                        'main() function is defined')

    def gather_build_info(self, modules):

        BuildableSingle.gather_build_info(self, modules)

        for m in modules:
            for bi in m.buildinfos():

                if isinstance(bi, BuildInfo_CIncludePath_NativeLocal): # in confix2
                    # remember to set the include path to our artificial # in confix2
                    # local include directory, # in confix2
                    # $(top_builddir)/confix_include # in confix2
                    self.using_native_local_module_ = True # in confix2
                    continue # in confix2

                if isinstance(bi, BuildInfo_CIncludePath_NativeInstalled): # in confix2
                    # remember to add $(includedir) and the readonly # in confix2
                    # prefixes to our include path. # in confix2
                    self.using_native_installed_module_ = True # in confix2
                    continue # in confix2

                if isinstance(bi, BuildInfo_CIncludePath_External): # in confix2
                    incpath = bi.incpath() # in confix2
                    key = '.'.join(incpath) # in confix2
                    if not self.have_reverse_include_path_external_.has_key(key): # in confix2
                        self.reverse_include_path_external_.append(incpath) # in confix2
                        self.have_reverse_include_path_external_[key] = 1 # in confix2
                    continue # in confix2

                if isinstance(bi, BuildInfo_CommandlineMacros): # in confix2
                    for (k, v) in bi.macros().iteritems(): # in confix2
                        self.insert_cmdlinemacro_(k, v) # in confix2
                    continue # in confix2
                pass
            pass
        pass

    def reset_build_infos(self):

        self.reverse_include_path_external_ = []
        self.have_reverse_include_path_external_ = {}
        self.cmdlinemacros_ = {}
        self.using_native_local_module_ = False
        self.using_native_installed_module_ = False

        BuildableSingle.reset_build_infos(self)

    def contribute_makefile_am(self, buildmod):

        BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

        if self.using_native_local_module_:
            buildmod.makefile_am().add_includepath(
                os.path.join('-I$(top_builddir)', const.LOCAL_INCLUDE_DIR))

        if self.using_native_installed_module_:
            buildmod.makefile_am().add_includepath('-I$(includedir)')
            buildmod.makefile_am().add_includepath('$('+readonly_prefixes.incpath_var+')')

        incpath = self.reverse_include_path_external_[:] # in confix2
        incpath.reverse() # in confix2
 # in confix2
        for p in incpath: # in confix2
            for item in p: # in confix2
                buildmod.makefile_am().add_includepath(item) # in confix2

        for m in self.cmdlinemacros_.keys(): # in confix2
            val = self.cmdlinemacros_[m] # in confix2
            buildmod.makefile_am().add_cmdlinemacro(m, val) # in confix2

    def insert_cmdlinemacro_(self, key, value): # in confix2
 # in confix2
        if self.cmdlinemacros_.has_key(key): # in confix2
            existing_value = self.cmdlinemacros_[key] # in confix2
            if existing_value != value: # in confix2
                raise Error(self.name()+': ' # in confix2
                            'conflicting values for macro "'+key+'": ' # in confix2
                            '"'+existing_value+'"/"'+value+'"') # in confix2
            return # in confix2
 # in confix2
        self.cmdlinemacros_[key] = value # in confix2

    def eval_iface_(self, lines): # copied to plugins.c.base
 # copied to plugins.c.base
        # extract python lines from the file and evaluate them. search # copied to plugins.c.base
        # for 'CONFIX:' lines, gathering blocks of consecutive # copied to plugins.c.base
        # lines. 'blocks' is a dictionary, with the key being the # copied to plugins.c.base
        # starting line number, and the value being a list of lines. # copied to plugins.c.base
 # copied to plugins.c.base
        ctx = BuildableInterface(self) # copied to plugins.c.base
 # copied to plugins.c.base
        blocks = {} # copied to plugins.c.base
 # copied to plugins.c.base
        lineno = 0 # copied to plugins.c.base
        current_block = -1 # copied to plugins.c.base
 # copied to plugins.c.base
        for l in lines: # copied to plugins.c.base
            lineno = lineno + 1 # copied to plugins.c.base
            match = _re_confix.match(l) # copied to plugins.c.base
 # copied to plugins.c.base
            if match: # copied to plugins.c.base
                # start new block if we don't yet have one # copied to plugins.c.base
                if current_block == -1: # copied to plugins.c.base
                    current_block = lineno # copied to plugins.c.base
                    blocks[current_block] = [] # copied to plugins.c.base
                blocks[current_block].append(match.group(1)) # copied to plugins.c.base
            else: # copied to plugins.c.base
                # terminate current block if any # copied to plugins.c.base
                if current_block != -1: # copied to plugins.c.base
                    current_block = -1 # copied to plugins.c.base
                continue # copied to plugins.c.base
 # copied to plugins.c.base
        errors = [] # copied to plugins.c.base
        keys = blocks.keys()[:] # copied to plugins.c.base
        keys.sort() # copied to plugins.c.base
        for start_line in keys: # copied to plugins.c.base
            try: # copied to plugins.c.base
                ctx.execute(blocks[start_line]) # copied to plugins.c.base
            except Error, e: # copied to plugins.c.base
                msg = self.fullname()+': error in Confix code block starting at line '+str(start_line) # copied to plugins.c.base
                errors.append(Error(msg, [e])) # copied to plugins.c.base
 # copied to plugins.c.base
        if len(errors): # copied to plugins.c.base
            raise Error('Encountered %s errors in file %s' % \
                        (len(errors), self.fullname()), errors) # copied to plugins.c.base
 # copied to plugins.c.base
 # copied to plugins.c.base
        # - pull in require objects (that is, hand them over to our # copied to plugins.c.base
        # base class which will take care to propagate them outwards. # copied to plugins.c.base
 # copied to plugins.c.base
        for r in ctx.requires(): # copied to plugins.c.base
            self.add_require(r) # copied to plugins.c.base
 # copied to plugins.c.base
 # copied to plugins.c.base
        # - override the properties we have so far with the properties # copied to plugins.c.base
        #   the iface has, if any # copied to plugins.c.base
 # copied to plugins.c.base
        self.consume_fileproperties(ctx.fileproperties()) # copied to plugins.c.base

