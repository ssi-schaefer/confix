# $Id: buildable_mgr_bases.py,v 1.6 2005/11/28 21:14:26 jfasch Exp $

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

class BuildableCluster:

    """ A cluster of L{Buildable<buildable.Buildable>} objects. Base
    class for all classes that "absorb" other (single-file) buildable
    objects. Objects of this kind take part in the
    L{algorithm<buildable_mgr.BuildableManager>} where single-file
    buildables are gathered together into composite buildables - such
    as a library or an executable.

    Let's take these - library and executable - as examples of the
    responsibilities of objects of type BuildableCluster. During the
    said algorithm, single file buildables are offered to
    clusters. Each cluster may then take that buildable object as
    follows.

      - B{exclusively}; this prevent the buildable from being taken by
        any other cluster in the module. A library, for example, takes
        a compiled object file exclusively - remember, if a module
        decides to build a library, there can be only one library, and
        that library then absorbs all single-file buildables.

      - B{shared}; this leaves the buildable open to be taken by other
        clusters as well. Executables, for example, takes objects that
        do not contain the main() function B{shared} - that is, these
        objects can be taken by other executables as well.

      - B{reject}; a cluster rejects a buildable object when it has no
        idea of what to do with it. A library cluster will not be
        interested in taking a compiled Python object, for example.

      - B{nochange}; a cluster responds this way if it has an idea how
        to handle the buildable object in principle, but that it does
        not want to take it for some reason (it may decide to take it
        later).

    There is no well-founded reason why
    L{buildable_composite.BuildableComposite} is not the starting
    point of this hierarchy. In fact, all classes which are derived
    from BuildableComposite are also derived from
    BuildableCluster. It's just a matter of taste/neurosis to keep the
    responsibilities separated.

    """

    ADD_REJECT = 0
    ADD_EXCLUSIVE = 1
    ADD_SHARED = 2
    ADD_NOCHANGE = 3

    def __init__(self): pass

    def cluster_add(self, buildable):

        assert 0

class BuildableClusterer:

    """ During the L{algorithm<buildable_mgr.BuildableManager>},
    objects of this type are used to determine the clusters.

    """

    def __init__(self): pass

    def make_clusters(self, buildables, existing_clusters, module):

        """ Create clusters from buildables. Take into account the
        clusters that already exist. (For example, we must not create
        a cluster for a library when we already have done so.)

        @param buildables: a list of L{single-file buildable
        objects<buildable_single.BuildableSingle>} which are subject
        to be taken by a cluster.

        @param existing_clusters: Clusters that already exist. This
        parameter prevents a clusterer from creating a L{library
        cluster<buildable_library.BuildableLibrary>} twice, for
        example.

        @type existing_clusters: list of
        L{clusters<buildable_mgr_bases.BuildableCluster>}

        @param module: The module that the created cluster (if any)
        will be a member of. This is mainly used to extract
        constructor parameters for certain clusters.

        @type module: L{modbuild.BuildableModule}
        

        @return: new clusters (or the empty list if there no new
        clusters)

        @rtype: list of
        L{clusters<buildable_mgr_bases.BuildableCluster>}

        """

        assert 0

class BuildableCreator:

    """ Used to wrap a L{(single-file) buildable
    object<buildable_single.BuildableSingle>} around a source file to
    manage its build process. """

    def __init__(self): pass

    def create_from_file(self, dir, filename, lines):
        assert 0
        return None
