from inspect import cleandoc

class SsnInputInt:
    """
    A node that provides a numeric textbox for integer input and outputs the entered integer.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node. In this case, a single integer field.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple. Here, it is a single INT.
    RETURN_NAMES (`tuple`):
        Optional: The name of the output ("value").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Input").
    execute(integer) -> tuple:
        The entry-point method that returns the integer entered by the user.
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

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("value",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Input"

    def __init__(self):
        pass

    def execute(self, integer):
        return (integer,)
