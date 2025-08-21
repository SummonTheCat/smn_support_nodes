"""Top-level package for smn_comfy."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """smn_comfy"""
__email__ = "julien_andrew@outlook.com"
__version__ = "1.0.5"

from .src.smn_support_nodes.nodes import NODE_CLASS_MAPPINGS
from .src.smn_support_nodes.nodes import NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "./web"
