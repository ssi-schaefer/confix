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

from libconfix.plugins.automake import makefile

from libconfix.core.utils.error import Error

import unittest

class MakefileUtilsSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(RuleTest('test_ok1'))
        self.addTest(RuleTest('test_ok2'))
        self.addTest(RuleTest('test_error'))
        self.addTest(RuleTest('test_command_as_list'))
        self.addTest(IncludeTest('test'))
        pass
    pass

class RuleTest(unittest.TestCase):
    def test_ok1(self):
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

        self.failIf(makefile.find_list(name='list1', elements=elements).values() != \
                    ['list1value1', 'list1value2', 'list1value3'])
        self.failIf(makefile.find_list(name='list2', elements=elements).values() != \
                    ['list2value1'])

        rule = makefile.find_rule(targets=['target'], elements=elements)
        self.failIf(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.failIf(rule.commands() != ['command1', 'command2'])

        rule = makefile.find_rule(targets=['target1', 'target2'], elements=elements)
        self.failIf(rule.prerequisites() != [])
        self.failIf(rule.commands() != ['command3', 'command4'])

        rule = makefile.find_rule(targets=['target3', 'target4'], elements=elements)
        self.failIf(rule.prerequisites() != [])
        self.failIf(rule.commands() != [])

        rule = makefile.find_rule(targets=['target5', 'target6'], elements=elements)
        self.failIf(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.failIf(rule.commands() != [])
        pass

    def test_ok2(self):
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
        self.failIf(rule.prerequisites() != ['prereq1', 'prereq2'])
        self.failIf(rule.commands() != ['command1', 'command2'])

        list = makefile.find_list(name='list1', elements=elements)
        self.failIf(list.values() != ['value1', 'value2'])

        list = makefile.find_list(name='list2', elements=elements)
        self.failIf(list.values() != ['value3', 'value4', 'value5'])

        list = makefile.find_list(name='list3', elements=elements)
        self.failIf(list.values() != [])

        rule = makefile.find_rule(targets=['target2', 'target3'], elements=elements)
        self.failIf(rule.prerequisites() != ['prereq3', 'prereq4'])
        self.failIf(rule.commands() != [])

        rule = makefile.find_rule(targets=['target4', 'target5'], elements=elements)
        self.failIf(rule.prerequisites() != ['prereq3', 'prereq4'])
        self.failIf(rule.commands() != ['command3'])
        pass
        
    def test_error(self):
        self.failUnlessRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx'])
        self.failUnlessRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx yyy zzz'])
        self.failUnlessRaises(Error,
                              makefile.parse_makefile,
                              lines=['xxx: yyy',
                                     'zzz'])
        pass

    def test_command_as_list(self):
        rule = makefile.Rule(targets=['target'],
                             commands=[['cmd1', 'cmd2'], ['cmd3']])
        elements = makefile.parse_makefile(lines=rule.lines())
        found_rule = makefile.find_rule(targets=['target'], elements=elements)
        self.failIf(found_rule is None)
        self.failUnlessEqual(found_rule.commands(), ['cmd1 cmd2', 'cmd3'])
        pass

    pass

class IncludeTest(unittest.TestCase):
    def test(self):
        lines = []
        for element in [makefile.Include('blah')]:
            lines.extend(element.lines())
            pass

        elements = makefile.parse_makefile(lines=lines)
        self.failUnless(isinstance(elements[0], makefile.Include))
        self.failUnlessEqual(elements[0].file(), 'blah')
        pass
    pass


if __name__ == '__main__':
    unittest.TextTestRunner().run(MakefileUtilsSuite())
    pass
