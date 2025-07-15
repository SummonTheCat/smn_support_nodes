from inspect import cleandoc

class SsnConvInt:
    """
    A converter node that takes an integer input and outputs its string and float representations.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node: a single integer.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple: a STRING and a FLOAT.
    RETURN_NAMES (`tuple`):
        The name of the output ("String", "Float").
    FUNCTION (`str`):
        The entry-point method name ("execute").
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Converter").
    execute(integer) -> tuple:
        Returns a tuple containing the string form of the input integer.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "integer": (
                    "INT",
                    {
                        "default": 0,
                        "min": -2147483648,
                        "max": 2147483647,
                        "step": 1,
                        "display": "number"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT",)
    RETURN_NAMES = ("string", "float",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Converter"

    def __init__(self):
        pass

    def execute(self, integer):



        return (str(integer), float(integer),)  # Return both string and float representations
