from inspect import cleandoc
import json

class SsnJsonValueAs:
    """
    A node that takes a JSON-formatted value as a string and outputs that value
    cast to BOOL, INT, FLOAT, and STRING (without quotes).

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input field for this node: a single-line JSON value string.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The types of the output tuple: (BOOL, INT, FLOAT, STRING).
    RETURN_NAMES (`tuple`):
        The names of each output ("as_bool", "as_int", "as_float", "as_string").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("JSON").
    execute(json_value) -> tuple:
        Parses the JSON value and returns a tuple:
          - BOOL: The boolean interpretation of the value.
          - INT: The integer interpretation (or 0 if not convertible).
          - FLOAT: The float interpretation (or 0.0 if not convertible).
          - STRING: The string interpretation without quotation marks.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_value": (
                    "STRING",
                    {
                        "multiline": False,
                        "default": ""
                    }
                )
            }
        }

    RETURN_TYPES = ("BOOL", "INT", "FLOAT", "STRING")
    RETURN_NAMES = ("as_bool", "as_int", "as_float", "as_string")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "JSON"

    def __init__(self):
        pass

    def execute(self, json_value):
        """
        Attempt to load the input string as a JSON value.
        Then provide sensible conversions for each requested type.
        """
        # Defaults
        bool_out = False
        int_out = 0
        float_out = 0.0
        str_out = ""

        try:
            parsed = json.loads(json_value)
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, treat the raw string as a plain string value
            raw = json_value
            # BOOL: true if raw is "true" (case-insensitive), or a nonempty string not equal to "false"
            bool_out = raw.strip().lower() in ("true",) or (raw.strip() not in ("", "false", "0"))
            # INT: try converting raw to int
            try:
                int_out = int(raw)
            except:
                int_out = 0
            # FLOAT: try converting raw to float
            try:
                float_out = float(raw)
            except:
                float_out = 0.0
            # STRING: raw itself (no surrounding quotes)
            str_out = raw
            return (bool_out, int_out, float_out, str_out)

        # If parsing succeeds, work with the Python object `parsed`.
        # BOOL output
        if isinstance(parsed, bool):
            bool_out = parsed
        elif isinstance(parsed, (int, float)):
            bool_out = bool(parsed)
        elif isinstance(parsed, str):
            # Nonempty string is True, except literal "false" or "0"
            lower = parsed.strip().lower()
            bool_out = (lower not in ("", "false", "0"))
        else:
            # For objects/arrays/null, default False
            bool_out = False

        # INT output
        if isinstance(parsed, bool):
            int_out = int(parsed)
        elif isinstance(parsed, int):
            int_out = parsed
        elif isinstance(parsed, float):
            int_out = int(parsed)
        elif isinstance(parsed, str):
            try:
                int_out = int(parsed)
            except:
                int_out = 0
        else:
            int_out = 0

        # FLOAT output
        if isinstance(parsed, bool):
            float_out = float(parsed)
        elif isinstance(parsed, int):
            float_out = float(parsed)
        elif isinstance(parsed, float):
            float_out = parsed
        elif isinstance(parsed, str):
            try:
                float_out = float(parsed)
            except:
                float_out = 0.0
        else:
            float_out = 0.0

        # STRING output (no surrounding quotes)
        if isinstance(parsed, str):
            str_out = parsed
        else:
            # Serialize back to JSON but without wrapping quotes for primitives:
            # json.dumps on numbers/bools yields unquoted literals; on arrays/objects, we return the JSON text.
            str_out = json.dumps(parsed)

        return (bool_out, int_out, float_out, str_out)
