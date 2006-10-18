# $Id: buildable_mgr.py,v 1.14 2006/03/22 15:03:54 jfasch Exp $

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

from buildable_mgr_bases import \
     BuildableCluster, \
     BuildableClusterer, \
     BuildableCreator
from buildable import Buildable
from core.error import Error
import core.debug
import core.helper

import dircache
import os
import re

class BuildableManager:

    def __init__(self, global_mgr=None):

        self.global_mgr_ = global_mgr
        self.creators_ = []
        self.clusterers_ = []
        pass

    def register_creator(self, regex, c):

        assert isinstance(c, BuildableCreator)

        try:
            compiled_regex = re.compile(regex)
        except:
            raise Error('Could not compile regular expression "'+regex+'"')
        
        self.creators_.append((compiled_regex, regex, c))

    def register_clusterer(self, c):

        assert isinstance(c, BuildableClusterer)
        self.clusterers_.append(c)

    def create_from_file(self, dir, filename):
        buildable = None
        
        for (compiled_regex, regex, c) in self.creators_:
            if compiled_regex.search(filename):
                buildable = c.create_from_file(
                    dir=dir,
                    filename=filename,
                    lines=core.helper.lines_of_file(os.path.join(dir, filename)))
                if not buildable:
                    raise Error('Regex "'+regex+'" was said to create buildables, '
                                'but it does not with file "'+os.path.join(dir, filename)+'"')
                break
            pass

        if self.global_mgr_ and not buildable:
            buildable = self.global_mgr_.create_from_file(dir=dir, filename=filename)

        return buildable

    def create_from_dir(self, dir, ignore_files):

        """ Examine the files in the given directory. From these we
        know about, create a list of Buildable objects and return
        that.

        @type  dir: string

        @param dir: The directory in which to look for source files.

        @type ignore_files: list of string

        @param ignore_files: a list of filenames which no buildable
        objects should be generated for.

        @rtype: list of L{buildable.Buildable}

        @return: A list of all the Buildable objects that make sense
        to construct from the sources in this directory. It is worth
        repeating that a single directory is not allowed to hold
        sources for both libraries and executables (either programs or
        checks). (That's bad code layout anyway.)
        
        """

        # first, create a buildable for every file whose type we know.
        # collect buildable files in the directory, uncritically.

        buildables = []

        if os.path.isdir(dir):
            for f in dircache.listdir(dir):

                if os.path.isfile(os.path.join(dir, f)) \
                       and f not in ignore_files:                
                    b = self.create_from_file(dir=dir, filename=f)
                    if b:
                        buildables.append(b)
                        pass
                    pass
                pass
            pass

        return buildables

    def create_clusters(self, buildables, module):

        active = buildables[:]
        passive = []
        clusters = []

        there_were_changes = 1

        core.debug.trace(['cluster'], 'clustering in '+'.'.join(module.localname()))

        while there_were_changes:

            there_were_changes = 0

            debug_cluster('ENTER', active, passive, clusters)

            # GENERATE-FROM-ACTIVE pass

            generated_active_buildables = []
            for b in active:
                gen = b.generate_buildables()
                for g in gen:
                    # paranoia
                    assert not g in active+generated_active_buildables
                generated_active_buildables.extend(gen)

            there_were_changes += len(generated_active_buildables)
            active.extend(generated_active_buildables)

            debug_cluster('GENERATE-FROM-ACTIVE', active, passive, clusters)

            # GENERATE-FROM-CLUSTERS pass
            
            generated_cluster_buildables = []
            for c in clusters:
                gen = c.generate_buildables()
                for g in gen:
                    # paranoia, again
                    assert not g in active+generated_cluster_buildables
                generated_cluster_buildables.extend(gen)

            there_were_changes += len(generated_cluster_buildables)
            active.extend(generated_cluster_buildables)

            debug_cluster('GENERATE-FROM-CLUSTERS', active, passive, clusters)

            # MAKE-CLUSTERS pass

            generated_clusters = []

            clusterers = self.clusterers_[:]
            if self.global_mgr_:
                clusterers.extend(self.global_mgr_.clusterers_)
            for c in clusterers:
                gen = c.make_clusters(active, clusters, module)
                for g in gen:
                    # ... and over and over again ...
                    assert not g in clusters+generated_clusters
                generated_clusters.extend(gen)

            there_were_changes += len(generated_clusters)
            clusters.extend(generated_clusters)

            debug_cluster('MAKE-CLUSTERS', active, passive, clusters)

            # ASSIGN-TO-CLUSTERS pass

            new_active = []
            for a in active:
                action = BuildableCluster.ADD_REJECT
                for c in clusters:
                    rv = c.cluster_add(a)
                    if rv == BuildableCluster.ADD_REJECT: pass
                    elif rv == BuildableCluster.ADD_EXCLUSIVE:
                        if action == BuildableCluster.ADD_SHARED:
                            raise Error('BuildableCluster '+c.__class__.__name__+''
                                        '('+c.name()+') is misbehaving: '
                                        'cannot take buildable '+a.name()+' '
                                        'exclusively when another cluster has '
                                        'already taken it shared')
                        action = BuildableCluster.ADD_EXCLUSIVE
                    elif rv == BuildableCluster.ADD_SHARED:
                        if action == BuildableCluster.ADD_EXCLUSIVE:
                            raise Error('BuildableCluster '+c.__class__.__name__+''
                                        '('+c.name()+') is misbehaving: '
                                        'cannot take buildable '+a.name()+' '
                                        'shared when another cluster has '
                                        'already taken it exclusively')
                        action = BuildableCluster.ADD_SHARED
                    elif rv == BuildableCluster.ADD_NOCHANGE: pass
                    else: assert 0
                    pass

                if action == BuildableCluster.ADD_EXCLUSIVE:
                    passive.append(a)
                    there_were_changes += 1
                elif action == BuildableCluster.ADD_SHARED:
                    new_active.append(a)
                    there_were_changes += 1
                else:
                    new_active.append(a)

                pass

            active = new_active

            debug_cluster('ASSIGN-TO-CLUSTERS', active, passive, clusters)

            pass

        # legally, clusters need not be buildables, so we cannot
        # return them all. currently, all of them are, but, y'know,
        # the law ...

        buildable_clusters = []
        for c in clusters:
            if isinstance(c, Buildable):
                buildable_clusters.append(c)

        return active + passive + buildable_clusters

BuildableManager.instance = BuildableManager()


def debug_cluster(heading, active, passive, clusters):

    core.debug.trace(['cluster'], heading)
    core.debug.indent()

    core.debug.trace(['cluster'], 'ACTIVE')
    core.debug.indent()
    for a in active:
        core.debug.trace(['cluster'], a.__class__.__name__+':'+a.name())
    core.debug.outdent()

    core.debug.trace(['cluster'], 'PASSIVE')
    core.debug.indent()
    for p in passive:
        core.debug.trace(['cluster'], p.__class__.__name__+':'+p.name())
    core.debug.outdent()

    core.debug.trace(['cluster'], 'CLUSTERS')
    core.debug.indent()
    for c in clusters:
        core.debug.trace(['cluster'], c.__class__.__name__+':'+c.name())
        core.debug.indent()
        for m in c.members():
            core.debug.trace(['cluster'], m.__class__.__name__+':'+m.name())
        core.debug.outdent()
    core.debug.outdent()

    core.debug.outdent()
