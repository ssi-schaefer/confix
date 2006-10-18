# $Id: buildable_gen_demo_single.py,v 1.10 2005/11/28 21:14:26 jfasch Exp $

# Copyright (C) 2003 Salomon Automation

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

from buildable_mgr_bases import BuildableCreator
from buildable_single import BuildableSingle
from buildable_h import BuildableHeader
from buildable_cxx import BuildableCXX
from fileprops import FileProperties
import helper_automake

class BuildableGeneratorDemo_SingleGeneratorCreator(BuildableCreator):
    def create_from_file(self, dir, filename, lines):
        if filename.endswith('.dummygen'):
            return BuildableGeneratorDemo_SingleGenerator(
                dir=dir,
                filename=filename,
                lines=lines)
        return None

class BuildableGeneratorDemo_SingleGenerator(BuildableSingle):

    """ A demo class for a single-file buildable object which
    generates .h and .cc files from the maintained source file. """

    def __init__(self,
                 dir,
                 filename,
                 lines):

        BuildableSingle.__init__(self,
                                 dir=dir,
                                 filename=filename,
                                 lines=lines)

        self.generated_ = 0

    def generate_buildables(self):

        if self.generated_: return []

        self.generated_ = 1

        root, ext = os.path.splitext(self.filename())

        h = BuildableHeader(dir=self.dir(),
                            filename=root+'.h',
                            lines=[])

        cc = BuildableCXX(dir=self.dir(),
                          filename=root+'.cc',
                          lines=[])
                            
        return [h, cc]

    def contribute_makefile_am(self, buildmod):

        BuildableSingle.contribute_makefile_am(self, buildmod=buildmod)

        root, ext = os.path.splitext(self.filename())

        root_h = root+'.h'
        root_cc = root+'.cc'

        buildmod.makefile_am().add_built_sources(root_h)
        buildmod.makefile_am().add_built_sources(root_cc)

        buildmod.makefile_am().add_lines(
            [
            '# BuildableSingleDummyGenerator, generating files',
            '# from '+self.filename()
            ])
        buildmod.makefile_am().add_lines(helper_automake.format_rule(
            targets=[root_h, root_cc],
            prerequisites=[],
            commands=['python '+\
                      os.path.join('$(srcdir)', self.filename())+\
                      ' h > '+root_h,
                      
                      'python '+\
                      os.path.join('$(srcdir)', self.filename())+\
                      ' cc > '+root_cc]
            ))
