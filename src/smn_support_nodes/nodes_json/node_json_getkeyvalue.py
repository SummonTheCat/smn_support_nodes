from inspect import cleandoc
import json

class SsnJSONGetKeyValue:
    """
    A node that takes a JSON-formatted string (via a pin) and a key, then outputs the value associated with that key.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node. In this case, a JSON string (single-line pin) and a key string.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple. Here, it is a single STRING.
    RETURN_NAMES (`tuple`):
        Optional: The name of the output ("value").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("JSON").
    execute(json_string, key) -> tuple:
        Parses the JSON from the pin and returns the value for the given key as a JSON-formatted string.
        If the key is not found or parsing fails, returns an empty string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": "{}"
                    }
                ),
                "key": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": ""
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

    def execute(self, json_string, key):
        try:
            data = json.loads(json_string)
            if key in data:
                value = data[key]
                print(f"Key '{key}' found with value: {value}")
                return (json.dumps(value),)
            else:
                print(f"Key '{key}' not found in the JSON data.")
                return ("",)
        except (json.JSONDecodeError, TypeError):
            print("Invalid JSON string provided.")
            return ("",)
