from inspect import cleandoc

class SsnInputJSON:
    """
    A node that provides a multi-line textbox for JSON input and outputs the entered string.

    Class methods
    -------------
    INPUT_TYPES (dict):
        Defines the input fields for this node. In this case, a single multi-line string field.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of the output tuple. Here, it is a single STRING.
    RETURN_NAMES (`tuple`):
        Optional: The name of the output ("value").
    FUNCTION (`str`):
        The name of the entry-point method. This node uses "execute".
    CATEGORY (`str`):
        The category under which this node appears in the UI ("Input").
    execute(string) -> tuple:
        The entry-point method that returns the JSON string entered by the user.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "{}"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "Input"

    def __init__(self):
        pass

    def execute(self, string):
        return (string,)
