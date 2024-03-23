import os ; os.environ["KIVY_NO_ARGS"] = "1" # hack for making tests loadable in VS Code
import unittest
from calculator.ui.gui import CalculatorApp


class CalculatorGUITestCase(unittest.TestCase):
    def setUp(self):
        self.app = CalculatorApp()
        self.app._run_prepare()

    def press_button(self, button_text):
        self.app.find_button_by(button_text).trigger_action()

    def assert_display(self, value):
        self.assertEqual(self.app.display.text, value)   

    def tearDown(self):
        self.app.stop()
    

class TestExpressions(CalculatorGUITestCase):
    def test_integer_expression(self):
        self.press_button("1")
        self.press_button("+")
        self.press_button("2")
        self.assert_display("1+2")
        self.press_button("=")
        self.assert_display("3")

    def test_float_expression(self):
        self.press_button("1")
        self.press_button(".")
        self.press_button("2")
        self.press_button("+")
        self.press_button("2")
        self.assert_display("1.2+2")
        self.press_button("=")
        self.assert_display("3.2")

    def test_expression_with_parentheses(self):
        self.press_button("(")
        self.press_button("1")
        self.press_button("+")
        self.press_button("2")
        self.press_button(")")
        self.press_button("*")
        self.press_button("3")
        self.assert_display("(1+2)*3")
        self.press_button("=")
        self.assert_display("9")

    def test_expression_wit_sqrt(self):
        self.press_button("sqrt")
        self.press_button("4")
        self.press_button(")")
        self.assert_display("sqrt(4)")
        self.press_button("=")
        self.assert_display("2.0")

    def test_expression_with_pow(self):
        self.press_button("2")
        self.press_button("**")
        self.press_button("3")
        self.assert_display("2**3")
        self.press_button("=")
        self.assert_display("8")
    