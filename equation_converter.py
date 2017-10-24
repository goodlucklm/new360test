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


def is_equation_legal(eq):
    '''
    legal equation contains only one '='
    :param eq: equation presented in string
    :return: True/False
    '''
    if type(eq) is not str:
        return None
    return eq.count('=') == 1


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
    parser = argparse.ArgumentParser(description='To enter interactive mode, invoke with no arguments',
                                     prog='equation_converter')
    parser.add_argument('-f', '--file', type=str, dest='filename')
    args = parser.parse_args()

    if args.filename:
        is_input_readable(args.filename)
