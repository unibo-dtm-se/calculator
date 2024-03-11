from typing import Any, Union, get_args


Number = Union[int, float]


class Calculator:

    def __init__(self):
        self.expression = ""

    def _ensure_is_digit(self, value: int | str) -> int:
        if isinstance(value, str):
            value = int(value)
        if value not in range(10):
            raise ValueError("Value must a digit in [0, 9]: " + str(value))
        return value

    def _append(self, value: Any):
        self.expression += str(value)
    
    def digit(self, value: int | str):
        value = self._ensure_is_digit(value)
        self._append(value)
    
    def plus(self):
        self._append("+")

    def minus(self):
        self._append("-")
    
    def multiply(self):
        self._append("*")
    
    def divide(self):
        self._append("/")

    def dot(self):
        self._append(".")

    def clear(self):
        self.expression = ""
    
    def compute_result(self) -> Number:
        try:
            result = eval(self.expression)
            if any(isinstance(result, type) for type in get_args(Number)):
                self.expression = str(result)
                return result
            else:
                raise ValueError("Result is not a number: " + str(result))
        except Exception as e:
            expression = self.expression
            self.expression = ""
            raise ValueError("Invalid expression: " + expression) from e
