# ----- Imports ----- #

# Input Imports
from .nodes_input.node_input_string import SsnInputString
from .nodes_input.node_input_int import SsnInputInt
from .nodes_input.node_input_float import SsnInputFloat
from .nodes_input.node_input_color import SsnInputColor  
from .nodes_input.node_input_font import SsnInputFont

# Convert Imports
from .nodes_convert.node_convert_int import SsnConvInt
from .nodes_convert.node_convert_float import SsnConvFloat
from .nodes_convert.node_convert_string import SsnConvString

# Output Imports
from .nodes_output.node_output_webm import SsnOutputWebM

# Image Draw Imports
from .nodes_draw.node_draw_text import SsnDrawText 

# JSON Imports
from .nodes_json.node_json_getkeyvalue import SsnJSONGetKeyValue
from .nodes_json.node_json_getindexvalue import SsnJsonGetIndexValue
from .nodes_json.node_json_getvalueas import SsnJsonValueAs

# Prep Imports
from .nodes_prep.node_prep_trimscale import SsnPrepTrimScale
from .nodes_prep.node_prep_flattenalpha import SsnPrepFlattenAlpha
from .nodes_prep.node_prep_batchappend import SsnPrepAppendBatch
from .nodes_prep.node_prep_batchreverse import SsnPrepReverseBatch


# ----- Node Class Mappings ----- #

# Node/Name Dictionary Mappings
# A dictionary that maps node class names to their respective classes
NODE_CLASS_MAPPINGS = {
    "SsnInputString": SsnInputString,
    "SsnInputInt": SsnInputInt,
    "SsnInputFloat": SsnInputFloat,
    "SsnInputColor": SsnInputColor,
    "SsnInputFont": SsnInputFont,

    "SsnConvInt": SsnConvInt,
    "SsnConvFloat": SsnConvFloat,
    "SsnConvString": SsnConvString,

    "SsnOutputWebM": SsnOutputWebM,

    "SsnDrawText": SsnDrawText,

    "SsnJSONGetKeyValue": SsnJSONGetKeyValue,
    "SsnJSONGetIndexValue": SsnJsonGetIndexValue,
    "SsnJSONGetValueAs": SsnJsonValueAs,

    "SsnPrepTrimScale": SsnPrepTrimScale,
    "SsnPrepFlattenAlpha": SsnPrepFlattenAlpha,
    "SsnPrepAppendBatch": SsnPrepAppendBatch,
    "SsnPrepReverseBatch": SsnPrepReverseBatch,
}

# ----- Node Display Name Mappings ----- #

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SsnInputString": "[SSN] Input String",
    "SsnInputInt": "[SSN] Input Integer",
    "SsnInputFloat": "[SSN] Input Float",
    "SsnInputColor": "[SSN] Input Color",
    "SsnInputFont": "[SSN] Input Font",

    "SsnConvInt": "[SSN] Convert Int To Others",
    "SsnConvFloat": "[SSN] Convert Float To Others",
    "SsnConvString": "[SSN] Convert String To Others",

    "SsnOutputWebM": "[SSN] Output WebM",

    "SsnDrawText": "[SSN] Draw Text",

    "SsnJSONGetKeyValue": "[SSN] JSON Get Key Value",
    "SsnJSONGetIndexValue": "[SSN] JSON Get Index Value",
    "SsnJSONGetValueAs": "[SSN] JSON Get Value As",

    "SsnPrepTrimScale": "[SSN] Prep Trim Scale",
    "SsnPrepFlattenAlpha": "[SSN] Prep Flatten Alpha",
    "SsnPrepAppendBatch": "[SSN] Prep Append Batch",
    "SsnPrepReverseBatch": "[SSN] Prep Reverse Batch",

}
