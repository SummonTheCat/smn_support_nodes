from inspect import cleandoc
import torch  # type: ignore

class SsnPrepAppendBatch:
    """
    A node that appends one batch of images to another if they are the same size.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_a": ("IMAGE", ),
                "images_b": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "smn/prep"

    def execute(self, images_a: torch.Tensor, images_b: torch.Tensor):
        # Check if the image batches have the same shape
        if images_a.shape[1:] != images_b.shape[1:]:
            raise ValueError("Image batches must have the same dimensions except for the batch size.")

        # Concatenate the batches along the batch dimension
        result = torch.cat((images_a, images_b), dim=0)

        return (result, )
