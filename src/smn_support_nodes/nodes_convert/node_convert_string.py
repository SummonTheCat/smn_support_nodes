from inspect import cleandoc

class SsnConvString:
    """
    A converter node that takes a string input and outputs its float and integer representations,
    defaulting to 0 if the conversion fails.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node: a single string.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The types of the output tuple: FLOAT and INT.
    RETURN_NAMES (`tuple`):
        The names of the outputs ("float", "int").
    FUNCTION (`str`):
        The entry-point method name ("execute").
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Converter").
    execute(string_value) -> tuple:
        Returns (float_value, int_value) converted from the input string, or (0.0, 0) on failure.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "display": "text"
                    }
                )
            }
        }

    RETURN_TYPES = ("FLOAT", "INT",)
    RETURN_NAMES = ("float", "int",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Converter"

    def __init__(self):
        pass

    def execute(self, string):
        try:
            f = float(string)
        except (ValueError, TypeError):
            f = 0.0
        try:
            i = int(f)
        except (ValueError, TypeError):
            i = 0
        return (f, i)
