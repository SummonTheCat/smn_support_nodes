from inspect import cleandoc
import os

class SsnInputFont:
    """
    A node for selecting a font from the available fonts in the fonts directory.
    """
    def __init__(self):
        pass

    @classmethod
    def get_font_files(cls):
        """
        Get all .ttf files in the fonts directory, sorted by name.
        """
        font_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../resources/fonts"))

        if not os.path.exists(font_dir):
            return []
        return sorted([f for f in os.listdir(font_dir) if f.endswith(".ttf")])

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT", "FONT".
        Input types "INT", "STRING", "FLOAT" or "FONT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: dict
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
            - Value input_fields (`dict`): Contains input fields config:
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    + First value is a string indicating the type of field or a list for selection.
                    + Second value is a config for type "INT", "STRING", "FLOAT" or "FONT".
        """
        font_files = cls.get_font_files()
        return {
            "required": {
                "font_name": (font_files if font_files else ["default"], {
                    "default": "default",  # Default to "default" if no fonts are found
                }),
            },
        }

    RETURN_TYPES = ("FONT",)
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"


    def execute(self, font_name):
        """
        Execute the node with the selected font name.

        Args:
            font_name (str): The name of the selected font file.

        Returns:
            tuple: A tuple containing the font name.
        """
        return (font_name, )