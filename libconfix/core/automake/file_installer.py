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

import re, os, types

from libconfix.core.utils.error import Error
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils import const

import helper_automake
from rule import Rule

## class FileInstallerFactory:
##     def __init__(self, configure_in, auxdir, source_auxdir, use_bulk_install):
##         self.configure_in_ = configure_in
##         self.auxdir_ = auxdir
##         self.source_auxdir_ = source_auxdir
##         self.use_bulk_install_ = use_bulk_install
##         self.bulk_install_program_ = 'bulk-install.py'

##         if self.use_bulk_install_:
##             self.auxdir_.eat_file(sourcename=os.path.join(self.source_auxdir_, self.bulk_install_program_),
##                                   mode=0755)
##             self.configure_in_.add_paragraph(
##                 order=helper_configure_in.ORDER_OPTIONS,
##                 paragraph=Paragraph([enable_bulk_install_option]))
##             pass
##         pass
##     def create(self):
##         return FileInstaller(configure_in=self.configure_in_,
##                              auxdir=self.auxdir_,
##                              use_bulk_install=self.use_bulk_install_,
##                              bulk_install_program=self.bulk_install_program_)
##     pass

class FileInstaller:

    re_subst = re.compile('(^[_\d]|\W)')

##     FILENAME_BULK_INSTALL_PUBLIC = '.bulk-install-public'
##     FILENAME_BULK_INSTALL_LOCAL = '.bulk-install-local'

##    TARGET_INSTALL_PUBLIC = 'confix-install-public'
    TARGET_INSTALL_LOCAL = 'confix-install-local'
    TARGET_CLEAN_LOCAL = 'confix-clean-local'

##     VAR_SRCDIR = 'srcdir'
##     VAR_BUILDDIR = 'builddir'
##     VAR_INCLUDEDIR = 'includedir'
##     VAR_DATADIR = 'datadir'
##     VAR_PREFIX = 'prefix'
##     VAR_LOCALINCLUDEDIR = 'localincludedir'

##     BULK_INSTALL_FILE_HEADER = [
##         '# DO NOT EDIT! This file was automatically generated',
##         '# by Confix version '+const.CONFIX_VERSION,
##         ''
##         ]
    
    def __init__(self,
                 #makefile_am,
                 #configure_in,
                 #auxdir,
                 #use_bulk_install,
                 #bulk_install_program
                 ):

        #self.configure_in_ = configure_in
        #self.auxdir_ = auxdir
        #self.bulk_install_program_ = bulk_install_program

        #self.use_bulk_install_ = use_bulk_install

        # dictionary filename -> set of paths relative to
        # $(includedir)
        
        self.public_headers_ = {}
        self.private_headers_ = {}

        # same for $(datadir)

        self.datafiles_ = {}

        # same for $(prefix) (dirty thing that, but some people want
        # it)

        self.prefixfiles_ = {}

        # same for arbitrary install locations (even more dirty)

        self.tunnelfiles_ = {}
        
        pass

    def add_public_header(self, filename, dir):
        self.add_to_file2dirdict_(file2dirdict=self.public_headers_,
                                  filetype_errmsg='Public header',
                                  filename=filename,
                                  dir=dir)
        pass

    def add_private_header(self, filename, dir):
        self.add_to_file2dirdict_(file2dirdict=self.private_headers_,
                                  filetype_errmsg='Private header',
                                  filename=filename,
                                  dir=dir)
        pass

    def add_datafile(self, filename, dir):
        self.add_to_file2dirdict_(file2dirdict=self.datafiles_,
                                  filetype_errmsg='Data file',
                                  filename=filename,
                                  dir=dir)
        pass

    def add_prefixfile(self, filename, dir):
        self.add_to_file2dirdict_(file2dirdict=self.prefixfiles_,
                                  filetype_errmsg='Prefix file',
                                  filename=filename,
                                  dir=dir)
        pass

    def add_tunnelfile(self, filename, dir):
        self.add_to_file2dirdict_(file2dirdict=self.tunnelfiles_,
                                  filetype_errmsg='Tunnel file',
                                  filename=filename,
                                  dir=dir)
        pass

    def output(self, makefile_am):

##         # if we are offering that feature at all, write the input
##         # files for the bulk-install program

##         public_installs = []
##         local_installs = []
        
##         if self.use_bulk_install_:
##             public_installs.extend(self.bulk_install_public_headers_())
##             public_installs.extend(self.bulk_install_datafiles_())
##             public_installs.extend(self.bulk_install_prefixfiles_())
##             public_installs.extend(self.bulk_install_tunnelfiles_())

##             local_installs.extend(self.bulk_install_private_headers_())

##             pass

##         if len(public_installs):
##             buildmod.add_pseudo_handwritten_file(FileInstaller.FILENAME_BULK_INSTALL_PUBLIC)
##             buildmod.add_lines_to_pseudo_handwritten_file(
##                 FileInstaller.FILENAME_BULK_INSTALL_PUBLIC,
##                 FileInstaller.BULK_INSTALL_FILE_HEADER + public_installs)
##             buildmod.makefile_am().add_extra_dist(FileInstaller.FILENAME_BULK_INSTALL_PUBLIC)
##             pass

##         if len(local_installs):
##             buildmod.add_pseudo_handwritten_file(FileInstaller.FILENAME_BULK_INSTALL_LOCAL)
##             buildmod.add_lines_to_pseudo_handwritten_file(
##                 FileInstaller.FILENAME_BULK_INSTALL_LOCAL,
##                 FileInstaller.BULK_INSTALL_FILE_HEADER + local_installs)
##             buildmod.makefile_am().add_extra_dist(FileInstaller.FILENAME_BULK_INSTALL_LOCAL)
##             pass

        # add our common hook targets that both methods
        # (automake-native and confix-bulk) must provide.

        makefile_am.add_all_local(FileInstaller.TARGET_INSTALL_LOCAL)
        makefile_am.add_clean_local(FileInstaller.TARGET_CLEAN_LOCAL)
##         makefile_am.add_install_data_local(FileInstaller.TARGET_INSTALL_PUBLIC)

        # generate (conditional) install instructions for both
        # methods.
        
##         if self.use_bulk_install_:
##             buildmod.makefile_am().add_lines(['if !BULK_INSTALL', ''])
##             pass

        self.automake_install_public_headers_(makefile_am=makefile_am)
        self.automake_install_datafiles_(makefile_am=makefile_am)
        self.automake_install_prefixfiles_(makefile_am=makefile_am)
        self.automake_install_private_headers_(makefile_am=makefile_am)
##         buildmod.makefile_am().add_lines(helper_automake.format_rule(
##             targets=[FileInstaller.TARGET_INSTALL_PUBLIC]))

##         if self.use_bulk_install_:
##             buildmod.makefile_am().add_lines(['', 'else', ''])

##             installprog = '/'.join(['$(top_srcdir)',
##                                     self.auxdir_.relpath(),
##                                     self.bulk_install_program_])
            
##             if len(local_installs):
##                 local_install_commands = [installprog + ' ' + \
##                                           FileInstaller.VAR_SRCDIR + '=$(srcdir) ' + \
##                                           FileInstaller.VAR_BUILDDIR + '=. ' + \
##                                           FileInstaller.VAR_LOCALINCLUDEDIR + '=$(top_builddir)/' + const.LOCAL_INCLUDE_DIR + \
##                                           ' < $(srcdir)/' + FileInstaller.FILENAME_BULK_INSTALL_LOCAL]
##                 local_clean_commands=['@echo FIXME: dont know how to bulk-clean']
##             else:
##                 local_install_commands = []
##                 local_clean_commands = []
##                 pass

##             if len(public_installs):
##                 public_install_commands = [installprog + ' ' + \
##                                            FileInstaller.VAR_SRCDIR + '=$(srcdir) ' + \
##                                            FileInstaller.VAR_BUILDDIR + '=. ' + \
##                                            FileInstaller.VAR_INCLUDEDIR + '=$(includedir) ' + \
##                                            FileInstaller.VAR_DATADIR + '=$(datadir) ' + \
##                                            FileInstaller.VAR_PREFIX + '=$(prefix)' + \
##                                            ' < $(srcdir)/' + FileInstaller.FILENAME_BULK_INSTALL_PUBLIC]
##             else:
##                 public_install_commands = []
##                 pass
            
##             buildmod.makefile_am().add_lines(helper_automake.format_rule(
##                 targets=[FileInstaller.TARGET_INSTALL_LOCAL],
##                 commands=local_install_commands))
##             buildmod.makefile_am().add_lines(helper_automake.format_rule(
##                 targets=[FileInstaller.TARGET_CLEAN_LOCAL],
##                 commands=local_clean_commands))

##             buildmod.makefile_am().add_lines(helper_automake.format_rule(
##                 targets=[FileInstaller.TARGET_INSTALL_PUBLIC],
##                 commands=public_install_commands))
##             pass

##         if self.use_bulk_install_:
##             buildmod.makefile_am().add_lines(['', 'endif'])
##             pass

        pass

    def automake_install_public_headers_(self, makefile_am):
        for reldir, filelist in self.dir2filedict_(file2dirdict=self.public_headers_).iteritems():
            if len(reldir):
                # define subdirectory
                symbolicname = self.compute_install_dirname_('publicheader_'+reldir)
                makefile_am.define_install_directory(symbolicname=symbolicname,
                                                     dirname='$(includedir)/'+reldir)
                pass
            else:
                # no need to define subdirectory; take predefined
                symbolicname = ''
                pass
            makefile_am.add_to_install_directory(
                symbolicname=symbolicname,
                family='HEADERS',
                files=filelist)
            pass
        pass
    
    def automake_install_datafiles_(self, makefile_am):
        for dirname, filelist in self.dir2filedict_(file2dirdict=self.datafiles_).iteritems():
            # define directory
            symbolicname = self.compute_install_dirname_('data_'+dirname)
            makefile_am.define_install_directory(symbolicname=symbolicname,
                                                 dirname='$(datadir)/'+dirname)
            makefile_am.add_to_install_directory(
                symbolicname=symbolicname,
                family='DATA',
                files=filelist)
            pass
        pass

    def automake_install_prefixfiles_(self, makefile_am):
        for dirname, filelist in self.dir2filedict_(file2dirdict=self.prefixfiles_).iteritems():
            # define directory
            symbolicname = self.compute_install_dirname_('prefix_'+dirname)
            makefile_am.define_install_directory(symbolicname=symbolicname,
                                                 dirname='$(prefix)/'+dirname)
            makefile_am.add_to_install_directory(
                symbolicname=symbolicname,
                family='DATA',
                files=filelist)
            pass
        pass

    def automake_install_private_headers_(self, makefile_am):

        # now for the private header files. this is a bit more
        # complicated as we have to do it by hand, using the all-local
        # hook.

        makefile_am.add_all_local('confix-install-local')
        makefile_am.add_clean_local('confix-clean-local')

        install_local_rule = Rule(targets=['confix-install-local'], prerequisites=[], commands=[])
        clean_local_rule = Rule(targets=['confix-clean-local'], prerequisites=[], commands=[])
        makefile_am.add_element(install_local_rule)        
        makefile_am.add_element(clean_local_rule)

        dir2file_dict = self.dir2filedict_(self.private_headers_)

        for (installpath, files) in dir2file_dict.iteritems():
            if len(installpath):
                targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR, installpath])
            else:
                targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR])
                pass
            
            # add mkdir rules for every subdirectory
            makefile_am.add_element(
                Rule(targets=[targetdir],
                     prerequisites=[],
                     commands=['-$(mkinstalldirs) '+targetdir]))

            # copy files
            for f in files:
                targetfile = '/'.join([targetdir, f])
                makefile_am.add_element(
                    Rule(targets=[targetfile],
                         prerequisites=[f, targetdir],
                         # I tried with 'cp -fp $< targetdir', but
                         # this is not portable make.
                         commands=['set junk $?; shift; cp -fp $$1 '+targetdir,
                                   'chmod 0444 '+targetfile]))
                makefile_am.add_element(
                    Rule(targets=[targetfile+'-clean'],
                         prerequisites=[],
                         commands=['rm -f '+targetfile]))
                install_local_rule.add_prerequisite(targetfile)
                clean_local_rule.add_prerequisite(targetfile+'-clean')
                pass
            pass
        pass

##         install_targets = []
##         clean_targets = []

##         makefile_am.add_lines(
##             ['',
##              '# install header files local to the package'])

##         for dirname, filelist in self.dir2filedict_(file2dirdict=self.private_headers_).iteritems():
##             if len(dirname):
##                 targetdir  = os.path.join('$(top_builddir)', const.LOCAL_INCLUDE_DIR, dirname)
##             else:
##                 targetdir  = os.path.join('$(top_builddir)', const.LOCAL_INCLUDE_DIR)
##                 pass

##             clean_targets = []
##             for filename in filelist:
##                 makefile_am.add_line('')
##                 targetfile = os.path.join(targetdir, filename)
##                 makefile_am.add_lines(helper_automake.format_rule(
##                     targets=[targetfile],
##                     prerequisites=[filename],
##                     commands=['-@$(mkinstalldirs) '+targetdir,
##                               '@cp -fp $? '+' '+targetdir,
##                               '@chmod 0444 '+targetfile]
##                     ))
##                 install_targets.append(targetfile)

##                 clean_target = targetfile+'-clean'
##                 clean_targets.append(clean_target)
##                 buildmod.makefile_am().add_lines(helper_automake.format_rule(
##                     targets=[clean_target],
##                     prerequisites=[],
##                     commands=['@rm -f '+targetfile]
##                     ))
##                 pass
##             buildmod.makefile_am().add_lines(helper_automake.format_rule(
##                 targets=['.PHONY'],
##                 prerequisites=clean_targets,
##                 commands=[]
##                 ))
##             pass

##         buildmod.makefile_am().add_line('')
##         buildmod.makefile_am().add_lines(helper_automake.format_rule(
##             targets=[FileInstaller.TARGET_INSTALL_LOCAL],
##             prerequisites=install_targets))
##         buildmod.makefile_am().add_lines(helper_automake.format_rule(
##             targets=[FileInstaller.TARGET_CLEAN_LOCAL],
##             prerequisites=clean_targets))
##         pass





##     def bulk_install_public_headers_(self):
##         lines = []
##         for f, dirlist in self.public_headers_.iteritems():
##             base = '$(builddir)/'+f+',$(srcdir)/'+f+':0644:$(includedir)'
##             for d in dirlist:
##                 if len(d):
##                     lines.append(base+'/'+d)
##                 else:
##                     lines.append(base)
##                     pass
##                 pass
##             pass
##         return lines
        
##     def bulk_install_datafiles_(self):
##         lines = []
##         for f, dirlist in self.datafiles_.iteritems():
##             base = '$(builddir)/'+f+',$(srcdir)/'+f+':0644:$(datadir)'
##             for d in dirlist:
##                 if len(d):
##                     lines.append(base+'/'+d)
##                 else:
##                     lines.append(base)
##                     pass
##                 pass
##             pass
##         return lines

##     def bulk_install_prefixfiles_(self):
##         lines = []
##         for f, dirlist in self.prefixfiles_.iteritems():
##             base = '$(builddir)/'+f+',$(srcdir)/'+f+':0644:$(prefix)'
##             for d in dirlist:
##                 if len(d):
##                     lines.append(base+'/'+d)
##                 else:
##                     lines.append(base)
##                     pass
##                 pass
##             pass
##         return lines

##     def bulk_install_tunnelfiles_(self):
##         lines = []
##         for f, dirlist in self.tunnelfiles_.iteritems():
##             base = '$(builddir)/'+f+',$(srcdir)/'+f+':0644:'
##             for d in dirlist:
##                 lines.append(base+d)
##                 pass
##             pass
##         return lines

##     def bulk_install_private_headers_(self):
##         lines = []
##         for f, dirlist in self.private_headers_.iteritems():
##             base = '$(builddir)/'+f+',$(srcdir)/'+f+':0644:$(localincludedir)'
##             for d in dirlist:
##                 if len(d):
##                     lines.append(base+'/'+d)
##                 else:
##                     lines.append(base)
##                     pass
##                 pass
##             pass
##         return lines

    def compute_install_dirname_(self, str):
        return helper_automake.automake_name(FileInstaller.re_subst.sub('', str))

    def add_to_file2dirdict_(self, file2dirdict, filetype_errmsg, filename, dir):
        assert type(dir) in (types.ListType, types.TupleType), str(dir)
        the_dir = os.sep.join(dir)
        if the_dir is None:
            the_dir = ''
            pass
        dirset = file2dirdict.get(filename)
        if dirset is None:
            dirset = set()
            file2dirdict[filename] = dirset
            pass
        if the_dir in dirset:
            raise Error(filetype_errmsg+' "'+filename+'" installed to "'+the_dir+'" twice')
        dirset.add(the_dir)
        pass

    def dir2filedict_(self, file2dirdict):
        ret = {}
        for filename, dirset in file2dirdict.iteritems():
            for d in dirset:
                filelist = ret.get(d)
                if filelist is None:
                    filelist = []
                    ret[d] = filelist
                    pass
                filelist.append(filename)
                pass
            pass
        return ret

    pass


## enable_bulk_install_option = """

## AC_ARG_ENABLE(
##     bulk-install,
##     AC_HELP_STRING([--enable-bulk-install]
##                    [Install all files using a dedicated program rather than installing files one-by-one]),
##     [
##     case $enableval in
##         yes) bulk_install=true;;
##         *) bulk_install=false;;
##     esac
##     ],
##     [
##     bulk_install=false
##     ])
## AM_CONDITIONAL(BULK_INSTALL,test x$bulk_install = xtrue)

## """
