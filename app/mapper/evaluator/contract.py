from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from typing import Any


class ExpressionEvaluatorContract(ABC):
    """Abstract contract for expression evaluation.

    It defines the operations required for evaluating expressions and lambda functions.
    """

    @abstractmethod
    def register_function(self, name: str, func: Callable) -> None:
        """Register a function to be available during expression evaluation.

        :param name: The name under which the function will be available
        :param func: The function implementation
        """
        raise NotImplementedError

    def register_functions(self, functions: Mapping[str, Callable]) -> None:
        """Register multiple functions to be available during expression evaluation.

        :param functions: Mapping of function names and implementations
        """
        for name, func in functions.items():
            self.register_function(name, func)

    @abstractmethod
    def eval_expression(self, expression: str) -> Any:
        """Evaluate a simple expression in a secure environment.

        :param expression: The expression to evaluate
        :return: The result of the evaluation
        :raises ExpressionEvaluationError: If evaluation fails
        """
        raise NotImplementedError

    @abstractmethod
    def eval_lambda(self, lambda_expr: str, *args) -> Any:
        """Evaluate a lambda expression with the given arguments.

        :param lambda_expr: The lambda expression as a string (e.g., "lambda x, y: x + y")
        :param args: Arguments to pass to the lambda function
        :return: The result of the lambda evaluation
        :raises ExpressionEvaluationError: If evaluation fails
        """
        raise NotImplementedError
