from inspect import cleandoc
import json

class SsnJsonGetIndexValue:
    """
    A node that takes a JSON-formatted string representing an array and an integer index,
    then outputs the value at that index in the array.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node: 
          - "json_string": the JSON array as a string.
          - "index": the zero-based index to retrieve from the array.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple. Here, it is a single STRING (the JSON-formatted value).
    RETURN_NAMES (`tuple`):
        The name of the output ("value").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("JSON").
    execute(json_string, index) -> tuple:
        Parses the JSON string as an array and returns the element at the given index
        as a JSON-formatted string. If parsing fails, the input is not an array, or the
        index is out of bounds, returns an empty string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "[]"
                    }
                ),
                "index": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 2147483647,
                        "step": 1,
                        "display": "number"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "JSON"

    def __init__(self):
        pass

    def execute(self, json_string, index):
        try:
            data = json.loads(json_string)
            if isinstance(data, list) and 0 <= index < len(data):
                value = data[index]
                return (json.dumps(value),)
            else:
                return ("",)
        except (json.JSONDecodeError, TypeError):
            return ("",)
