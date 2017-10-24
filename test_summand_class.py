import unittest
import summand_class


class TestEquationConverter(unittest.TestCase):
    def test_normal(self):
        summand = summand_class.Summand('+3.76xyz^3')
        self.assertEqual(summand.get_sign(), '+')
        summand.flip_self()
        self.assertEqual(summand.get_sign(), '-')
        self.assertEqual(summand.get_coefficient(), 3.76)
        self.assertEqual(summand.get_operand(), 'xyz^3')
        self.assertEqual(summand.get_original_form(), '+3.76xyz^3')

    def test_no_coefficient(self):
        summand = summand_class.Summand('-   xy^7')
        self.assertEqual(summand.get_sign(), '-')
        summand.flip_self()
        self.assertEqual(summand.get_sign(), '+')
        self.assertEqual(summand.get_coefficient(), 1.0)
        self.assertEqual(summand.get_operand(), 'xy^7')
        self.assertEqual(summand.get_original_form(), '-   xy^7')

    def test_constant(self):
        summand = summand_class.Summand('-6.78')
        self.assertEqual(summand.get_sign(), '-')
        summand.flip_self()
        self.assertEqual(summand.get_sign(), '+')
        self.assertEqual(summand.get_coefficient(), 6.78)
        self.assertEqual(summand.get_operand(), '')
        self.assertEqual(summand.get_original_form(), '-6.78')

    def test_no_power(self):
        summand = summand_class.Summand('-6.78xyz')
        self.assertEqual(summand.get_sign(), '-')
        summand.flip_self()
        self.assertEqual(summand.get_sign(), '+')
        self.assertEqual(summand.get_coefficient(), 6.78)
        self.assertEqual(summand.get_operand(), 'xyz')
        self.assertEqual(summand.get_original_form(), '-6.78xyz')

    def test_exception(self):
        try:
            summand = summand_class.Summand('+4.5x^2y^3z^4')
        except ValueError as ex:
            self.assertEqual(ex.message, 'Illegal summand: +4.5x^2y^3z^4')


if __name__ == '__main__':
    unittest.main()