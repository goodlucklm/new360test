import unittest
import equation_converter as ec


class TestEquationConverter(unittest.TestCase):
    def test_is_equation_legal(self):
        self.assertEqual(ec.is_equation_legal('x = y'), True)
        self.assertEqual(ec.is_equation_legal('x == y'), False)
        self.assertEqual(ec.is_equation_legal('x^2 + 4y'), False)
        self.assertEqual(ec.is_equation_legal('4x^5+(3y-8.9z) = (6m - 7.5z^5)'), True)
        self.assertEqual(ec.is_equation_legal('4x^5+(3y-8.9z)) = (6m - 7.5z^5)'), False)

    def test_parse_summands(self):
        summands = ec.parse_summands('2x+3y+4z-6m')
        results = []
        for s in summands:
            results.append(s.get_original_form())
        self.assertEqual(results, ['+2x', '+3y', '+4z', '-6m'])
        summands = ec.parse_summands('x^2 + 3.5xy^76 +y - 4.78xyz^100-7.88m^78')
        results = []
        for s in summands:
            results.append(s.get_original_form())
        self.assertEqual(results, ['+x^2', '+ 3.5xy^76', '+y', '- 4.78xyz^100', '-7.88m^78'])

    def test_flat_parentheses_no_starting_sign(self):
        s = '(5.6x-(7.5y-4.6z^7))'
        s1 = ec.remove_parentheses(s)
        self.assertEqual(s1, '(5.6x-7.5y+4.6z^7)')
        s2 = ec.remove_parentheses(s1)
        self.assertEqual(s2, '5.6x-7.5y+4.6z^7')

    def test_is_operand_identical(self):
        self.assertEqual(ec.is_operand_identical('xy^76', 'xyz^100'), False)

    def test_parse_one_equation_normal(self):
        eq = "x^2 + 3.5xy + y = y^2 - xy + y"
        expect = 'x^2+4.5xy-y^2=0'
        self.assertEqual(ec.parse_one_equation(eq), expect)

    def test_parse_one_equation_simple(self):
        eq = "x = 1"
        expect = 'x-1=0'
        self.assertEqual(ec.parse_one_equation(eq), expect)

    def test_parse_one_equation_with_parentheses(self):
        eq = 'x - (y^2 - x) = 0'
        expect = '2x-y^2=0'
        self.assertEqual(ec.parse_one_equation(eq), expect)

    def test_parse_on_equation_with_nested_parentheses(self):
        eq = "x-(0-(0-x))=0"
        expect = '0=0'
        self.assertEqual(ec.parse_one_equation(eq), expect)

if __name__ == '__main__':
    unittest.main()
