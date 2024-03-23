import unittest
from calculator import Calculator


class TestCalculatorMethods(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_initial_expression_is_empty(self):
        self.assertEqual("", self.calculator.expression)

    def test_digit(self):
        self.calculator.digit(1)
        self.assertEqual("1", self.calculator.expression)

    def test_plus(self):
        self.calculator.plus()
        self.assertEqual("+", self.calculator.expression)

    def test_minus(self):
        self.calculator.minus()
        self.assertEqual("-", self.calculator.expression)
    
    def test_multiply(self):
        self.calculator.multiply()
        self.assertEqual("*", self.calculator.expression)
    
    def test_divide(self):
        self.calculator.divide()
        self.assertEqual("/", self.calculator.expression)


class TestCalculatorUsage(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_expression_insertion(self):
        self.calculator.digit(1)
        self.calculator.plus()
        self.calculator.digit(2)
        self.assertEqual("1+2", self.calculator.expression)

    def test_compute_result(self):
        self.calculator.expression = "1+2"
        self.assertEqual(3, self.calculator.compute_result())

    def test_compute_result_with_invalid_expression(self):
        self.calculator.expression = "1+"
        with self.assertRaises(ValueError) as context:
            self.calculator.compute_result()
        self.assertEqual("Invalid expression: 1+", str(context.exception))


class TestComplexExpressions(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_expression_with_parentheses(self):
        self.calculator.open_parenthesis()
        self.calculator.digit(1)
        self.calculator.plus()
        self.calculator.digit(2)
        self.calculator.close_parenthesis()
        self.calculator.multiply()
        self.calculator.digit(3)
        self.assertEqual("(1+2)*3", self.calculator.expression)
        self.assertEqual(9, self.calculator.compute_result())

    def test_expression_with_sqrt(self):
        self.calculator.digit(1)
        self.calculator.plus()
        self.calculator.square_root()
        self.calculator.open_parenthesis()
        self.calculator.digit(1)
        self.calculator.digit(1)
        self.calculator.minus()
        self.calculator.digit(2)
        self.calculator.close_parenthesis()
        self.assertEqual("1+sqrt(11-2)", self.calculator.expression)
        self.assertEqual(4, self.calculator.compute_result())

    def test_expression_with_pow(self):
        self.calculator.open_parenthesis()
        self.calculator.digit(1)
        self.calculator.plus()
        self.calculator.digit(1)
        self.calculator.close_parenthesis()
        self.calculator.power()
        self.calculator.digit(3)
        self.assertEqual("(1+1)**3", self.calculator.expression)
        self.assertEqual(8, self.calculator.compute_result())
