from inspect import cleandoc
import shutil
import numpy as np
import torch
import folder_paths
import subprocess
import os

from typing import List
from PIL import Image


class SsnOutputWebM:
    """
    A node that converts an image batch to WebM.
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
                "framerate": ("INT", {"default": 25, "min": 5, "max": 60, "step": 1}),
                "bitrate_mb": ("FLOAT", {"default": 10.0, "min": 1.0, "max": 100.0, "step": 1}),
                "output_path": ("STRING",),
            }
        }

    RETURN_TYPES = ()


    OUTPUT_NODE = True
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "output"


    def execute(
        self,
        images: torch.Tensor,
        framerate: int,
        bitrate_mb: float,
        output_path: str,
    ) -> tuple:

        log = ""

        # Get initial variables
        frame_count = images.shape[0]
        height = images.shape[1]
        width = images.shape[2]

        path_comfy_out = folder_paths.get_output_directory()
        path_gen_output = os.path.join(path_comfy_out, output_path)
        path_gen_frames = os.path.join(path_gen_output, "frames")

        # Add inputs to log
        log += "\n[Input Data]"
        log += f"\nImage Field: {images.shape if isinstance(images, torch.Tensor) else 'Not a tensor'}"
        log += f"\nFrame count: {frame_count if isinstance(images, torch.Tensor) else 'Not a tensor'}"
        log += f"\nSize: {width}x{height}"
        log += f"\nFramerate: {framerate}"
        log += f"\nBitrate: {bitrate_mb}MB"
        log += f"\nOutput Path: {output_path}"

        # Path handling
        log += "\n\n[Working Directory]"
        log += f"\nWorking Directory: {os.getcwd()}"
        log += f"\nGenerated Output: {path_gen_output}"
        log += f"\nGenerated Frames: {path_gen_frames}"

        # Channel check
        if images.shape[3] != 4:
            log += "\nError: Image field must have 4 channels (RGBA)."
            return (log,)

        base_name = os.path.basename(output_path.rstrip("/\\"))
        output_file = os.path.join(path_gen_output, f"{base_name}.webm")

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",  # overwrite output if exists
            "-framerate", str(framerate),
            "-pattern_type", "sequence",
            "-start_number", "0",
            "-i", os.path.join(path_gen_frames, "frame_%02d.png"),
            "-s", f"{width}x{height}",
            "-c:v", "libvpx",
            "-b:v", f"{bitrate_mb}M",
            "-c:a", "libopus",
            "-auto-alt-ref", "0",
            output_file
        ]

        log += "\n\n[ffmpeg Command]"
        log += "\n" + " ".join(ffmpeg_cmd)

        # Prepare frames for ffmpeg
        frame_paths, frames_log = self._prepare_frames(images, path_gen_frames)
        log += frames_log
        log += f"\n\n[Prepared {len(frame_paths)} frames for ffmpeg]"

        # Run ffmpeg and capture output
        log += "\n\n[Running ffmpeg]"
        try:
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False
            )
            log += f"\nffmpeg exit code: {result.returncode}"
            log += "\nffmpeg output:\n" + result.stdout
            if result.returncode != 0:
                log += "\nError: ffmpeg reported a non-zero exit code."
        except Exception as e:
            log += f"\nError running ffmpeg: {e}"


        # Return the pin outputs for log, and the actual output file path
        if result.returncode == 0:
            log += f"\n\n[WebM file created successfully at {output_file}]"
        else:
            log += "\n\n[WebM file creation failed]"

        print(log)


        # build a FileLocator-like list so ComfyUI can show it in the queue:
        results = [{
            "filename": os.path.basename(output_file),
            "subfolder": os.path.dirname(output_file),
            "type": "output"
        }]

        return {
        "ui": {
            "images": results,
            "animated": (True,)
        }
}




    def _prepare_frames(self, images: torch.Tensor, frames_dir: str) -> tuple[List[str], str]:
        """
        Save each frame in `images` (NxHxWx4 float or uint8 tensor)
        as frame_XX.png in `frames_dir`, zero-padding to two digits.
        Returns the list of full file paths and a log of what was saved.
        """
        # 1. Clean and recreate output dir
        if os.path.isdir(frames_dir):
            shutil.rmtree(frames_dir)
        os.makedirs(frames_dir, exist_ok=True)

        frame_paths: List[str] = []
        num_frames = images.shape[0]

        # collect per-frame log messages here
        frames_log = "\n\n[Saving frames]\n"

        for idx in range(num_frames):
            frame = images[idx]

            # a) Detach & CPU
            frame = frame.detach().cpu()

            # b) If floats, scale
            if frame.dtype.is_floating_point:
                frame = frame.clamp(0.0, 1.0).mul(255.0)

            # c) Cast to uint8
            frame = frame.to(torch.uint8)

            # d) Permute from C×H×W to H×W×C, or if already H×W×C skip
            if frame.ndim == 3 and frame.shape[0] in (3, 4):
                frame_np = frame.permute(1, 2, 0).numpy()
            else:
                frame_np = frame.numpy()

            # 3. Build PIL image and save
            img = Image.fromarray(frame_np, mode="RGBA")
            filename = f"frame_{idx:02d}.png"
            path = os.path.join(frames_dir, filename)
            img.save(path, format="PNG", compress_level=4)

            frames_log += f"Saved frame {idx + 1}/{num_frames} to {path}\n"
            frame_paths.append(path)

        return frame_paths, frames_log
