# Copyright (C) 2009-2010 Joerg Faschingbauer

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

import cmake_consts
from cmakelists import CMakeLists
from aux_dir_builders import ModulesDirectoryBuilder
from aux_dir_builders import ScriptsDirectoryBuilder
from buildinfo import BuildInfo_Toplevel_CMakeLists_Include
from buildinfo import BuildInfo_Toplevel_CMakeLists_FindCall
from buildinfo import BuildInfo_CMakeModule

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.repo import AutomakePackageRepository
from libconfix.core.hierarchy.dirbuilder import DirectoryBuilder
from libconfix.core.hierarchy import confix_admin
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils import const

import itertools

def find_cmake_output_builder(dirbuilder):
    """
    Find the directory's dedicated automake output builder.
    """
    for b in dirbuilder.iter_builders():
        if type(b) is CMakeBackendOutputBuilder:
            return b
        pass
    else:
        assert False
        pass
    pass

class CMakeBackendOutputBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__local_cmakelists = None
        self.__top_cmakelists = None
        self.__modules_dir_builder = None
        self.__scripts_dir_builder = None
        self.__bursted = False

        # remember the dependency graph for use in output(). (we
        # generated inter-node dependencies to force module build
        # order.)
        self.__last_digraph = None
        pass

    def local_cmakelists(self):
        return self.__local_cmakelists

    def top_cmakelists(self):
        return self.__top_cmakelists

    def add_module_file(self, name, lines):
        """
        Add a file @name (consisting of @lines) to the package's
        Modules directory.
        """
        self.__modules_dir_builder.add_module_file(name, lines)
        pass

    def add_scripts_file(self, name, lines):
        """
        Add a file @name (consisting of @lines) to the package's
        Scripts directory.
        """
        self.__scripts_dir_builder.add_script_file(name, lines)
        pass

    def locally_unique_id(self):
        return str(self.__class__)

    def initialize(self, package):
        super(CMakeBackendOutputBuilder, self).initialize(package)

        # CMakeLists.txt files all over
        self.__local_cmakelists = CMakeLists()
        if self.parentbuilder() is package.rootbuilder():
            self.__top_cmakelists = self.__local_cmakelists
            pass
        else:
            top_cmake_builder = find_cmake_output_builder(package.rootbuilder())
            self.__top_cmakelists = top_cmake_builder.local_cmakelists()
            pass
        pass

        # if in the top directory, add the CMake admin section to
        # confix-admin. if not in the top directory, steal it from
        # there.
        if self.parentbuilder() is self.package().rootbuilder():
            # create the directory hierarchy if necessary.
            admin_dir_builder = confix_admin.add_confix_admin(self.package())
            cmake_dir = admin_dir_builder.directory().get('cmake')
            if cmake_dir is None:
                cmake_dir = admin_dir_builder.directory().add(name='cmake', entry=Directory())
                pass
            modules_dir = cmake_dir.get('Modules')
            if modules_dir is None:
                modules_dir = cmake_dir.add(name='Modules', entry=Directory())
                pass
            scripts_dir = cmake_dir.get('Scripts')
            if scripts_dir is None:
                scripts_dir = cmake_dir.add(name='Scripts', entry=Directory())
                pass

            # wrap builder hierarchy around directory hierarchy. NOTE
            # that the modules and scripts directory builders are
            # backend builders.
            cmake_dir_builder = admin_dir_builder.add_builder(DirectoryBuilder(directory=cmake_dir))
            self.__modules_dir_builder = cmake_dir_builder.add_backend_builder(ModulesDirectoryBuilder(directory=modules_dir))
            self.__scripts_dir_builder = cmake_dir_builder.add_backend_builder(ScriptsDirectoryBuilder(directory=scripts_dir))
        else:
            self.__modules_dir_builder = find_cmake_output_builder(self.package().rootbuilder()).__modules_dir_builder
            self.__scripts_dir_builder = find_cmake_output_builder(self.package().rootbuilder()).__scripts_dir_builder
            pass

        pass

    def relate(self, node, digraph, topolist):
        super(CMakeBackendOutputBuilder, self).relate(node, digraph, topolist)

        for n in topolist:
            for bi in n.iter_buildinfos_type(BuildInfo_Toplevel_CMakeLists_Include):
                self.__top_cmakelists.add_include(bi.include())
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_Toplevel_CMakeLists_FindCall):
                self.__top_cmakelists.add_find_call(bi.find_call())
                pass
            for bi in n.iter_buildinfos_type(BuildInfo_CMakeModule):
                self.__modules_dir_builder.add_module_file(bi.name(), bi.lines())
                pass
            pass

        self.__last_digraph = digraph
        pass
                    
    def output(self):
        # if in the top directory, our CMakeLists.txt file needs to
        # contain a lot of boilerplate things, in addition to its
        # regular module content.
        if self.parentbuilder() is self.package().rootbuilder():
            self.__output_top_cmakelists()
            pass

        # generate additional dependencies to work around CMake bug
        # #10082
        # ================================================================

        # CMake calls make recursively in an extremely idiotic way
        # which renders it almost unusable for parallel make. in the
        # presence of code generators and explicit 'all' targets this
        # can lead to multiple parallel invocations of the same code
        # generator. depending on the code generator, this will result
        # in an error (if you are lucky), or lead to subtle bugs -
        # without any error.

        # specify explicit dependencies between nodes
        # -------------------------------------------
        
        # it is obviously a good idea to specify as many explicit
        # dependencies as we can. we maintain a directed graph between
        # directories anyway, so we can add the following.

        # * a node-specific target for my own node. this is to let
        #   others point an edge towards us.

        # * dependencies from my node-specific target to all of my
        #   node's toplevel targets (executable, libraries, and custom
        #   targets). when somebody points an edge towards us, then
        #   this way we make sure that all that we have is built.

        # * dependencies from my node's toplevel targets to all
        #   toplevel targets of my node's successors. this is a
        #   necessary refinement of the above.

        # * dependencies from my node-specific target to all successor
        #   nodes' node-specific targets. this is not strictly
        #   necessary, but it sure can't hurt.

        # chain a node's 'all' targets together
        # -------------------------------------

        # in order to prevent multiple parallel 'all' entry points
        # into one node (and thus parallel build failures), we
        # artificially chain together everything that would be
        # triggered by 'make all'. this way we force linearization
        # inside one directory. it is likely that an otherwise correct
        # parallel build is slowed down by this: the 'all' entry
        # points into a directory can well be independent. but we sure
        # take that penalty in order to yield a correct build.
        
        if True:
            assert self.__last_digraph is not None

            toplevel_targets = list(itertools.chain(
                    self.__local_cmakelists.iter_executable_target_names(),
                    self.__local_cmakelists.iter_library_target_names(),
                    self.__local_cmakelists.iter_custom_target_names()))
            
            # dependencies to my node's toplevel targets
            self.__local_cmakelists.add_dependencies(
                name=self.__node_specific_target_name(self.parentbuilder()),
                depends=toplevel_targets,
                comment=['edge from my node\'s node-specific target to',
                         'all toplevel targets of this directory'])

            # node-specific target. add this after the outgoing
            # dependencies, or else we have a cycle.
            self.__local_cmakelists.add_custom_target(
                name=self.__node_specific_target_name(self.parentbuilder()),
                depends=[],
                all=False,
                comment='node-specific target for this directory')

            # outgoing dependencies ...

            # determine the successors for later use.
            successor_nodes = []
            for succ in self.__last_digraph.successors(self.parentbuilder()):
                if isinstance(succ, DirectoryBuilder):
                    # exclude installed nodes
                    successor_nodes.append(succ)
                    pass
                pass
            
            # dependencies from the node-specific target to all
            # successors' node-specific targets.
            self.__local_cmakelists.add_dependencies(
                name=self.__node_specific_target_name(self.parentbuilder()),
                depends=[self.__node_specific_target_name(succ) for succ in successor_nodes],
                comment=["edges from this directory's node-specific target",
                         "to all successors' node-specific targets"])

            # dependencies from each top-level target to all
            # successors' node-specific targets
            for t in toplevel_targets:
                self.__local_cmakelists.add_dependencies(
                    name=t,
                    depends=[self.__node_specific_target_name(succ) for succ in successor_nodes],
                    comment=["edges from top-level target "+t+" to",
                             "all successors' node-specific targets"])
                pass

#             # intra-package dependencies...
#             for succ in self.__last_digraph.successors(self.parentbuilder()):
#                 if not isinstance(succ, DirectoryBuilder):
#                     # exclude installed nodes
#                     continue
# 
#                 succ_name = '.'.join(succ.directory().relpath(self.package().rootbuilder().directory()))
# 
#                 # node-specific target dependencies
#                 self.__local_cmakelists.add_dependencies(
#                     name=local_target,
#                     depends=['confix-internal-node-target-'+succ_name],
#                     comment=['edge from this node to successor node ', succ_name])
# 
#                 # dependencies from my node's toplevel targets to
#                 # every successor's toplevel targets.
#                 succ_cmakelists = find_cmake_output_builder(succ).local_cmakelists()
#                 for local_toptarget in itertools.chain(self.__local_cmakelists.iter_executable_target_names(),
#                                                        self.__local_cmakelists.iter_library_target_names(),
#                                                        self.__local_cmakelists.iter_custom_target_names()):
#                     for succ_toptarget in itertools.chain(succ_cmakelists.iter_executable_target_names(),
#                                                           succ_cmakelists.iter_library_target_names(),
#                                                           succ_cmakelists.iter_custom_target_names()):
#                         self.__local_cmakelists.add_dependencies(
#                             name=local_toptarget,
#                             depends=[succ_toptarget],
#                             comment=['edge from this node\'s target "'+local_toptarget+'"',
#                                      'to target "'+succ_toptarget+'" of node ',
#                                      succ_name])
#                         pass
#                     pass
#                 pass
# 
#             # chain 'all' entry points together.
#             all_targets = []
#             for target_name in self.__local_cmakelists.iter_custom_target_names():
#                 if self.__local_cmakelists.custom_target_is_all(target_name):
#                     all_targets.append(target_name)
#                     pass
#                 pass
#             all_targets.extend(list(self.__local_cmakelists.iter_executable_target_names()))
#             all_targets.extend(list(self.__local_cmakelists.iter_library_target_names()))
#             for i in xrange(len(all_targets)):
#                 if i+1 == len(all_targets):
#                     break
#                 self.__local_cmakelists.add_dependencies(
#                     name=all_targets[i],
#                     depends=[all_targets[i+1]],
#                     comment='artificial all-target chaining')
#                 pass
#             pass

        # write the CMakeLists.txt file.
        cmakelists_file = self.parentbuilder().directory().find(['CMakeLists.txt'])
        if cmakelists_file is None:
            cmakelists_file = File()
            self.parentbuilder().directory().add(name='CMakeLists.txt', entry=cmakelists_file)
        else:
            cmakelists_file.truncate()
            pass
        cmakelists_file.add_lines(self.__local_cmakelists.lines())

        # NOTE: this has to come last because we add stuff to the
        # ModulesDirectoryBuilder, and he has to come after us.
        super(CMakeBackendOutputBuilder, self).output()
        pass

    def __output_top_cmakelists(self):
        top_cmakelists = find_cmake_output_builder(self.parentbuilder()).top_cmakelists()

        # project name and version. extract as much from confix's
        # package properties as we can.
        # FIXME: rest of the package's properties.
        top_cmakelists.set_project(self.package().name())
        top_cmakelists.add_set('VERSION', self.package().version())

        # CMake requires us to write something like that.
        top_cmakelists.add_cmake_minimum_required('VERSION', '2.6')

        # in case we add our own modules, point the include path
        # there.
        top_cmakelists.add_set(
            'CMAKE_MODULE_PATH',
            '${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/%s"' % cmake_consts.modules_dir)

        # rpath wizardry
        self.__apply_rpath_settings(top_cmakelists)

        # CPack wizardry
        self.__apply_cpack_settings(top_cmakelists)

        # piggy-back repo install
        if True:
            top_cmakelists.add_install__files(
                files=[self.package().repofilename()],
                destination=AutomakePackageRepository.REPO_FULL_PATH)

            # add a custom target 'repo-install' to give the user the
            # possibility to install the repo file without building
            # the package first. (Salomon wants this - if it hurts one
            # day, we can easily make it a plugin there.)
            installed_file = '${CMAKE_INSTALL_PREFIX}/'+\
                             '/'.join(AutomakePackageRepository.REPO_FULL_PATH)+\
                             '/'+self.package().repofilename()
            top_cmakelists.add_custom_command__output(
                outputs=[installed_file],
                commands=[('${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/%s %s' % \
                           (self.package().repofilename(), installed_file), [])],
                depends=['${CMAKE_CURRENT_SOURCE_DIR}/%s' % self.package().repofilename()])
            top_cmakelists.add_custom_target(
                name='repo-install',
                all=False,
                depends=[installed_file])
            pass

        # register subdirectories with our toplevel CMakeLists.txt
        for dirnode in self.package().topo_directories():
            assert isinstance(dirnode, DirectoryBuilder)
            relpath = dirnode.directory().relpath(self.package().rootdirectory())
            if len(relpath) == 0:
                continue # don't add package root
            self.local_cmakelists().add_subdirectory('/'.join(relpath))
            pass
        pass

    def __apply_rpath_settings(self, top_cmakelists):
        # RPATH settings, according to
        # http://www.vtk.org/Wiki/CMake_RPATH_handling. this ought to
        # be the way that we know from automake/libtool.

        # use, i.e. don't skip the full RPATH for the build tree
        top_cmakelists.add_set('CMAKE_SKIP_BUILD_RPATH', 'FALSE')

        # when building, don't use the install RPATH already (but
        # later on when installing)
        top_cmakelists.add_set('CMAKE_BUILD_WITH_INSTALL_RPATH', 'FALSE')

        # the RPATH to be used when installing
        top_cmakelists.add_set('CMAKE_INSTALL_RPATH', "${CMAKE_INSTALL_PREFIX}/lib")

        # add the automatically determined parts of the RPATH which
        # point to directories outside the build tree to the install
        # RPATH
        top_cmakelists.add_set('CMAKE_INSTALL_RPATH_USE_LINK_PATH', 'TRUE')

        # version information.
        version_parts = self.package().version().split('.')
        if (len(version_parts) >= 1):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_MAJOR', version_parts[0])
            pass
        if (len(version_parts) >= 2):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_MINOR', version_parts[1])
            pass
        if (len(version_parts) >= 3):
            top_cmakelists.add_set('CPACK_PACKAGE_VERSION_PATCH', version_parts[2])
            pass
        
        pass

    def __apply_cpack_settings(self, top_cmakelists):
        top_cmakelists.add_include('CPack')
        top_cmakelists.add_set('CPACK_SOURCE_PACKAGE_FILE_NAME', '"${PROJECT_NAME}-${VERSION}"')
        top_cmakelists.add_set('CPACK_SOURCE_IGNORE_FILES', "${CPACK_SOURCE_IGNORE_FILES};~\$")
        pass

    @staticmethod
    def __node_specific_target_name(dirbuilder):
        assert isinstance(dirbuilder, DirectoryBuilder)
        return 'confix-node-specific-target--'+'.'.join(dirbuilder.directory().relpath(dirbuilder.package().rootbuilder().directory()))
    
    pass
