'''
1. without arguments: interactive; -f filename, read from a file
2. legal equation contains only one '='
3. legal summand has [+-],[float/int],[char],[^int]
'''
import argparse
import sys
from summand_class import Summand


def is_input_readable(f):
    try:
        open(f, 'r')
    except IOError as ex:
        print ex
        sys.exit(-1)


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


def flat_parentheses(super_summand):
    '''
    remove one pair of parentheses by changing +/- accordingly
    does not support (x+y)^2
    :param super_summand: summands from one side of t'='
    :return: string with the most inner pair removed and sign changed
    '''
    # find the first closing parenthese
    closing_parenthese_index = 0
    closing_parenthese_index = super_summand.find(')', closing_parenthese_index)
    print 'closing parenthese is at', closing_parenthese_index

    # find the open parenthese that paired with the first closing parenthese
    i = closing_parenthese_index
    while i >= 0 and super_summand[i] != '(':
            i -= 1
    open_parenthese_index = i
    print 'open parenthese is at', i

    # find the sign before open parenthese
    while i >= 0 and super_summand[i] not in ['+', '-']:
        i -= 1
    print i, super_summand[i]
    if i < 0 and super_summand[i] not in ['+', '-']:
        sign = '+'
        inner_summand = super_summand[:closing_parenthese_index+1]
        sign_index = 0
    else:
        sign = super_summand[i]
        inner_summand = super_summand[i:closing_parenthese_index+1]
        sign_index = i
    print 'sign is ', sign
    print 'inner summand is', inner_summand

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
    lsummands = parse_summands(left)


if __name__ == '__main__':
    description = \
    """
    To enter interactive mode, invoke with no arguments
    Restrictions:
    1. do not support (x + y)^2
    2. do not support (+x - y) or (-x - z), the first summand in parentheses can not contain a sign
    """
    parser = argparse.ArgumentParser(description='To enter interactive mode, invoke with no arguments',
                                     prog='equation_converter')
    parser.add_argument('-f', '--file', type=str, dest='filename')
    args = parser.parse_args()

    if args.filename:
        is_input_readable(args.filename)
