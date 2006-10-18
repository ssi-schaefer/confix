# $Id: buildable_gen_demo_cluster.py,v 1.5 2005/02/22 20:40:49 jfasch Exp $

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

from buildable_single import BuildableSingle
from buildable_composite import BuildableComposite
from buildable_cxx import BuildableCXX
from buildable_mgr_bases import \
     BuildableCluster, \
     BuildableClusterer

class BuildableGeneratorDemo_SingleClusterable(BuildableSingle):

    """ Shallow thing, this. Supposed to be taken by a
    BuildableGeneratorDemo_Cluster which then generates .cc and .h
    files. """

    def __init__(self,
                 dir,
                 filename,
                 lines):

        BuildableSingle.__init__(self,
                                 dir=dir,
                                 filename=filename,
                                 lines=lines)

class BuildableGeneratorDemo_Cluster(BuildableComposite, BuildableCluster):

    """ A dummy class that acts like a PDL-Set, but much more
    dummy. """

    def __init__(self,
                 name,
                 dir):
        
        BuildableComposite.__init__(
            self,
            name=name,
            dir=dir)

        BuildableCluster.__init__(self)

        self.has_generated_ = 0

    def cluster_add(self, buildable):

        # reject anything that is not BuildableDummy

        if not isinstance(buildable, BuildableGeneratorDemo_SingleClusterable):
            return BuildableCluster.ADD_REJECT

        assert not buildable in self.members()

        self.add_member(buildable)
        return BuildableCluster.ADD_EXCLUSIVE

    def generate_buildables(self):

        if self.has_generated_: return []

        self.has_generated_ = 1

        generated = []

        for b in self.members():
            root, ext = os.path.splitext(b.filename())
            generated.append(
                BuildableCXX(dir=self.dir(),
                             filename= root + '.cc',
                             lines=[]
                             )
                )
            pass

        return generated

class BuildableGeneratorDemo_Clusterer(BuildableClusterer):

    def make_clusters(self, buildables, existing_clusters, module):

        for c in existing_clusters:
            if isinstance(c, BuildableGeneratorDemo_Cluster):
                return []
            pass

        return [BuildableGeneratorDemo_Cluster(name='.'.join(module.name()),
                                               dir=module.dir())]
    
