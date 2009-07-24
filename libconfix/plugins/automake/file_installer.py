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

import helper
import makefile

from libconfix.core.utils.error import Error
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.utils import const

import re, os, types

class FileInstaller:

    TARGET_INSTALL_LOCAL = 'confix-install-local'
    TARGET_CLEAN_LOCAL = 'confix-clean-local'

    def __init__(self):

        # dictionary filename -> list of directory paths relative to
        # $(includedir)
        
        self.__public_headers = _InstallDirectoryContainer(error_title='Public header')
        self.__private_headers = _InstallDirectoryContainer(error_title='Private header')

        # same for $(datadir)

        self.__datafiles = _InstallDirectoryContainer(error_title='Data file')

        # same for $(prefix) (dirty thing that, but some people want
        # it)

        self.__prefixfiles = _InstallDirectoryContainer(error_title='Prefix file')

        # same for arbitrary install locations (even more dirty)

        self.__tunnelfiles = _InstallDirectoryContainer(error_title='Tunnel file')
        
        pass

    def add_public_header(self, filename, dir):
        self.__public_headers.add_file(filename=filename, dir=dir)
        pass

    def add_private_header(self, filename, dir):
        self.__private_headers.add_file(filename=filename, dir=dir)
        pass

    def add_datafile(self, filename, dir):
        self.__datafiles.add_file(filename=filename, dir=dir)
        pass

    def add_prefixfile(self, filename, dir):
        self.__prefixfiles.add_file(filename=filename, dir=dir)
        pass
    
    def add_tunnelfile(self, filename, dir):
        return self.__tunnelfiles.add_file(filename=filename, dir=dir)
    def is_public_header_in_dir(self, filename, dir):
        return self.__public_headers.is_file_in_dir(filename=filename, dir=dir)
    def is_private_header_in_dir(self, filename, dir):
        return self.__private_headers.is_file_in_dir(filename=filename, dir=dir)

    def output(self, makefile_am):

        # add our common hook targets that both methods
        # (automake-native and confix-bulk) must provide.

        makefile_am.add_all_local(FileInstaller.TARGET_INSTALL_LOCAL)
        makefile_am.add_clean_local(FileInstaller.TARGET_CLEAN_LOCAL)

        self.automake_install_public_headers_(makefile_am=makefile_am)
        self.automake_install_datafiles_(makefile_am=makefile_am)
        self.automake_install_prefixfiles_(makefile_am=makefile_am)
        self.automake_install_private_headers_(makefile_am=makefile_am)

        pass

    def automake_install_public_headers_(self, makefile_am):
        for reldir, filelist in self.__public_headers.iterate_dirs():
            if len(reldir):
                # define subdirectory
                symbolicname = self.__compute_install_dirname(title='publicheader', dir=reldir)
                makefile_am.define_install_directory(symbolicname=symbolicname,
                                                     dirname='/'.join(['$(includedir)']+reldir))
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
        for dirname, filelist in self.__datafiles.iterate_dirs():
            # define directory
            symbolicname = self.__compute_install_dirname(title='data', dir=dirname)
            makefile_am.define_install_directory(symbolicname=symbolicname,
                                                 dirname='/'.join(['$(datadir)']+dirname))
            makefile_am.add_to_install_directory(
                symbolicname=symbolicname,
                family='DATA',
                files=filelist)
            pass
        pass

    def automake_install_prefixfiles_(self, makefile_am):
        for dirname, filelist in self.__prefixfiles.iterate_dirs():
            # define directory
            symbolicname = self.__compute_install_dirname(title='prefix', dir=dirname)
            makefile_am.define_install_directory(symbolicname=symbolicname,
                                                 dirname='/'.join(['$(prefix)']+dirname))
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

        install_local_rule = makefile.Rule(targets=['confix-install-local'], prerequisites=[], commands=[])
        clean_local_rule = makefile.Rule(targets=['confix-clean-local'], prerequisites=[], commands=[])
        makefile_am.add_element(install_local_rule)        
        makefile_am.add_element(clean_local_rule)

        for installpath, files in self.__private_headers.iterate_dirs():
            if len(installpath):
                targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR]+installpath)
            else:
                targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR])
                pass
            
            # add mkdir rules for every subdirectory
            makefile_am.add_element(
                makefile.Rule(targets=[targetdir],
                              prerequisites=[],
                              commands=['-$(mkinstalldirs) '+targetdir]))

            # copy files
            for f in files:
                targetfile = '/'.join([targetdir, f])
                makefile_am.add_element(
                    makefile.Rule(targets=[targetfile],
                                  prerequisites=[f],
                                  commands=['-@$(mkinstalldirs) '+targetdir,
                                            'cp -fp $? '+' '+targetdir,
                                            'chmod 0444 '+targetfile]))
                makefile_am.add_element(
                    makefile.Rule(targets=[targetfile+'-clean'],
                                  prerequisites=[],
                                  commands=['rm -f '+targetfile]))
                install_local_rule.add_prerequisite(targetfile)
                clean_local_rule.add_prerequisite(targetfile+'-clean')
                pass
            pass
        pass

    re_subst = re.compile('(^[_\d]|\W)')
    def __compute_install_dirname(self, title, dir):
        str = title+'_'+''.join(dir)
        return helper.automake_name(FileInstaller.re_subst.sub('', str))

    pass

class _InstallDirectoryContainer(object):
    def __init__(self, error_title):
        # part of the 'duplicated file' error message
        self.__error_title = error_title
        # per file information:
        # dictionary 'filename' => [[dir]]. tells us in which
        # directories a file is installed.
        self.__files = {}
        # per directory information:
        # dictionary 'hashed_dir' => ([dir], [files]). sadly, lists
        # are not hashable (ok, how could they?), so we have to mangle
        # a key by ourselves.
        self.__directories = {}
        pass
    def add_file(self, filename, dir):
        # per file
        dirlist = self.__files.setdefault(filename, [])
        for d in dirlist:
            if d == dir:
                raise Error(self.__error_title+' '+filename+' already installed in '+'/'.join(dir))
            pass
        dirlist.append(dir)
        # per directory. no error checking required because we already
        # did it with the per file information (which happens to be
        # faster since the list of directories a file is installed to
        # is supposed to be quite small).
        data = self.__directories.setdefault(self.__hash_dir(dir), (dir, []))
        data[1].append(filename)
        pass
    def is_file_in_dir(self, filename, dir):
        dirlist = self.__files.get(filename)
        if dirlist is None:
            return False
        for d in dirlist:
            if d == dir:
                return True
            pass
        return False
    def iterate_dirs(self):
        return self.__directories.itervalues()
    def __hash_dir(self, dir):
        return '/'.join(dir)
