from inspect import cleandoc

class SsnConvFloat:
    """
    A converter node that takes a float input and outputs its string representation,
    its integer base (truncating the decimal part), and its integer rounded to the nearest whole number.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node: a single float.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The types of the output tuple: STRING, INT, INT.
    RETURN_NAMES (`tuple`):
        The names of the outputs ("string", "int_base", "int_round").
    FUNCTION (`str`):
        The entry-point method name ("execute").
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Converter").
    execute(float_value) -> tuple:
        Returns (string, int_base, int_round) for the input float.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -1e6,
                        "max": 1e6,
                        "step": 0.01,
                        "display": "number"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING", "INT", "INT",)
    RETURN_NAMES = ("string", "int_base", "int_round",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Converter"

    def __init__(self):
        pass

    def execute(self, float):
        # Convert to string
        s = str(float)
        # Truncate decimal part
        int_base = int(float)
        # Round to nearest integer
        int_round = int(round(float))
        return (s, int_base, int_round)
