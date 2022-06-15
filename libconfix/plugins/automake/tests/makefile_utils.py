# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2013 Joerg Faschingbauer

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

from libconfix.plugins.automake import makefile

from libconfix.core.utils.error import Error

import unittest

class MakefileUtilsTest(unittest.TestCase):
    def test__rules_ok1(self):
        lines = []
        for element in [makefile.Rule(targets=['target'],
                                      prerequisites=['prereq1', 'prereq2'],
                                      commands=['command1', 'command2']),
                        makefile.White(lines=['# some comment',
                                              '# even more comment']),
                        makefile.List(name='list1', values=['list1value1', 'list1value2', 'list1value3'], mitigate=True),
                        makefile.List(name='list2', values=['list2value1'], mitigate=True),
                        makefile.Rule(targets=['target1', 'target2'],
                                      prerequisites=[],
                                      commands=['command3', 'command4']),
                        makefile.Rule(targets=['target3', 'target4'],
                                      prerequisites=[],
                                      commands=[]),
                        makefile.Rule(targets=['target5', 'target6'],
                                      prerequisites=['prereq1', 'prereq2'],
                                      commands=[])]:
            lines.extend(element.lines())
            pass

        elements = makefile.parse_makefile(lines=lines)

        self.assertFalse(list(makefile.find_list(name='list1', elements=elements).values()) != \
                    ['list1value1', 'list1value2', 'list1value3'])
        self.assertFalse(list(makefile.find_list(name='list2', elements=elements).values()) != \
                    ['list2value1'])

        rule = makefile.find_rule(targets=['target'], elements=elements)
        self.assertFalse(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.assertFalse(rule.commands() != ['command1', 'command2'])

        rule = makefile.find_rule(targets=['target1', 'target2'], elements=elements)
        self.assertFalse(rule.prerequisites() != [])
        self.assertFalse(rule.commands() != ['command3', 'command4'])

        rule = makefile.find_rule(targets=['target3', 'target4'], elements=elements)
        self.assertFalse(rule.prerequisites() != [])
        self.assertFalse(rule.commands() != [])

        rule = makefile.find_rule(targets=['target5', 'target6'], elements=elements)
        self.assertFalse(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.assertFalse(rule.commands() != [])
        pass

    def test__rules_ok2(self):
        elements = makefile.parse_makefile(
            ['',
             'target1: prereq1 prereq2',
             '\tcommand1',
             '\tcommand2',
             '',
             '',
             'list1 = value1 value2',
             'list2 = value3 \\',
             '  value4 \\',
             '  value5',
             '',
             'target2 target3: \\',
             '  prereq3 \\',
             '  prereq4',
             '',
             'list3 =',
             'target4 target5: \\',
             '  prereq3 \\',
             '  prereq4',
             '\tcommand3',
             ])
        rule = makefile.find_rule(targets=['target1'], elements=elements)
        self.assertFalse(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.assertFalse(rule.commands() != ['command1', 'command2'])

        list = makefile.find_list(name='list1', elements=elements)
        self.assertFalse(list(list.values()) != ['value1', 'value2'])

        list = makefile.find_list(name='list2', elements=elements)
        self.assertFalse(list(list.values()) != ['value3', 'value4', 'value5'])

        list = makefile.find_list(name='list3', elements=elements)
        self.assertFalse(list(list.values()) != [])

        rule = makefile.find_rule(targets=['target2', 'target3'], elements=elements)
        self.assertFalse(rule.prerequisites() != ['prereq3', 'prereq4'])
        self.assertFalse(rule.commands() != [])

        rule = makefile.find_rule(targets=['target4', 'target5'], elements=elements)
        self.assertFalse(rule.prerequisites() != ['prereq3', 'prereq4'])
        self.assertFalse(rule.commands() != ['command3'])
        pass
        
    def test__rules_error(self):
        self.assertRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx'])
        self.assertRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx yyy zzz'])
        self.assertRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx: yyy',
                                     'zzz'])
        pass

    def test__rules_command_as_list(self):
        rule = makefile.Rule(targets=['target'],
                             commands=[['cmd1', 'cmd2'], ['cmd3']])
        elements = makefile.parse_makefile(lines=rule.lines())
        found_rule = makefile.find_rule(targets=['target'], elements=elements)
        self.assertFalse(found_rule is None)
        self.assertEqual(found_rule.commands(), ['cmd1 cmd2', 'cmd3'])
        pass

    def test__include(self):
        lines = []
        for element in [makefile.Include('blah')]:
            lines.extend(element.lines())
            pass

        elements = makefile.parse_makefile(lines=lines)
        self.assertTrue(isinstance(elements[0], makefile.Include))
        self.assertEqual(elements[0].file(), 'blah')
        pass
    pass

suite = unittest.defaultTestLoader.loadTestsFromTestCase(MakefileUtilsTest)

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    pass
