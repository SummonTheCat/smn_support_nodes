from inspect import cleandoc
import numpy as np
import torch  # type: ignore
from ..util_convert import convert_np_array_to_tensor, convert_tensor_to_np_array
import cv2

class SsnPrepCrop:
    """
    A node that takes an image batch and adjusts the canvas size by either clipping or filling whitespace,
    while keeping the original content centered.
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
                "images": ("IMAGE",),
                "target_width": ("INT", {"widget": "int_field"}),
                "target_height": ("INT", {"widget": "int_field"}),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/prep"

    def execute(self, images: torch.Tensor, target_width: int, target_height: int):
        batch_size, height, width, channels = images.shape
        assert channels == 4, "Images must be RGBA"

        result = torch.zeros((batch_size, target_height, target_width, 4), dtype=images.dtype)

        for b in range(batch_size):
            img_np = convert_tensor_to_np_array(images[b])

            # Convert to RGBA if needed
            if img_np.shape[2] == 3:
                img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2RGBA)

            h, w = img_np.shape[:2]
            paste_x = (target_width - w) // 2
            paste_y = (target_height - h) // 2

            new_img = np.zeros((target_height, target_width, 4), dtype=np.uint8)

            if paste_x >= 0 and paste_y >= 0:
                # Image is smaller than target: center it with padding
                new_img[paste_y:paste_y + h, paste_x:paste_x + w, :] = img_np
            else:
                # Image is larger than target: center-crop it
                start_x = max(0, -paste_x)
                start_y = max(0, -paste_y)
                end_x = min(w, target_width - paste_x)
                end_y = min(h, target_height - paste_y)

                crop = img_np[start_y:end_y, start_x:end_x]
                new_img[:end_y - start_y, :end_x - start_x] = crop

            result[b] = convert_np_array_to_tensor(new_img, images.dtype)

        return (result, )
