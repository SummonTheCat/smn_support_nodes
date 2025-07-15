from inspect import cleandoc
import cv2
import numpy as np
import torch  # type: ignore
from ..util_convert import convert_np_array_to_tensor, convert_tensor_to_np_array
import random

class SsnPrepTrimScale:
    """
    A node that takes an image, trims it to size, then scales each to the width or height of the image.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Return a dictionary which contains config for all input fields.
        """
        return {
            "required": {
                "images": ("IMAGE", ),
                "trim_padding": ("INT", {"widget": "int_field"}),
                "trim_threshold": ("INT", {"widget": "int_field", "min": 0, "max": 255}),
                "target_width": ("INT", {"widget": "int_field"}),
                "target_height": ("INT", {"widget": "int_field"}),
                "debug": ("BOOLEAN", {"widget": "checkbox"}),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/prep"

    def execute(self, images: torch.Tensor, trim_padding: int, trim_threshold: int, target_width: int, target_height: int, debug: bool):
        batch_size, height, width, channels = images.shape
        assert channels == 4, "Images must be RGBA"

        result = torch.zeros((batch_size, target_height, target_width, channels), dtype=images.dtype)

        for b in range(batch_size):
            modified_image = convert_tensor_to_np_array(images[b])

            # Convert to RGBA if not already
            if modified_image.shape[2] == 3:
                modified_image = cv2.cvtColor(modified_image, cv2.COLOR_RGB2RGBA)

            # Trim the image by checking from the outside in until we hit a non-alpha pixel
            alpha_channel = modified_image[:, :, 3]
            non_alpha_indices = np.where(alpha_channel > trim_threshold)

            if non_alpha_indices[0].size > 0:
                min_y = max(np.min(non_alpha_indices[0]) - trim_padding, 0)
                max_y = min(np.max(non_alpha_indices[0]) + trim_padding, modified_image.shape[0])
                min_x = max(np.min(non_alpha_indices[1]) - trim_padding, 0)
                max_x = min(np.max(non_alpha_indices[1]) + trim_padding, modified_image.shape[1])
                trimmed_image = modified_image[min_y:max_y, min_x:max_x]
            else:
                trimmed_image = modified_image

            if debug:
                # Fill the background with red
                red_background = np.zeros_like(trimmed_image)
                red_background[:, :, 0] = 255  # Red channel
                red_background[:, :, 3] = 255  # Alpha channel
                alpha_mask = trimmed_image[:, :, 3]
                red_background[alpha_mask > 0] = trimmed_image[alpha_mask > 0]
                trimmed_image = red_background

            # Scale the trimmed image while maintaining the aspect ratio
            aspect_ratio = trimmed_image.shape[1] / trimmed_image.shape[0]
            new_width = target_width
            new_height = int(new_width / aspect_ratio)
            if new_height > target_height:
                new_height = target_height
                new_width = int(new_height * aspect_ratio)

            scaled_image = cv2.resize(trimmed_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Create a new image with the target dimensions and random background color
            new_img = np.zeros((target_height, target_width, 4), dtype=np.uint8)
            if debug:
                random_color = [random.randint(0, 255) for _ in range(3)]
                new_img[:, :, 0] = random_color[0]  # Red channel
                new_img[:, :, 1] = random_color[1]  # Green channel
                new_img[:, :, 2] = random_color[2]  # Blue channel
                new_img[:, :, 3] = 255  # Alpha channel

            # Calculate the position to paste the resized image to center it
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2

            # Paste the resized image onto the new image
            new_img[paste_y:paste_y + new_height, paste_x:paste_x + new_width, :] = scaled_image

            # Convert back to tensor and store in result
            result[b] = convert_np_array_to_tensor(new_img, images.dtype)

        return (result, )
