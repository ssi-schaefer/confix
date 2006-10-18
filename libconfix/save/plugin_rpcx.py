# $Id: plugin_rpcx.py,v 1.5 2005/10/31 15:09:57 jfasch Exp $

assert 0, "Sorry Haubi, I had to disable this file during refactoring"

## import re
## import os

## from ac_lines import AC_Lines
## from check import AC_Check
## from require_symbol import Require_Symbol
## from require_h import Require_CInclude
## from require import Require
## from provide import Provide
## from content import ModuleContent
## from buildable_mgr_bases import BuildableCreator
## from buildable_single import BuildableSingle
## from buildable_h import BuildableHeader
## from buildable_c import BuildableC
## from buildinfo import BuildInformation
## import helper
## import helper_c
## import helper_automake
## import const
## import debug

## class BuildableRPCXCreator(BuildableCreator):

##     """ Factory class that generates a L{BuildableRPCX} object from
##     filenames that end with '.x'. """

##     def create_from_file(self, dir, filename):

##         if filename.endswith('.x'):
##             return BuildableRPCX(
##                 dir=dir,
##                 filename=filename,
##                 lines=helper.lines_of_file(os.path.join(dir, filename)))
##         return None

## class BuildableRPCX(BuildableSingle):

##     """ This buildable knows how to handle a file.x, which has to be
##     an rpc-definition file, compileable by 'rpcgen'.
##     It automatically creates the marshalling/demarshalling things (xdr)
##     and the header-file for the rpc-definition. """

##     _re_xinclude = re.compile(r"^\s*#\s*include\s*[\"<]([^\">]*)[\">]")
##     _re_cinclude = re.compile(r"^%\s*#\s*include\s*[\"<]([^\">]*)[\">]")

##     # provide-modes

##     PROVIDE_PUBLIC = BuildableHeader.PROVIDE_PUBLIC
##     PROVIDE_PACKAGE = BuildableHeader.PROVIDE_PACKAGE
##     PROVIDE_GUESS = BuildableHeader.PROVIDE_GUESS
##     PROVIDE_NOTATALL = BuildableHeader.PROVIDE_NOTATALL

##     def __init__(self,
##                  dir,
##                  filename,
##                  lines):

##         BuildableSingle.__init__(self,
##                                  dir=dir,
##                                  filename=filename,
##                                  lines=lines)

##         self.install_path_ = None
##         self.provide_mode_ = None
##         self.generated_h_provide_mode_ = None
##         self.xincludes_ = []
##         self.cincludes_ = []

##         for line in lines:
##             match = BuildableRPCX._re_xinclude.match(line)
##             if match:
##                 inc = match.group(1)
##                 self.xincludes_.append(inc)
##                 self.add_require(Require_RPCX(filename=inc, found_in=self.filename()))
##                 debug.trace(['scan'], self.filename()+' includes '+inc)
##                 continue

##             match = BuildableRPCX._re_cinclude.match(line)
##             if match:
##                 inc = match.group(1)
##                 self.cincludes_.append(inc)
##                 debug.trace(['scan'], 'output from '+self.filename()+' includes '+inc)
##                 continue

##         # we remember the buildables we generated; we have to send
##         # information on to them later in the process. if that list is
##         # None, this is an indicator that we haven't yet generated
##         # them. (we must only generate once, or else our depgraph
##         # builder enters a loop.)

##         self.generated_buildables_ = None

##     def provide_mode(self): return self.provide_mode_
##     def install_path(self): return self.install_path_
##     def set_install_path(self, p): self.install_path_ = p

##     def set_provide_mode(self, provide_mode):
##         assert provide_mode in [ BuildableRPCX.PROVIDE_PUBLIC
##                                , BuildableRPCX.PROVIDE_PACKAGE
##                                , BuildableRPCX.PROVIDE_GUESS
##                                , BuildableRPCX.PROVIDE_NOTATALL
##                                ]
##         self.provide_mode_ = provide_mode

##     def consume_fileproperty(self, name, value):

##         debug.trace(['fileprops'], self.filename() 
##             + ' consumes fileprops for ' + name + ': ' + `value`)

##         BuildableSingle.consume_fileproperty(self, name, value)

##         if name == FileProperties.PROVIDE_MODE:
##             if type(value) is not types.StringType:
##                 raise Error(self.name()+': file property "'+name
##                     +'" must be a string')

##             if value == 'public':
##                 self.provide_mode_ = BuildableRPCX.PROVIDE_PUBLIC
##             elif value == 'package':
##                 self.provide_mode_ = BuildableRPCX.PROVIDE_PACKAGE
##             elif value == 'guess':
##                 self.provide_mode_ = BuildableRPCX.PROVIDE_GUESS
##             else:
##                 raise Error(self.name()+': file property "'+name+'" '
##                     'must be one of "public", "package", or "guess" '
##                     '(was "'+value+'")')

##         if name == FileProperties.INSTALL_PATH:
##             if type(value) is not types.StringType:
##                 raise Error(self.name()+': file property "'+name
##                     +'" must be a string')

##             self.install_path_ = value

##     def generate_buildables(self):

##         if self.generated_buildables_ is not None:
##             return []
##         self.generated_buildables_ = []

##         for inc in self.xincludes_:
##             self.add_require(Require_RPCX(filename=inc,
##                 found_in=os.path.join(self.dir(), self.filename())
##             ))

##         if self.install_path_ is None:
##             self.install_path_ = ''

##         if self.provide_mode_ in [None, BuildableRPCX.PROVIDE_GUESS]:
##             if self.filename().startswith('_'):
##                 self.provide_mode_ = BuildableRPCX.PROVIDE_PACKAGE
##             else:
##                 self.provide_mode_ = BuildableRPCX.PROVIDE_PUBLIC

##         self.add_internal_provide(Provide_RPCX(self.filename()))

##         provide_as = os.path.join(self.install_path(), self.filename())

##         if self.provide_mode_ == BuildableRPCX.PROVIDE_PACKAGE:
##             self.add_package_provide(Provide_RPCX(provide_as))
##         elif self.provide_mode_ == BuildableRPCX.PROVIDE_PUBLIC:
##             self.add_public_provide(provide_as)
##         elif self.provide_mode_ == BuildableRPCX.PROVIDE_NOTATALL:
##             pass
##         else:
##             assert 0

##         generated_h = BuildableRPCX_H(dir=self.dir()
##             , xfile=self.filename()
##             , provide_mode=self.provide_mode_
##             , install_path=self.install_path()
##         )

##         for inc_file in self.cincludes_:
##             debug.trace(['generate'], 'generated '+generated_h.filename()
##                 +' includes '+inc_file);
##             generated_h.add_requires([
##                 Require_CInclude(filename=inc_file,
##                     found_in=self.filename())
##             ])

##         self.generated_buildables_.append(generated_h)

##         generated_xdr_c = BuildableRPCX_XDR(dir=self.dir()
##             , xfile=self.filename()
##         )

##         debug.trace(['generate'], self.filename()
##             + ' generates ' + generated_xdr_c.filename())

##         self.generated_buildables_.append(generated_xdr_c)

##         return self.generated_buildables_

##     def validate(self):

##         BuildableSingle.validate(self)

##         self.add_content(ModuleContent_RPCX_Local(name=self.name()
##             , dir=self.dir()
##             , filename=self.filename()
##             , install_path=self.install_path()
##             , includes=self.xincludes_
##         ))

##     def contribute_makefile_am(self, buildmod):

##         BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

##         buildmod.makefile_am().add_extra_dist(self.filename())

##         buildmod.makefile_am().install_header_private(
##             filename=self.filename()
##             , install_path=self.install_path()
##         )

##         if self.provide_mode_ == BuildableRPCX.PROVIDE_PUBLIC:
##             buildmod.makefile_am().install_header_public(
##                 filename=self.filename()
##                 , install_path=self.install_path()
##             )

##     def gen_base_(self):
##         base, ext = os.path.splitext(os.path.basename(self.filename()))
##         return base
        
##     def gen_h_(self): return self.gen_base_()+'.h'
##     def gen_xdr_c_(self): return self.gen_base_()+'_xdr.c'
##     def gencmd_h_(self):
##         return '$(RPCGEN) -h -o '+self.gen_h_()     +' '+self.rpcx_sourcefile_
##     def gencmd_xdr_c_(self):
##         return '$(RPCGEN) -c -o '+self.gen_xdr_c_() +' '+self.rpcx_sourcefile_

## class Require_RPCX(Require):

##     """ Object representing a module's need for an RPCX file of a
##     certain name. A module may need an RPCX file because one or more of
##     that module's files #include the file, or because the module wants
##     to generate code from the RPCX file. """

##     def __init__(self, filename, found_in):

##         Require.__init__(self, id='RPCX:'+filename)

##         self.filename_ = helper.normalize_filename(filename)
##         self.found_in_ = []

##         if (len(found_in)):
##             self.found_in_.append(found_in)

##     def update(self, r):

##         if not isinstance(r, Require_RPCX): return 0

##         if r.filename() != self.filename(): return 0

##         # we have a match. add r's found_in to my list, and update the
##         # urgency appropriately

##         self.found_in_ = self.found_in_ + r.found_in()
##         if r.urgency() > self.urgency():
##             self.set_urgency(r.urgency())

##         return 1

##     def __repr__(self):
##         ret = '(RPCX) #include<%s>' % self.filename_
##         if len(self.found_in_):
##             ret = ret + ' (from ' + str(self.found_in_) + ')'
##         return ret

##     def filename(self):

##         return self.filename_

##     def found_in(self):

##         return self.found_in_

## class Provide_RPCX(Provide):

##     """ Provide_RPCX satisfies require objects of type
##     L{Require_RPCX}. """

##     EXACT_MATCH = 0
##     PREFIX_MATCH = 1
##     GLOB_MATCH = 2

##     # ATTENTION: the ctor signature is part of the repository
##     # format. do not change it unless you have a good reason and you
##     # are willing to receive user complaints.

##     def __init__(self, filename, match=EXACT_MATCH):
##         Provide.__init__(self)
##         self.filename_ = helper.normalize_filename(filename)
##         self.match_ = match

##     def __repr__(self):
##         return "RPCX: "+self.filename_

##     def resolve(self, req):
##         assert isinstance(req, Require), \
##                "Provide_RPCX.resolve(): not even a Provide"
##         if not isinstance(req, Require_RPCX): return 0

##         if self.match_ == Provide_RPCX.EXACT_MATCH:
##             if req.filename() != self.filename_:
##                 return 0
##         elif self.match_ == Provide_RPCX.PREFIX_MATCH:
##             if req.filename().find(self.filename_) != 0:
##                 return 0
##         elif self.match_ == Provide_RPCX.GLOB_MATCH:
##             if not fnmatch.fnmatchcase(req.filename(), self.filename_):
##                 return 0
##         else:
##             assert 0, "Bad match identifier: %d" % self.match_

##         return 1

## class ModuleContent_RPCX(ModuleContent):

##     def __init__(self, name, filename, install_path, includes):
        
##         ModuleContent.__init__(self
##             , name=name
##             , configure_in=[]
##             , acinclude_m4=[]
##         )

##         self.install_path_ = install_path
##         self.filename_ = filename
##         self.includes_ = includes[:]

##     def __repr__(self):

##         return ModuleContent.__repr__(self) + ' installpath "' + \
##             self.install_path_ + '", ' + `len(self.includes_)` + ' includes'

##     def install_path(self): return self.install_path_
##     def filename(self): return self.filename_
##     def includes(self): return self.includes_

##     def distribute_build_infos(self, b):

##         ModuleContent.distribute_build_infos(self, b)

##         buildinfos = []

##         buildinfos.append(
##           ( "RPCX_INCLUDE_LIST"
##           , ( os.path.join(self.install_path_, self.filename_)
##             , self.includes_
##           ) )
##         )

##         debug.trace(['buildinfos'], self.name()+' distributes build infos: '
##             +`buildinfos`+' to '+`b`)

##         b.consume_build_infos(buildinfos)

## class ModuleContent_RPCX_Local(ModuleContent_RPCX):

##     def __init__(self, name, dir, filename, install_path, includes):

##         ModuleContent_RPCX.__init__(self
##           , name=name
##           , filename=filename
##           , install_path=install_path
##           , includes=includes
##         )

##         self.dir_ = dir

##     def distribute_build_infos(self, b):

##         ModuleContent_RPCX.distribute_build_infos(self, b)
##         buildinfos = []
##         buildinfos.append(
##           ( "RPCX_SOURCEFILE"
##           , ( os.path.join(self.install_path(), self.filename())
##             , os.path.join('$(top_builddir)'
##                   , const.LOCAL_INCLUDE_DIR 
##                   , self.install_path()
##                   , self.filename()
##         ) ) ) )
##         debug.trace(['buildinfos'], self.name()+' distributes build infos: '
##             +`buildinfos`+' to '+`b`)
##         b.consume_build_infos(buildinfos)


##     def install(self):

##         return ModuleContent_RPCX_Installed(name=self.name()
##             , filename=self.filename()
##             , install_path=self.install_path()
##             , includes=self.includes()
##         )

## class ModuleContent_RPCX_Installed(ModuleContent_RPCX):

##     def __init__(self, name, filename, install_path, includes):
    
##         ModuleContent_RPCX.__init__(self
##             , name=name
##             , filename=filename
##             , install_path=install_path
##             , includes=includes
##         )

##     def distribute_build_infos(self, b):
    
##         ModuleContent_RPCX.distribute_build_infos(self, b)

##         b.consume_build_infos(
##           [ ( "RPCX_SOURCEFILE"
##             , ( os.path.join(self.install_path(), self.filename())
##               , os.path.join('$(includedir)'
##                   , self.install_path()
##                   , self.filename()
##         ) ) ) ] )


## class BuildableRPCX_output_base(BuildableSingle):

##     OUTPUTMODE_H = 0
##     OUTPUTMODE_XDR = 1
##     OUTPUTMODE_SVC = 2
##     OUTPUTMODE_CLNT = 3

##     def __init__(self, dir, xfile, outputmode, name):

##         BuildableSingle.__init__(self, dir=dir,
##                                  filename=name,
##                                  lines=[])

##         self.xfile_ = xfile
##         self.outputmode_ = outputmode

##         self.rpcx_includes_ = None
##         self.rpcx_sourcefile_ = None

##         self.generated_buildables_ = None

##     def xfile(self): return self.xfile_
##     def outputmode(self): return self.outputmode_
##     def rpcx_includes(self): return self.rpcx_includes_
##     def rpcx_sourcefile(self): return self.rpcx_sourcefile_

##     def gather_configure_in(self):

##         # we are going to compile PDL files, so we will need PDL

##         ret = [AC_Lines(lines=['AC_CHECK_PROG(RPCGEN, rpcgen, rpcgen)',
##                                'if test x$RPCGEN = x; then',
##                                '  AC_MSG_ERROR([rpcgen not found in path])',
##                                'fi'
##                                ],
##                         order=AC_Check.PROGRAMS,
##                         id='AC_PROG_RPCGEN')]
##         ret.extend(BuildableSingle.gather_configure_in(self))
##         return ret

##     def validate(self):

##         BuildableSingle.validate(self)

##         self.add_require(Require_RPCX(filename=self.xfile_
##             , found_in=self.filename()
##         ))

##     def gather_configure_in(self):

##         # we are going to compile RPCX files, so we will need rpcgen

##         ret = [AC_Lines(lines=['AC_CHECK_PROG(RPCGEN, rpcgen, rpcgen)',
##                                'if test x$RPCGEN = x; then',
##                                '  AC_MSG_ERROR([rpcgen not found in path])',
##                                'fi'
##                                ],
##                         order=AC_Check.PROGRAMS,
##                         id='AC_PROG_RPCGEN')]
##         ret.extend(BuildableSingle.gather_configure_in(self))
##         return ret

##     def consume_build_infos(self, infos):

##         BuildableSingle.consume_build_infos(self, infos)

##         for (name, value) in infos:
         
##             debug.trace(['buildinfos'], self.filename()
##                 +' consumes build infos: ('+name+', '+`value`+')')

##             if name == "RPCX_INCLUDE_LIST" and value[0] == self.xfile_:
            
##                 if self.rpcx_includes_ is not None:
##                     continue
##                 self.rpcx_includes_ = value[1]

##                 for inc in self.rpcx_includes_:
##                     root, ext = os.path.splitext(inc)
##                     require_h = Require_CInclude(filename=root+'.h'
##                         , found_in=self.filename())

##                     for b in self.generated_buildables_:
##                         b.add_require(require_h)

##                 continue
           
##             if name == "RPCX_SOURCEFILE" and value[0] == self.xfile_:

##                 if self.rpcx_sourcefile_ is not None:
##                     assert self.rpcx_sourcefile_ == value[1]
##                     continue

##                 self.rpcx_sourcefile_ = value[1]

##                 continue

##     def contribute_makefile_am(self, buildmod):

##         BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

##         buildmod.makefile_am().add_line('')

##         if self.rpcx_sourcefile_ is None:
##             # assume xfile is locally provided
##             self.rpcx_sourcefile_ = os.path.join('$(top_builddir)'
##                 , const.LOCAL_INCLUDE_DIR 
##                 , self.xfile_
##             )
##             if self.outputmode_ != self.OUTPUTMODE_H:
##                 buildmod.makefile_am().add_line(self.gen_out_()+': '
##                     +os.path.join('$(top_builddir)'
##                         , const.LOCAL_INCLUDE_DIR
##                         , self.gen_h_()
##                 ))

##         buildmod.makefile_am().add_line(self.gen_out_()+': '+self.rpcx_sourcefile_)
##         buildmod.makefile_am().add_line('\trm -f '+self.gen_out_())
##         buildmod.makefile_am().add_line('\t'+self.gen_outcmd_())

##         # register generated files as BUILT_SOURCES

##         buildmod.makefile_am().add_built_sources(self.gen_out_())

##     def gen_base_(self):
##         base, ext = os.path.splitext(os.path.basename(self.xfile_))
##         return base

##     def gen_h_(self):
##         return self.gen_base_()+'.h'

##     def gen_out_(self):
##         if self.outputmode_ == self.OUTPUTMODE_H:
##             return self.gen_h_()
##         if self.outputmode_ == self.OUTPUTMODE_XDR:
##             return self.gen_base_()+'_xdr.c'
##         if self.outputmode_ == self.OUTPUTMODE_SVC:
##             return self.gen_base_()+'_svc.c'
##         if self.outputmode_ == self.OUTPUTMODE_CLNT:
##             return self.gen_base_()+'_clnt.c'
##         assert 0, 'invalid output mode'

##     def gen_outcmd_(self):
##         if self.outputmode_ == self.OUTPUTMODE_H:
##             return '$(RPCGEN) -h -o '+self.gen_out_() +' '+self.rpcx_sourcefile_
##         if self.outputmode_ == self.OUTPUTMODE_XDR:
##             return '$(RPCGEN) -c -o '+self.gen_out_() +' '+self.rpcx_sourcefile_
##         if self.outputmode_ == self.OUTPUTMODE_SVC:
##             return '$(RPCGEN) -m -o '+self.gen_out_() +' '+self.rpcx_sourcefile_
##         if self.outputmode_ == self.OUTPUTMODE_CLNT:
##             return '$(RPCGEN) -l -o '+self.gen_out_() +' '+self.rpcx_sourcefile_
##         assert 0, 'invalid output mode'

## class BuildableRPCX_H(BuildableRPCX_output_base):

##     """ This buildable is automatically created by BuildableRPCX() and
##     creates the header-file from the rpc-definition file 'file.x' """

##     def __init__(self, dir, xfile, provide_mode, install_path):

##         BuildableRPCX_output_base.__init__(self
##             , name='(Automatic RPCX_H invocation from '
##                   + os.path.join(dir, xfile) + ')'
##             , dir=dir
##             , xfile=xfile
##             , outputmode=BuildableRPCX_output_base.OUTPUTMODE_H
##         )

##         self.generated_buildables_ = None
##         self.provide_mode_ = provide_mode
##         self.install_path_ = install_path

##     def generate_buildables(self):

##         if self.generated_buildables_ is not None:
##             return []
##         self.generated_buildables_ = []

##         generated_h = BuildableHeader(dir=self.dir()
##             , filename=self.gen_h_()
##             , lines=[]
##             , provide_mode=self.provide_mode_
##         )
##         generated_h.set_install_path(self.install_path_)

##         self.generated_buildables_.append(generated_h)

##         return self.generated_buildables_

##     def validate(self):
        
##         BuildableRPCX_output_base.validate(self)

##         self.add_requires(
##           [ Require_RPCX(filename=self.xfile()
##               , found_in=self.gen_h_()
##         ) ] )

##         self.add_requires(
##           [ Require_CInclude(filename=os.path.join('rpc', 'rpc.h')
##               , found_in=self.gen_h_()
##         ) ] )

## class BuildableRPCX_c_base(BuildableRPCX_output_base):

##     def __init__(self, dir, xfile, outputmode, name):

##         BuildableRPCX_output_base.__init__(self
##             , name=name
##             , dir=dir
##             , xfile=xfile
##             , outputmode=outputmode
##         )

##     def generate_buildables(self):

##         if self.generated_buildables_ is not None:
##             return []
##         self.generated_buildables_ = []

##         generated_out = BuildableC(dir=self.dir(),
##                            filename=self.gen_out_(),
##                            lines=[])

##         generated_out.add_requires(
##           [ Require_CInclude(filename=self.gen_h_()
##               , found_in=self.gen_out_()
##         ) ] )

##         self.generated_buildables_.append(generated_out)

##         return self.generated_buildables_

##     def validate(self):

##         BuildableRPCX_output_base.validate(self)

##         self.add_requires(
##           [ Require_CInclude(filename=self.gen_h_()
##               , found_in=self.gen_out_()
##         ) ] )

## class BuildableRPCX_XDR(BuildableRPCX_c_base):

##     """ This buildable is automatically created by BuildableRPCX() and
##     creates the marshalling/demarshalling things of rpcgen (aka xdr) """

##     def __init__(self, dir, xfile):

##         BuildableRPCX_c_base.__init__(self
##             , name='(Automatic RPCX_XDR invocation from '
##                   + os.path.join(dir, xfile) + ')'
##             , dir=dir
##             , xfile=xfile
##             , outputmode=BuildableRPCX_output_base.OUTPUTMODE_XDR
##         )

## class BuildableRPCX_SVC(BuildableRPCX_c_base):

##     """ Add this buildable in the Makefile.py to create the server-side stubs:
##     from libconfix.plugin_rpcx import BuildableRPCX_SVC
##     BUILDABLE(BuildableRPCX_SVC(dir=DIR(), xfile="file.x")) """

##     def __init__(self, dir, xfile):

##         BuildableRPCX_c_base.__init__(self
##             , name='(Explicit RPCX_SVC('+xfile+') invocation in '+dir+')'
##             , dir=dir
##             , xfile=xfile
##             , outputmode=BuildableRPCX_output_base.OUTPUTMODE_SVC
##         )

## class BuildableRPCX_CLNT(BuildableRPCX_c_base):

##     """ Add this buildable in the Makefile.py to create the client-side stubs:
##     from libconfix.plugin_rpcx import BuildableRPCX_CLNT
##     BUILDABLE(BuildableRPCX_CLNT(dir=DIR(), xfile="file.x")) """

##     def __init__(self, dir, xfile):

##         BuildableRPCX_c_base.__init__(self
##             , name='(Explicit RPCX_CLNT('+xfile+') invocation in '+dir+')'
##             , dir=dir
##             , xfile=xfile
##             , outputmode=BuildableRPCX_output_base.OUTPUTMODE_CLNT
##         )

## if __name__ == "__main__":
##     b = BuildableRPCX('x', 'x')
