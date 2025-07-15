import numpy as np
import torch  # type: ignore

def convert_tensor_to_np_array(image_tensor: torch.Tensor) -> np.ndarray:
    """
    Convert a tensor to a NumPy array.
    """
    try:
        tensor_image = (image_tensor.detach().cpu().numpy() * 255).astype(np.uint8)
        if tensor_image is None:
            raise ValueError("Conversion from tensor to NumPy array resulted in None")
        return tensor_image
    except Exception as e:
        raise RuntimeError(f"Error converting tensor to NumPy array: {e}")

def convert_np_array_to_tensor(image_np: np.ndarray, dtype) -> torch.Tensor:
    """
    Convert a NumPy array to a tensor.
    """
    try:
        tensor_image = torch.from_numpy(image_np).float() / 255
        tensor_image = tensor_image.to(dtype)
        if tensor_image is None:
            raise ValueError("Conversion from NumPy array to tensor resulted in None")
        return tensor_image
    except Exception as e:
        raise RuntimeError(f"Error converting NumPy array to tensor: {e}")

def convert_3ch_np_to_4ch_np(image_np: np.ndarray) -> np.ndarray:
    """
    Convert a 3-channel NumPy array to a 4-channel NumPy array.
    """
    try:
        if image_np.shape[-1] == 3:
            alpha_channel = np.ones((image_np.shape[0], image_np.shape[1], 1), dtype=image_np.dtype) * 255
            image_np = np.concatenate((image_np, alpha_channel), axis=-1)
        if image_np.shape[-1] != 4:
            raise ValueError("Conversion to 4-channel NumPy array failed")
        return image_np
    except Exception as e:
        raise RuntimeError(f"Error converting 3-channel NumPy array to 4-channel: {e}")

def convert_3ch_tensor_to_4ch_tensor(image_tensor: torch.Tensor) -> torch.Tensor:
    """
    Convert a 3-channel tensor to a 4-channel tensor.
    """
    try:
        if image_tensor.shape[-1] == 3:
            alpha_channel = torch.ones((image_tensor.shape[0], image_tensor.shape[1], 1), dtype=image_tensor.dtype)
            image_tensor = torch.cat((image_tensor, alpha_channel), dim=-1)
        if image_tensor.shape[-1] != 4:
            raise ValueError("Conversion to 4-channel tensor failed")
        return image_tensor
    except Exception as e:
        raise RuntimeError(f"Error converting 3-channel tensor to 4-channel: {e}")

def convert_3ch_batch_to_4ch_tbatch(tensor_batch: torch.Tensor) -> tuple:
    """
    Convert a batch of 3-channel tensors to 4-channel tensors and return the modified tensor along with its shape details.
    """
    try:
        batch_size, height, width, channels = tensor_batch.shape
        if channels == 3:
            alpha_channel = torch.ones((batch_size, height, width, 1), dtype=tensor_batch.dtype)
            tensor_batch = torch.cat((tensor_batch, alpha_channel), dim=-1)
            channels = 4  # Update the channels count
        if tensor_batch.shape[-1] != 4:
            raise ValueError("Conversion to 4-channel tensor batch failed")
        return tensor_batch, batch_size, height, width, channels
    except Exception as e:
        raise RuntimeError(f"Error converting 3-channel tensor batch to 4-channel: {e}")

def build_tensor_batch_from_nparray(image_np: np.ndarray) -> torch.Tensor:
    """
    Convert a single image (NumPy array) into a tensor batch.
    """
    try:
        image_tensor = convert_np_array_to_tensor(image_np, torch.float32)
        image_tensor_batch = image_tensor.unsqueeze(0)  # Add batch dimension
        return image_tensor_batch
    except Exception as e:
        raise RuntimeError(f"Error building tensor batch from NumPy array: {e}")
