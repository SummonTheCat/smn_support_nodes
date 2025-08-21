from inspect import cleandoc
import shutil
import numpy as np
import torch
import folder_paths
import subprocess
import os
import time
from datetime import datetime

from ..util_convert import (
    convert_tensor_to_np_array,
)

from typing import List, Tuple
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
            },
            "optional": {
                "pass_through": ("IMAGE",)
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "execute"
    CATEGORY = "output"

    # ---------- small logging helpers ----------
    def _ts(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log_line(self, s: str) -> str:
        return f"[{self._ts()}] {s}\n"

    def _stage_start(self, name: str) -> float:
        print(self._log_line(f"--- {name} START ---").rstrip())
        return time.perf_counter()

    def _stage_end(self, name: str, t0: float) -> str:
        dt = time.perf_counter() - t0
        line = self._log_line(f"--- {name} END ({dt:.3f}s) ---")
        print(line.rstrip())
        return line

    def execute(
        self,
        images: torch.Tensor,
        framerate: int,
        bitrate_mb: float,
        output_path: str,
        pass_through: torch.Tensor = None
    ) -> tuple:
        # master log string
        log = ""
        log += "\n" + "=" * 72 + "\n"
        log += self._log_line("SsnOutputWebM Log")
        log += "=" * 72 + "\n"

        # ---- Stage: Validate / Describe Inputs ----
        t0 = self._stage_start("Input Validation & Description")

        if images.ndim != 4:
            err = f"Error: expected 4D tensor (N,H,W,C) or (N,C,H,W); got shape {tuple(images.shape)}"
            log += self._log_line(err)
            log += self._stage_end("Input Validation & Description", t0)
            return (log,)

        n, h, w, c = self._infer_nhwc_shape(images)
        if c not in (1, 2, 3, 4):
            err = f"Error: unsupported channel count {c}. Expected 1, 2, 3, or 4."
            log += self._log_line(err)
            log += self._stage_end("Input Validation & Description", t0)
            return (log,)

        path_comfy_out = folder_paths.get_output_directory()
        path_gen_output = os.path.join(path_comfy_out, output_path)
        path_gen_frames = os.path.join(path_gen_output, "frames")
        path_gen_pass_through = os.path.join(path_gen_output, "pass_through")

        base_name = os.path.basename(output_path.rstrip("/\\"))
        output_file = os.path.join(path_gen_output, f"{base_name}.webm")

        # Input summary
        log += self._log_line("[Input Data]")
        log += self._log_line(f"  Image tensor shape: {tuple(images.shape)}")
        log += self._log_line(f"  Interpreted as: N={n}, H={h}, W={w}, C={c}")
        log += self._log_line(f"  Framerate: {framerate}")
        log += self._log_line(f"  Bitrate: {bitrate_mb} MB")
        log += self._log_line(f"  Output Path (relative to Comfy output): {output_path}")
        log += self._log_line(f"  Pass-through provided: {'Yes' if pass_through is not None else 'No'}")

        # Paths
        log += self._log_line("[Working Directories]")
        log += self._log_line(f"  CWD: {os.getcwd()}")
        log += self._log_line(f"  Output Dir: {path_gen_output}")
        log += self._log_line(f"  Frames Dir: {path_gen_frames}")
        log += self._log_line(f"  Pass-through Dir: {path_gen_pass_through}")
        log += self._log_line(f"  Output file: {output_file}")

        log += self._stage_end("Input Validation & Description", t0)

        # ---- Stage: Prepare Pass-through Frames (if any) ----
        if pass_through is not None:
            t1 = self._stage_start("Prepare Pass-through Frames")
            try:
                pt_paths, pt_log = self._prepare_frames(
                    pass_through, path_gen_pass_through, filename_prefix="pass_through_frame_"
                )
                log += self._log_line("[Pass-through]")
                log += pt_log
                log += self._log_line(f"[Prepared {len(pt_paths)} pass-through frames]")
            except Exception as e:
                log += self._log_line(f"Error preparing pass-through frames: {e}")
            log += self._stage_end("Prepare Pass-through Frames", t1)

        # ---- Stage: Prepare Main Frames ----
        t2 = self._stage_start("Prepare Frames")
        try:
            frame_paths, frames_log = self._prepare_frames(
                images, path_gen_frames, filename_prefix="frame_"
            )
            log += frames_log
            log += self._log_line(f"[Prepared {len(frame_paths)} frames for ffmpeg]")
        except Exception as e:
            log += self._log_line(f"Error preparing frames: {e}")
            log += self._stage_end("Prepare Frames", t2)
            return (log,)
        log += self._stage_end("Prepare Frames", t2)

        # ---- Stage: ffmpeg Encode ----
        t3 = self._stage_start("ffmpeg Encode")

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-framerate", str(framerate),
            "-pattern_type", "sequence",
            "-start_number", "0",
            "-i", os.path.join(path_gen_frames, "frame_%02d.png"),
            "-s", f"{w}x{h}",
            "-c:v", "libvpx",
            "-b:v", f"{bitrate_mb}M",
            "-c:a", "libopus",
            "-auto-alt-ref", "0",
            output_file
        ]

        log += self._log_line("[ffmpeg Command]")
        log += self._log_line("  " + " ".join(ffmpeg_cmd))

        try:
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False
            )
            log += self._log_line(f"ffmpeg exit code: {result.returncode}")
            # keep ffmpeg output as a block for readability
            log += "\n" + "-" * 28 + " ffmpeg output " + "-" * 28 + "\n"
            log += result.stdout
            log += "\n" + "-" * 72 + "\n"

            if result.returncode != 0:
                log += self._log_line("Error: ffmpeg reported a non-zero exit code.")
        except Exception as e:
            log += self._log_line(f"Error running ffmpeg: {e}")
            log += self._stage_end("ffmpeg Encode", t3)
            return (log,)

        log += self._stage_end("ffmpeg Encode", t3)

        # ---- Stage: Finalization ----
        t4 = self._stage_start("Finalization")
        if 'result' in locals() and result.returncode == 0:
            log += self._log_line(f"[Success] WebM file created: {output_file}")
        else:
            log += self._log_line("[Failure] WebM file creation failed")
        log += self._stage_end("Finalization", t4)

        # Print once more at the end for debugging convenience
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

    def _infer_nhwc_shape(self, images: torch.Tensor) -> Tuple[int, int, int, int]:
        """
        Accept (N,H,W,C) or (N,C,H,W). Return as NHWC shape tuple.
        """
        if images.shape[-1] in (1, 2, 3, 4):  # NHWC
            n, h, w, c = images.shape
            return int(n), int(h), int(w), int(c)
        elif images.shape[1] in (1, 2, 3, 4):  # NCHW
            n, c, h, w = images.shape
            return int(n), int(h), int(w), int(c)
        else:
            # Fallback to treating as NHWC
            n, h, w, c = images.shape
            return int(n), int(h), int(w), int(c)

    def _prepare_frames(
        self,
        images: torch.Tensor,
        frames_dir: str,
        filename_prefix: str = "frame_"
    ) -> tuple[List[str], str]:
        """
        Save each frame in `images` (supports N×H×W×{1,2,3,4} or N×{1,2,3,4}×H×W; float [0,1] or uint8)
        to PNG files in `frames_dir`, choosing an appropriate PIL mode:

          channels == 1 -> 'L'
          channels == 2 -> 'LA'
          channels == 3 -> 'RGB'
          channels == 4 -> 'RGBA'

        Preserves channel semantics; does not force alpha.
        """
        # Stage timing for this helper
        t0 = time.perf_counter()

        # Clean and recreate output dir
        if os.path.isdir(frames_dir):
            shutil.rmtree(frames_dir)
        os.makedirs(frames_dir, exist_ok=True)

        frame_paths: List[str] = []
        lines: List[str] = []
        lines.append(self._log_line(f"[Saving frames to: {frames_dir}]"))

        nhwc_like = images.shape[-1] in (1, 2, 3, 4)
        n = images.shape[0]

        for idx in range(n):
            frame = images[idx]

            # Detach & CPU
            frame = frame.detach().cpu()

            # Convert to HWC
            if frame.ndim == 3:
                if nhwc_like:
                    hwc = frame
                else:
                    hwc = frame.permute(1, 2, 0)
            else:
                raise ValueError(f"Expected per-frame tensor of rank 3, got shape {tuple(frame.shape)}")

            # Ensure uint8 in [0,255]
            if hwc.dtype.is_floating_point:
                hwc = hwc.clamp(0.0, 1.0).mul(255.0).to(torch.uint8)
            elif hwc.dtype != torch.uint8:
                hwc = hwc.to(torch.uint8)

            frame_np = hwc.numpy()
            channels = frame_np.shape[2]

            # Pick PIL mode
            if channels == 1:
                mode = "L"
            elif channels == 2:
                mode = "LA"
            elif channels == 3:
                mode = "RGB"
            elif channels == 4:
                mode = "RGBA"
            else:
                if channels > 4:
                    frame_np = frame_np[:, :, :4]
                    mode = "RGBA"
                else:
                    raise ValueError(f"Unsupported channel count {channels} for frame {idx}")

            img = Image.fromarray(frame_np, mode=mode)

            filename = f"{filename_prefix}{idx:02d}.png"
            path = os.path.join(frames_dir, filename)
            img.save(path, format="PNG", compress_level=4)

            lines.append(self._log_line(
                f"  Saved {filename}  ({mode}, {frame_np.shape[1]}x{frame_np.shape[0]})"
            ))
            frame_paths.append(path)

        dt = time.perf_counter() - t0
        lines.append(self._log_line(f"[Saved {len(frame_paths)} frames in {dt:.3f}s]"))

        return frame_paths, "".join(lines)
