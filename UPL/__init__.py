from . import upl_photoTools as photoTools
from . import gui_impliments as gui
from . import upl_cipher
from . import upl_logger
from . import upl_sound
from . import upl_time
from . import upl_byte
from . import Core 
"""
added upl_keyboard
"""

## removed upl_socket because it served no purpose nor one that
## was deemed useful to the library itself

__version__ = "0.0.6"
cwd = Core.currentDir()
home = Core.getHome()

null = None
void = None

EXIT_FAILURE = 1
EXIT_SUCCESS = 0