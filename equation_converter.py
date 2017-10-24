'''
1. without arguments: interactive; -f filename, read from a file
2. legal equation contains only one '='
3. legal summand has [+-],[float/int],[char],[^int]
'''
import argparse
import sys
import re


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


def is_summand_legal(summand):
    '''
    illegal: 9^2, ^8, x^2y^3
    legal: 2x, x^3, 3.67yz^7
    :param summand: legal string
    :return: True/False
    '''
    pattern = '^[+-]?(\d+|\d+\.\d+)?([a-zA-z]+(\^\d*)?)?$'
    if re.match(pattern, summand):
        return True
    else:
        return False


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
    lsummands = left.strip().split



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='To enter interactive mode, invoke with no arguments',
                                     prog='equation_converter')
    parser.add_argument('-f', '--file', type=str, dest='filename')
    args = parser.parse_args()

    if args.filename:
        is_input_readable(args.filename)
