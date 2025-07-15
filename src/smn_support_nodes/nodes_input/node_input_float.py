from inspect import cleandoc

class SsnInputFloat:
    """
    A node that provides a numeric textbox for float input and outputs the entered float.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node. In this case, a single float field.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple. Here, it is a single FLOAT.
    RETURN_NAMES (`tuple`):
        Optional: The name of the output ("value").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Input").
    execute(float_value) -> tuple:
        The entry-point method that returns the float entered by the user.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "float_value": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -1e6,
                        "max": 1e6,
                        "step": 0.01,
                        "round": 0.001,
                        "display": "number"
                    }
                )
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Input"

    def __init__(self):
        pass

    def execute(self, float_value):
        return (float_value,)
