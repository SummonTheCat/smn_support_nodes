from inspect import cleandoc
import numpy as np
import torch  # type: ignore
from ..util_convert import convert_np_array_to_tensor, convert_tensor_to_np_array

class SsnPrepFlattenAlpha:
    """
    A node that takes images with alpha and flattens them onto a background color, removing the alpha channel.
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
                "background_color": ("COLOR", {
                    "default": "#000000",  # Default black background
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/prep"

    def execute(self, images: torch.Tensor, background_color):
        batch_size, height, width, channels = images.shape
        assert channels == 4, "Images must be RGBA"

        # Convert background_color to RGB tuple if needed
        if isinstance(background_color, str):
            bg_rgb = tuple(int(background_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        else:
            bg_rgb = background_color

        result = torch.zeros((batch_size, height, width, 3), dtype=images.dtype)

        for b in range(batch_size):
            img_np = convert_tensor_to_np_array(images[b])

            if img_np.dtype != np.uint8:
                img_np = (img_np * 255).astype(np.uint8)

            rgb = img_np[:, :, :3].astype(np.float32)
            alpha = img_np[:, :, 3:4].astype(np.float32) / 255.0

            bg = np.ones_like(rgb) * np.array(bg_rgb, dtype=np.float32)

            flattened = rgb * alpha + bg * (1 - alpha)
            flattened = np.clip(flattened, 0, 255).astype(np.uint8)

            result[b] = convert_np_array_to_tensor(flattened, images.dtype)

        return (result, )

