import re


class Summand:
    def __init__(self, s):
        '''
        construct a summand from s
        :param s: the string contains a summand
        '''
        self.original_form = s.strip()
        pattern = '^([+-])?( *)(\d+|\d+\.\d+)?([a-zA-z]+(\^\d*)?)?$'
        m = re.match(pattern, self.original_form)
        if not m:
            raise ValueError('Illegal summand: '+self.original_form)
        self.sign = m.groups()[0]
        self.coefficient = 1.0 if not m.groups()[2] else float(m.groups()[2])
        self.operand = m.groups()[3]

    def get_original_form(self):
        return self.original_form

    def get_sign(self):
        return self.sign

    def flip_self(self):
        if self.sign is '+':
            self.sign = '-'
        elif self.sign is '-':
            self.sign = '+'
        else:
            # should never reach here
            pass

    def get_coefficient(self):
        return self.coefficient

    def get_operand(self):
        return self.operand
