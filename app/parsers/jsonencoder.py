import json
from decimal import Decimal


class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that handles Decimal objects.
    """

    def default(self, obj):
        """
        Convert the object to a JSON serializable format.

        :param obj: The object to be serialized
        :return: A JSON serializable representation of the object
        """
        if isinstance(obj, Decimal):
            return int(obj) if obj == obj.to_integral_value() else float(obj)
        return super().default(obj)
