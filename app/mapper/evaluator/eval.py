from collections.abc import Callable
from typing import Any

from app.infrastructure.logging.contract import LoggerContract

from .contract import ExpressionEvaluatorContract
from .exceptions import ExpressionEvaluationError


class EvalExpressionEvaluator(ExpressionEvaluatorContract):
    """
    Simple implementation of expression evaluation using eval().
    """

    def __init__(self, logger: LoggerContract):
        """
        Initialize the eval() expression evaluator.

        :param logger: LoggerContract implementation for logging
        """
        self.logger = logger

        self.registered_functions: dict[str, Callable] = {
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "isinstance": isinstance,
            "all": all,
            "any": any,
            "min": min,
            "max": max,
            "sum": sum,
            "sorted": sorted,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "format": format,
            "split": str.split,
            "join": str.join,
            "strip": str.strip,
            "replace": str.replace,
            "round": round,
            "abs": abs,
            "pow": pow,
            "None": None,
            "True": True,
            "False": False,
        }

    def register_function(self, name: str, func: Callable) -> None:
        """
        Register a function to be available during expression evaluation.

        :param name: The name under which the function will be available
        :param func: The function implementation
        """
        if not name.isidentifier():
            msg = "Invalid function name"
            self.logger.error(msg, {"name": name})
            raise ValueError(msg)

        if name in self.registered_functions:
            msg = "Already registered function"
            self.logger.error(msg, {"name": name})
            raise ValueError(msg)

        self.registered_functions[name] = func

    def eval_expression(self, expression: str) -> Any:
        """
        Evaluate a simple expression using eval().

        :param expression: The expression to evaluate
        :return: The result of the evaluation
        :raises ExpressionEvaluationError: If evaluation fails
        """
        if "__" in expression:
            msg = "Potentially unsafe expression"
            self.logger.error(msg, {"expression": expression})
            raise ExpressionEvaluationError(msg)

        try:
            globals_dict = self.registered_functions.copy()
            globals_dict["__builtins__"] = {}

            return eval(expression, globals_dict, {})  # noqa: S307
        except Exception as e:
            msg = "Expression evaluation failed"
            self.logger.exception(msg, e, {"expression": expression})
            raise ExpressionEvaluationError(msg) from e

    def eval_lambda(self, lambda_expr: str, *args) -> Any:
        """
        Evaluate a lambda expression with the given arguments.

        :param lambda_expr: The lambda expression as a string (e.g., "lambda x, y: x + y")
        :param args: Arguments to pass to the lambda function
        :return: The result of the lambda evaluation
        :raises ExpressionEvaluationError: If evaluation fails
        """
        # Compile and evaluate the lambda
        lambda_func = self.eval_expression(expression=lambda_expr)
        if not callable(lambda_func):
            msg = "Expression did not evaluate to a callable"
            self.logger.error(msg, {"expression": lambda_expr})
            raise ExpressionEvaluationError(msg)

        try:
            return lambda_func(*args)
        except Exception as e:
            msg = "Lambda evaluation failed"
            self.logger.exception(msg, e, {"expression": lambda_expr})
            raise ExpressionEvaluationError(msg) from e
