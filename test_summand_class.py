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


if __name__ == '__main__':
    unittest.main()