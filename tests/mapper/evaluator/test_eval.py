from unittest.mock import Mock

import pytest

from app.mapper.evaluator.eval import EvalExpressionEvaluator
from app.mapper.evaluator.exceptions import ExpressionEvaluationError


class TestEvalExpressionEvaluator:
    """Test suite for TestEvalExpressionEvaluator class."""

    @pytest.fixture
    def expression_evaluator(self, mock_logger):
        """Create an instance of EvalExpressionEvaluator for testing."""
        return EvalExpressionEvaluator(logger=mock_logger)

    def test_default_registered_functions(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test that some default functions are registered correctly."""
        default_functions = [
            "str",
            "dict",
            "isinstance",
            "len",
        ]
        registered_functions = expression_evaluator.registered_functions
        for func_name in default_functions:
            assert func_name in registered_functions

    def test_register_function_valid(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test registering a valid custom function."""

        def custom_func(x, y):
            return x + y

        expression_evaluator.register_function("custom_func", custom_func)

        assert "custom_func" in expression_evaluator.registered_functions
        assert expression_evaluator.registered_functions["custom_func"] == custom_func

    def test_register_function_override(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test that registering an existing function raises an error."""

        def new_isinstance():
            return 42

        with pytest.raises(ValueError, match="Already registered function"):
            expression_evaluator.register_function("isinstance", new_isinstance)

        mock_logger.error.assert_called_once()

    def test_register_function_invalid_name(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test registering a function with an invalid name raises an error."""

        def custom_func(x, y):
            return x + y

        with pytest.raises(ValueError, match="Invalid function name"):
            expression_evaluator.register_function("invalid-name", custom_func)

        mock_logger.error.assert_called_once()

    def test_eval_expression_basic(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test basic expression evaluation."""
        result = expression_evaluator.eval_expression("2 + 3")
        assert result == 5

    def test_eval_expression_function_call(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test expression evaluation with function calls."""
        result = expression_evaluator.eval_expression("len([1, 2, 3])")
        assert result == 3

    def test_eval_expression_no_builtins(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test that built-in functions are not available."""
        with pytest.raises(ExpressionEvaluationError):
            expression_evaluator.eval_expression("__import__('os').system('ls')")

        mock_logger.error.assert_called_once()

    def test_eval_expression_malicious(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test that malicious dictionary execution is blocked."""
        with pytest.raises(ExpressionEvaluationError):
            expression_evaluator.eval_expression("{'a': (lambda: 42).__call__()}")

        mock_logger.error.assert_called_once()

    def test_eval_lambda_simple(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test simple lambda expression evaluation."""
        result = expression_evaluator.eval_lambda("lambda x: x * 2", 5)
        assert result == 10

    def test_eval_lambda_multiple_args(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test lambda expression with multiple arguments."""
        result = expression_evaluator.eval_lambda("lambda x, y: x + y", 3, 4)
        assert result == 7

    def test_eval_lambda_with_registered_func(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test lambda expression using a registered function."""

        def multiply(x, y):
            return x * y

        expression_evaluator.register_function("multiply", multiply)

        result = expression_evaluator.eval_lambda("lambda x, y: multiply(x, y)", 3, 4)
        assert result == 12

    def test_eval_lambda_invalid_expression(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test lambda expression evaluation with an invalid expression."""
        with pytest.raises(ExpressionEvaluationError):
            expression_evaluator.eval_lambda("not a valid lambda")

        mock_logger.exception.assert_called_once()

    def test_eval_lambda_non_callable(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test lambda expression that does not evaluate to a callable."""
        with pytest.raises(
            ExpressionEvaluationError,
            match="Expression did not evaluate to a callable",
        ):
            expression_evaluator.eval_lambda("'not a function'", 1)

        mock_logger.error.assert_called_once()

    def test_eval_lambda_runtime_error(
        self,
        expression_evaluator: EvalExpressionEvaluator,
        mock_logger: Mock,
    ) -> None:
        """Test lambda expression that raises a runtime error during execution."""
        with pytest.raises(ExpressionEvaluationError):
            expression_evaluator.eval_lambda("lambda x: 1 / 0", 10)

        mock_logger.exception.assert_called_once()

    def test_register_function_edge_cases(
        self,
        expression_evaluator: EvalExpressionEvaluator,
    ) -> None:
        """Test registering functions with various argument signatures."""

        # Test functions with different numbers of arguments
        def no_args():
            return 42

        def var_args(*args):
            return sum(args)

        def keyword_args(**kwargs):
            return len(kwargs)

        expression_evaluator.register_function("no_args", no_args)
        expression_evaluator.register_function("var_args", var_args)
        expression_evaluator.register_function("keyword_args", keyword_args)

        assert expression_evaluator.eval_lambda("lambda: no_args()") == 42
        assert expression_evaluator.eval_lambda("lambda: var_args(1, 2, 3)") == 6
        assert expression_evaluator.eval_lambda("lambda: keyword_args(a=1, b=2)") == 2
