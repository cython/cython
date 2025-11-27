from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .Shadow import __version__

# Void cython.* directives (for case insensitive operating systems).
from .Shadow import *


def load_ipython_extension(ip: Any) -> None:
    """Load the extension in IPython."""
    from .Build.IpythonMagic import CythonMagics  # pylint: disable=cyclic-import
    ip.register_magics(CythonMagics)
