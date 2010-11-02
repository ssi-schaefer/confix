# Copyright (C) 2010 Joerg Faschingbauer

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

from aux_dir_builders import ScriptsDirectoryBuilder
import cmake_consts

import hashlib
import itertools

class CustomCommandHelper(object):

    SCRIPT_NAME = 'confix-cmake-generator-lock-loop'

    """
    Helps deal with all the ADD_CUSTOM_COMMAND(OUTPUT ...) hassle.

    CMake doesn't get their ADD_CUSTOM_COMMAND() invocations
    right. During parallel build it happens that code generators run
    multiple times in parallel - when multiple dependencies point
    towards the generator. See CMake bug #10082,
    http://public.kitware.com/Bug/view.php?id=10082.

    During initialization, the cmake output builder creates a
    ScriptsDirectoryBuilder where we put a wrapper script. The wrapper
    script contains logic to guard against multiple invocations, and
    executes the commands that the user thinks are part of
    ADD_CUSTOM_COMMAND() invocation. The only command of an
    ADD_CUSTOM_COMMAND() is a call to the wrapper script. (But read
    on.)

    The directory_buider ctor argument is my creator's parentbuilder
    that I need to make the MD5 hash unique. One hack implies another
    and another, as always.
    """

    def __init__(self, parent_builder, scripts_directory_builder):
        assert isinstance(scripts_directory_builder, ScriptsDirectoryBuilder)
        assert parent_builder is not None
        self.__parent_builder = parent_builder
        self.__scripts_directory_builder = scripts_directory_builder
        pass

    # def create_custom_command_bullshit(self, cmakelists, outputs, commands, depends, working_directory, comment):
    #     assert len(outputs)>0, "custom command that doesn't generate anything?"

    #     custom_command_md5 = hashlib.md5()
    #     for o in outputs + self.__parent_builder.directory().relpath(self.__parent_builder.package().rootdirectory()):
    #         custom_command_md5.update(o)
    #         pass

    #     custom_command_key = custom_command_md5.hexdigest()

    #     self.__scripts_directory_builder.add_script_file(
    #         name=self.SCRIPT_NAME,
    #         lines=[
    #             '#!/bin/sh',
    #             '',
    #             'LOCKDIR=.confix-generator-lock-$1',
    #             '',
    #             'wait=no',
    #             'mkdir ${LOCKDIR} 2>/dev/null || wait=yes',
    #             '',
    #             'if test "${wait}" = "yes"; then',
    #             '    echo "$$: waiting"',
    #             '    while test -d ${LOCKDIR}; do',
    #             '        echo Lock directory "${LOCKDIR} is (still?) in place; generator running"',
    #             '        sleep 1',
    #             '    done',
    #             'else',
    #             '    # trapping condition 0 means trapping "EXIT"',
    #             '    trap "rmdir ${LOCKDIR}" 0',
    #             '    while read cmd; do',
    #             '        echo executing ${cmd} 2>&1',
    #             '        (eval ${cmd}) || { _status=$?; echo Error: ${cmd}; exit $_status; }',
    #             '    done',
    #             'fi',
    #             ])

    #     # custom command to create the commands file.
    #     command_file_name = '.commands-'+custom_command_key
    #     command_file_create_commands = [('rm', ['-f', command_file_name])]
    #     for c in commands:
    #         if len(c[1]) > 0:
    #             esc_command = ' '.join([c[0]] + c[1])
    #         else:
    #             esc_command = c[0]
    #             pass
    #         # see
    #         # tests/handwritten-prototypes/add_custom_command__quoting
    #         # for an example.
    #         esc_command = esc_command.replace('"', r'\\\"')
    #         esc_command = esc_command.replace('(', r'\\\(')
    #         esc_command = esc_command.replace(')', r'\\\)')
    #         esc_command = esc_command.replace("'", r"\\\\'")
    #         esc_command = esc_command.replace('<', r'\\<')
    #         esc_command = esc_command.replace('>', r'\\>')
    #         command_file_create_commands.append(('echo', [esc_command + ' >> ' + command_file_name]))
    #         pass

    #     cmakelists.add_custom_command__output_internal(
    #         outputs=['.commands-'+custom_command_key],
    #         commands=command_file_create_commands,
    #         depends=depends,
    #         working_directory=working_directory,
    #         comment=comment)

    #     cmakelists.add_custom_command__output_internal(
    #         outputs=outputs,
    #         commands=[('${CMAKE_SOURCE_DIR}/'+cmake_consts.scripts_dir+'/'+self.SCRIPT_NAME,
    #                    [custom_command_key, ' < ' + command_file_name])],
    #         depends=[command_file_name],
    #         working_directory=working_directory,
    #         comment=comment)

    #     cmakelists.add_custom_target(
    #         name='confix-internal-custom-command-target-'+custom_command_key,
    #         depends=[outputs[0]],
    #         all=False,
    #         comment=comment)

    #     pass

    def create_custom_command_bullshit(self, cmakelists, outputs, commands, depends, working_directory, comment):
        assert len(outputs)>0, "custom command that doesn't generate anything?"

        custom_command_md5 = hashlib.md5()
        # jjj generate even more unique key
        for o in outputs + self.__parent_builder.directory().relpath(self.__parent_builder.package().rootdirectory()):
            custom_command_md5.update(o)
            pass

        custom_command_key = custom_command_md5.hexdigest()

        self.__scripts_directory_builder.add_script_file(
            name='wait-for-lock',
            lines=[
                '#!/bin/sh',
                '',
                'LOCKDIR=$1',
                '',
                'if ! mkdir ${LOCKDIR} then',
                '    while [ -d ${LOCKDIR} ]; do',
                '        echo \'Lock directory ${LOCKDIR} is (still?) in place; generator running\'',
                '        sleep 1',
                '    done',
                'fi',
                ])
    

jjjjj wait-for-lock lockfile
jjjjj echo futsau | execute-if-locked lockfile # mit quoting von vorher

        
        # jjj document this crap
        lock_dir = '.confix-generator-lock-' + custom_command_key
        real_commands = []
        real_commands.append(
            ('mkdir '+lock_dir+' || '
             'while [ -d '+lock_dir+' ]; do \'echo Lock directory '+lock_dir+' is in place; generator running\'; sleep 1; done', []))
        for c in commands:
            real_commands.append(('[ -d '+lock_dir+' ] || exit 0;', [c[0]] + c[1] + ['|| rmdir '+lock_dir]))
            pass
        real_commands.append(('rmdir '+lock_dir+' 2>/dev/null', []))

        cmakelists.add_custom_command__output_internal(
            outputs=outputs,
            commands=real_commands,
            depends=depends,
            working_directory=working_directory,
            comment=comment)

        cmakelists.add_custom_target(
            name='confix-internal-custom-command-target-'+custom_command_key,
            depends=[outputs[0]],
            all=False,
            comment=comment)

        pass


    pass
