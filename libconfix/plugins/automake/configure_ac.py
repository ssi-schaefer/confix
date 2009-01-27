# Copyright (C) 2004-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.utils.error import Error
from libconfix.core.utils.paragraph import OrderedParagraphSet

class Configure_ac:

    # rough ordering scheme according to the recommendations in the
    # autotools book , p.31

    BOILERPLATE = 0
    OPTIONS = 1000
    PROGRAMS = 2000
    LIBRARIES = 3000
    HEADERS = 4000
    TYPEDEFS_AND_STRUCTURES = 5000
    FUNCTIONS = 6000
    OUTPUT = 7000

    def __init__(self):

        # AC_INIT arguments

        self.packagename_ = None
        self.packageversion_ = None

        # AC_CONFIG_SRCDIR argument

        self.unique_file_in_srcdir_ = None

        self.ac_config_aux_dir_ = None

        self.minimum_autoconf_version_ = None

        # arguments to AC_CONFIG_FILES.

        self.ac_config_files_ = set()

        # same with AC_CONFIG_HEADERS.

        self.ac_config_headers_ = {}

        # the package's subdirectories that will be built. we are
        # getting this list, and put the subdirectories' Makefiles
        # into self.ac_config_files_.

        self.subdirs_ = []

        # everything else

        self.ordered_paragraphs_ = OrderedParagraphSet()
        pass

    def packagename(self): return self.packagename_
    def packageversion(self): return self.packageversion_
        
    def set_packagename(self, packagename):

        """ Package name (first argument to AC_INIT). """

        self.packagename_ = packagename

    def set_packageversion(self, packageversion):

        """ Package version (second argument to AC_INIT). """

        self.packageversion_ = packageversion

    def set_unique_file_in_srcdir(self, filename):
        self.unique_file_in_srcdir_ = filename
        pass
    def unique_file_in_srcdir(self):
        return self.unique_file_in_srcdir_

    def ac_config_aux_dir(self): return self.ac_config_aux_dir_
    def set_ac_config_aux_dir(self, dirname):
        self.ac_config_aux_dir_ = dirname
        pass
    
    def set_minimum_autoconf_version(self, version):
        self.minimum_autoconf_version_ = version
        pass

    def ac_config_files(self): return self.ac_config_files_        
    def add_ac_config_files(self, file):
        self.ac_config_files_.add(file)
        pass
    
    def ac_config_headers(self): return self.ac_config_headers_
    def add_ac_config_headers(self, file):
        self.ac_config_headers_[file] = 1
        pass

    def add_paragraph(self, paragraph, order):
        self.ordered_paragraphs_.add(paragraph=paragraph, order=order)
        pass

    def lines(self):

        assert self.packagename_ is not None
        assert self.packageversion_ is not None

        lines = []

        lines.append('AC_INIT('+self.packagename_+','+self.packageversion_+')')

        # set auxdir. note that either automake or autoconf (I believe
        # the former) is very particular about the place where it is
        # invoked - finally I got it only working right after AC_INIT.

        lines.append('AC_CONFIG_AUX_DIR(['+self.ac_config_aux_dir_+'])')

        # makes sense to call AC_PROG_INSTALL right after
        # AC_CONFIG_AUX_DIR.
        
        lines.append('AC_PROG_INSTALL')

        lines.append('AC_CONFIG_SRCDIR('+self.unique_file_in_srcdir_+')')

        assert self.minimum_autoconf_version_ is not None

        lines.append('AC_PREREQ('+self.minimum_autoconf_version_+')')

        # seems like this is a little inconvenience in autoconf. if I
        # call AC_CANONICAL_TARGET from somewhere inside configure.in,
        # behind AM_INIT_AUTOMAKE, I get warnings like below. so I
        # call AC_CANONICAL_TARGET unconditionally before
        # AM_INIT_AUTOMAKE, as part of the boilerplate stuff.

        # configure.in:3114: warning: AC_ARG_PROGRAM was called before AC_CANONICAL_TARGET

        lines.append('AC_CANONICAL_TARGET')

        lines.append('AM_INIT_AUTOMAKE')

        if len(self.ac_config_headers_):
            lines.append('AC_CONFIG_HEADERS('+' '.join(self.ac_config_headers_.keys())+')')
            pass

        if len(self.ac_config_files_):
            lines.append('AC_CONFIG_FILES('+' '.join(self.ac_config_files_)+')')
            pass

        # serialize our paragraphs, and output the lines.

        lines.extend(self.ordered_paragraphs_.lines())

        # and, finally

        lines.append('AC_OUTPUT')

        return lines
