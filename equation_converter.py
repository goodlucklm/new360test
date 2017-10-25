'''
1. without arguments: interactive; -f filename, read from a file
2. legal equation contains only one '='
3. legal summand has [+-],[float/int],[char],[^int]
'''
import argparse
import sys

import re

from summand_class import Summand


def ckeck_input_file(f):
    try:
        open(f, 'r')
    except IOError as ex:
        print ex.message
        sys.exit(-1)


def create_output_file(f):
    try:
        return open(f+'.out', 'w')
    except IOError as ex:
        print ex.message
        sys.exit(-2)


def are_parenthese_matched(eq):
    '''
    check if parentheses are in pair, ( is before )
    :param eq: legal string
    :return: True/False
    '''
    count = 0
    for c in eq:
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
        if count < 0:
            return False
    return count == 0


def is_equation_legal(eq):
    '''
    legal equation contains only one '=', () must be in pair
    :param eq: equation presented in string
    :return: True/False
    '''
    if type(eq) is not str:
        return None
    if eq.count('=') != 1:
        return False

    i = eq.find('=')
    left_side = eq[0:i]
    right_side = eq[i:]
    if not are_parenthese_matched(left_side):
        return False
    if not are_parenthese_matched(right_side):
        return False
    return True


def parse_summands(s):
    '''
    give a list of summands in the format of string
    return the summands in a list of Summands
    :param s: the string containing a number of summands
    :return: a list of summands
    '''

    # find the locations of operators
    operator_indexes = []
    for i in range(len(s)):
        if s[i] in ['+', '-']:
            operator_indexes.append(i)

    # slice the string
    summands = []
    last_index = 0
    for i in operator_indexes:
        summand = s[last_index:i].strip()
        last_index = i
        if not summand.startswith('+') and not summand.startswith('-'):
            summand = '+'+summand
        summands.append(Summand(summand))
    summands.append(Summand(s[last_index:]))
    return summands


def remove_parentheses(super_summand):
    '''
    remove one pair of parentheses by changing +/- accordingly
    does not support (x+y)^2
    :param super_summand: summands from one side of t'='
    :return: string with the most inner pair removed and sign changed
    '''
    # find the first closing parenthese
    closing_parenthese_index = 0
    closing_parenthese_index = super_summand.find(')', closing_parenthese_index)

    # find the open parenthese that paired with the first closing parenthese
    i = closing_parenthese_index
    while i >= 0 and super_summand[i] != '(':
            i -= 1
    open_parenthese_index = i

    # find the sign before open parenthese
    while i >= 0 and super_summand[i] not in ['+', '-']:
        i -= 1
    if i < 0 and super_summand[i] not in ['+', '-']:
        sign = '+'
        inner_summand = super_summand[:closing_parenthese_index+1]
        sign_index = 0
    else:
        sign = super_summand[i]
        inner_summand = super_summand[i:closing_parenthese_index+1]
        sign_index = i

    # flip the signs of each summand base on the sign before open parenthese
    if sign == '-':
        starting = inner_summand.find('(')
        for i in range(starting, len(inner_summand)-1): # the last charactor is not going to be +/-
            if inner_summand[i] == '+':
                inner_summand = inner_summand[:i] + '-' + inner_summand[i+1:]
            elif inner_summand[i] == '-':
                inner_summand = inner_summand[:i] + '+' + inner_summand[i+1:]

    # remove parentheses
    inner_summand = inner_summand.replace('(', '', 1)
    inner_summand = inner_summand.replace(')', '', 1)

    return super_summand[:sign_index] + inner_summand + super_summand[closing_parenthese_index+1:]


def is_operand_identical(op1, op2):
    '''
    check if two operands are identical
    only consider variables in the same order to be identical
    same variable, same power, different order considered identical
    :param op1: string
    :param op2: string
    :return: True/False
    '''
    return op1 == op2


def parse_one_equation(eq):
    '''
    transform 1 equation into canonical form
    :param eq: legal string
    :return: canonical form equation
    '''
    if not is_equation_legal(eq):
        return None

    # break eq into left summands and right summands
    left, right = eq.split('=')

    # construct all summands
    while '(' in left:
        left = remove_parentheses(left)
    while '(' in right:
        right = remove_parentheses(right)
    all_summands = parse_summands(left)
    rsummands = parse_summands(right)
    for summand in rsummands:
        summand.flip_sign()
        all_summands.append(summand)

    # do calculations
    final_summands = ''
    while len(all_summands) > 0:
        s = ''
        coeff = all_summands[0].get_signed_coefficient()
        operand = all_summands[0].get_operand()
        j = 1
        while j < len(all_summands):
            if is_operand_identical(operand, all_summands[j].get_operand()):
                coeff += all_summands[j].get_signed_coefficient()
                all_summands.pop(j)
            else:
                j += 1
        all_summands.pop(0)

        # build the final summand
        if coeff == 0.0:
            continue

        # format coefficient
        if coeff % 1.0 == 0:
            coeff_str = str(int(coeff))
        else:
            coeff_str = str(coeff)

        if operand == '':
            s += coeff_str
        else:
            if coeff == 1.0 and operand != '':
                s = operand
            elif coeff == -1.0 and operand != '':
                s = '-'+operand
            else:
                s = coeff_str+operand
        if coeff > 0:
            s = '+'+s
        final_summands += s
    if final_summands == '':
        final_summands += '0'
    if final_summands.startswith('+'):
        final_summands = final_summands[1:]
    return final_summands + '=0'


if __name__ == '__main__':
    description = \
    """\
To enter interactive mode, invoke with no arguments
    """
    restriction = \
    """
Restrictions:
1. does not support (x + y)^2 
2. does not support (+x - y) or (-x - z), the first summand in parentheses can not contain a sign
3. only considering variables in the same order to be the same operand e.g.: xyz^3 and yxz^3 are not considered equal (left room to fix this, can do it onsite)
4. output file will be created in the current working directory. If cwd is not writable, exception will be raised
    """
    welcome = \
    """
Wellcome to equation converter 1.0 by Ming Lu Oct 2017
    """
    parser = argparse.ArgumentParser(description=description+restriction, prog='equation_converter')
    parser.add_argument('-f', '--file', type=str, dest='filename')
    args = parser.parse_args()

    if args.filename:
        ckeck_input_file(args.filename)
        output = create_output_file(args.filename)

        input_equations = open(args.filename, 'r').readlines()
        results = []
        for equation in input_equations:
            if equation.strip() != '':
                result = parse_one_equation(equation.strip())
                results.append(result)

        s = ''
        for result in results:
            s += result + '\n'
        output.write(s[:-1])
        output.close()
    else:
        print welcome, restriction
        while True:
            print 'Please input an equation:'
            line = sys.stdin.readline()
            if line.strip() == '':
                continue
            if not is_equation_legal(line):
                print 'Illegal equation.'
                continue
            try:
                result = parse_one_equation(line)
            except ValueError as ex:
                print ex.message
                continue
            print result

