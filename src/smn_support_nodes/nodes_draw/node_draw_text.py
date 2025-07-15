import numpy as np
import torch  # type: ignore
from inspect import cleandoc
from ..util_convert import (
    convert_np_array_to_tensor,
    convert_tensor_to_np_array,
    convert_3ch_np_to_4ch_np,
)
from PIL import Image, ImageDraw, ImageFont  # type: ignore
import os

class SsnDrawText:
    """
    A node for drawing text onto an image.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", ),
                "text_content": ("STRING", {
                    "default": "Sample Text",
                }),
                "text_pos_x": ("INT", {
                    "default": 0,
                }),
                "text_pos_y": ("INT", {
                    "default": 0,
                }),
                "text_size": ("INT", {
                    "default": 12,
                }),
                "text_color": ("COLOR", {
                    "default": "#FFFFFF",
                }),
                "font_name": ("FONT", ),
                "text_align_horizontal": (["left", "center", "right"], {
                    "default": "left",
                }),
                "text_align_vertical": (["top", "center", "bottom"], {
                    "default": "top",
                }),
                "debug": ("BOOLEAN", {
                    "default": False,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/draw"

    def execute(
        self, image, text_content, text_pos_x, text_pos_y, text_size, text_color,
        font_name, text_align_horizontal, text_align_vertical, debug
    ):
        try:
            batch_size, height, width, channels = image.shape
        except Exception as e:
            raise ValueError(f"Error getting image shape: {e}. Input image: {image}")

        # Prepare result tensor, matching input shape (force 4 channels)
        result = torch.zeros((batch_size, height, width, 4), dtype=image.dtype)

        # Font path setup
        font_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "../resources/fonts"))
        font_true_path = os.path.join(font_dir, font_name) if font_name != "default" else None
        if font_name != "default" and not os.path.exists(font_true_path):
            raise ValueError(f"Font file not found: {font_true_path}")

        # Convert text color
        try:
            if isinstance(text_color, tuple) and len(text_color) == 3:
                text_color_rgb = text_color
            else:
                text_color_rgb = tuple(int(text_color[i:i+2], 16) for i in (1, 3, 5))
        except Exception as e:
            raise ValueError(f"Error parsing text color: {e}")

        for b in range(batch_size):
            # Convert tensor to numpy
            img_np = convert_tensor_to_np_array(image[b])

            # Ensure 4-channel (RGBA) using helper
            img_np = convert_3ch_np_to_4ch_np(img_np)

            # Convert to PIL Image
            pil_image = Image.fromarray(img_np, mode='RGBA')
            draw = ImageDraw.Draw(pil_image)

            # Load font
            try:
                font = (
                    ImageFont.truetype(font_true_path, text_size)
                    if font_true_path else ImageFont.load_default()
                )
            except Exception as e:
                raise ValueError(f"Error loading font: {e}")

            # Calculate text size
            try:
                text_width = draw.textlength(text_content, font=font)
                bbox = draw.textbbox((0, 0), text_content, font=font)
                text_height = bbox[3] - bbox[1]
            except Exception as e:
                raise ValueError(f"Error calculating text size: {e}")

            # Align position
            pos_x = (
                text_pos_x - text_width // 2 if text_align_horizontal == "center"
                else text_pos_x - text_width if text_align_horizontal == "right"
                else text_pos_x
            )
            pos_y = (
                text_pos_y - text_height // 2 if text_align_vertical == "center"
                else text_pos_y - text_height if text_align_vertical == "bottom"
                else text_pos_y
            )

            # Draw text with full alpha
            try:
                draw.text((pos_x, pos_y), text_content, font=font, fill=text_color_rgb + (255,))
            except Exception as e:
                raise ValueError(f"Error drawing text on image: {e}")

            # Convert back to numpy, ensure RGBA
            out_np = np.array(pil_image.convert('RGBA'))
            out_np = convert_3ch_np_to_4ch_np(out_np)

            # Convert to tensor and assign
            try:
                result[b] = convert_np_array_to_tensor(out_np, image.dtype)
            except Exception as e:
                raise ValueError(f"Error converting numpy array to tensor for batch {b}: {e}")

        return (result, )

