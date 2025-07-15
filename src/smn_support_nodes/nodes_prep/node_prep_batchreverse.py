import torch  # type: ignore

class SsnPrepReverseBatch:
    """
    A node that reverses the order of the image batch.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    DESCRIPTION = "Reverses the order of the image batch."
    FUNCTION = "execute"
    CATEGORY = "smn/prep"

    def execute(self, images: torch.Tensor):
        # Reverse the order of the batch
        result = images.flip(dims=[0])
        return (result, )
