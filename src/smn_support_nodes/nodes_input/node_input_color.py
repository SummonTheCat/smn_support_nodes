from inspect import cleandoc
import numpy as np
import torch  # type: ignore
from ..util_convert import convert_3ch_np_to_4ch_np, build_tensor_batch_from_nparray

class SsnInputColor:
    """
    A node for referencing externally to set a color value, also has a nice input field for editing.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return a dictionary which contains config for all input fields.
        Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
        Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
        The type can be a list for selection.

        Returns: dict
            - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property "required"
            - Value input_fields (`dict`): Contains input fields configurations.
                * Key field_name (`string`): Name of a entry-point method's argument
                * Value field_config (`tuple`):
                    - First value is a string indicating the type of field or a list for selection.
                    - Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "color_field": ("STRING", {
                    "default": "#000000",  # Default color is black
                }),
            },
        }

    RETURN_TYPES = ("COLOR", "IMAGE")
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/input"

    def execute(self, color_field):
        """
        Convert hex color to RGB tuple
        """
        color = self.hex_to_rgb(color_field)

        # Create a small block of the color
        color_block = self.create_color_block(color)

        # Convert the color block to a tensor batch
        color_block_tensor_batch = build_tensor_batch_from_nparray(color_block)

        return (color, color_block_tensor_batch)

    def hex_to_rgb(self, hex_color):
        """
        Convert hex color string to RGB tuple.
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_color_block(self, color):
        """
        Create a small block of the given color.
        """
        block_size = (50, 50, 3)  # 50x50 block with 3 color channels
        color_block = np.zeros(block_size, dtype=np.uint8)
        color_block[:, :] = color

        # Convert to 4-channel (RGBA)
        color_block = convert_3ch_np_to_4ch_np(color_block)

        return color_block
