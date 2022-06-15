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

from .aux_dir_builders import ScriptsDirectoryBuilder
from . import cmake_consts

from libconfix.core.utils.error import Error

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
    """

    def __init__(self, parent_builder, scripts_directory_builder):
        assert isinstance(scripts_directory_builder, ScriptsDirectoryBuilder)
        assert parent_builder is not None
        self.__parent_builder = parent_builder
        self.__scripts_directory_builder = scripts_directory_builder
        pass

    def create_custom_command_bullshit(self, cmakelists, outputs, commands, depends, working_directory, comment):
        assert len(outputs)>0, "custom command that doesn't generate anything?"

        custom_command_md5 = hashlib.md5()

        for c in commands:
            custom_command_md5.update(c[0])
            for a in c[1]:
                custom_command_md5.update(a)
                pass
            pass
        for o in outputs + self.__parent_builder.directory().relpath(self.__parent_builder.package().rootdirectory()):
            custom_command_md5.update(o)
            pass

        custom_command_key = custom_command_md5.hexdigest()
        custom_command_lock = 'custom-command-lock--'+custom_command_key

        self.__scripts_directory_builder.add_script_file(
            name='custom-command-lock-wait',
            lines=[
                '#!/bin/sh',
                '',
                'LOCKDIR=$1',
                '',
                'if mkdir ${LOCKDIR} 2>/dev/null; then',
                '    echo "Acquired lock ${LOCKDIR}" 1>&2',
                'else',
                '    while [ -d ${LOCKDIR} ]; do',
                '        echo "Lock directory ${LOCKDIR} is (still?) in place; generator running" 1>&2',
                '        sleep 1',
                '    done',
                'fi',
                ])

        self.__scripts_directory_builder.add_script_file(
            name='custom-command-unlock-if-locked',
            lines=[
                '#!/bin/sh',
                '',
                'LOCKDIR=$1',
                '',
                'if rmdir ${LOCKDIR} 2>/dev/null; then',
                '    echo "Released lock ${LOCKDIR}" 1>&2',
                'fi',
                'exit 0',
                ])

        self.__scripts_directory_builder.add_script_file(
            name='custom-command-lock-exec-if-locked',
            lines=[
                '#!/bin/sh',
                '',
                'LOCKDIR=$1',
                '',
                'read COMMAND',
                'if [ -d ${LOCKDIR} ]; then',
                '    echo "Executing ${COMMAND} lock ${LOCKDIR}" 1>&2',
                '    if (eval ${COMMAND}); then',
                '        exit 0',
                '    else',
                '        _status=$?',
                '        echo "Error: ${COMMAND} lock ${LOCKDIR}" 1>&2',
                '        rmdir ${LOCKDIR}',
                '        exit $_status',
                '    fi',
                '    # eval might have failed (?)',
                '    exit 42',
                'else',
                '    echo "Not executing ${COMMAND} lock ${LOCKDIR}" 1>&2',
                'fi',
                ])

        real_commands = []
        real_commands.append(
            ('${CMAKE_SOURCE_DIR}/'+cmake_consts.scripts_dir+'/custom-command-lock-wait',
             [custom_command_lock]))
        for c in commands:
            if len(c[1]) > 0:
                esc_command = ' '.join([c[0]] + c[1])
            else:
                esc_command = c[0]
                pass

            if esc_command.find(';') >= 0:
                raise Error("Custom command contains ';'. Don't use it - CMake will do unutterable things with it.")

            esc_command = esc_command.replace('"', r'\\\"')
            esc_command = esc_command.replace('(', r'\\\(')
            esc_command = esc_command.replace(')', r'\\\)')
            esc_command = esc_command.replace("'", r"\\\\'")
            esc_command = esc_command.replace('<', r'\\<')
            esc_command = esc_command.replace('>', r'\\>')

            real_commands.append(('echo', [esc_command, 
                                           '|',
                                           '${CMAKE_SOURCE_DIR}/'+cmake_consts.scripts_dir+'/custom-command-lock-exec-if-locked',
                                           custom_command_lock]))
            pass
        real_commands.append(
            ('${CMAKE_SOURCE_DIR}/'+cmake_consts.scripts_dir+'/custom-command-unlock-if-locked',
             [custom_command_lock]))

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
