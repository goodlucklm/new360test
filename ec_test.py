import unittest
import equation_converter as ec


class TestEquationConverter(unittest.TestCase):
    def test_is_equation_legal(self):
        self.assertEqual(ec.is_equation_legal('x = y'), True)
        self.assertEqual(ec.is_equation_legal('x == y'), False)
        self.assertEqual(ec.is_equation_legal('x^2 + 4y'), False)

    def test_is_rammand_legal(self):
        self.assertEqual(ec.is_summand_legal('x^2'), True)
        self.assertEqual(ec.is_summand_legal('3.5xy'), True)
        self.assertEqual(ec.is_summand_legal('+y'), True)
        self.assertEqual(ec.is_summand_legal('-4.78xyz^100'), True)
        self.assertEqual(ec.is_summand_legal('0^9'), False)
        self.assertEqual(ec.is_summand_legal('x&9'), False)
        self.assertEqual(ec.is_summand_legal('7'), True)
        self.assertEqual(ec.is_summand_legal('^8'), False)
        self.assertEqual(ec.is_summand_legal('4.5x^2y^3z^4'), False)


if __name__ == '__main__':
    unittest.main()
