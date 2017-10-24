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
            print results
        self.assertEqual(results, ['+2x', '+3y', '+4z', '-6m'])
        summands = ec.parse_summands('x^2 + 3.5xy^76 +y - 4.78xyz^100-7.88m^78')
        results = []
        for s in summands:
            results.append(s.get_original_form())
        self.assertEqual(results, ['+x^2', '+ 3.5xy^76', '+y', '- 4.78xyz^100', '-7.88m^78'])


if __name__ == '__main__':
    unittest.main()
