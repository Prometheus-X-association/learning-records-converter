from decimal import Decimal
from json import JSONEncoder
from typing import Any


class CustomJSONEncoder(JSONEncoder):
    """A custom JSON encoder that handles Decimal objects."""

    def default(self, o: Any):
        """Convert the object to a JSON serializable format.

        :param o: The object to be serialized
        :return: A JSON serializable representation of the object
        """
        if isinstance(o, Decimal):
            return int(o) if o == o.to_integral_value() else float(o)
        return super().default(o)
