from __future__ import annotations

import sys

if sys.version_info < (3, 12):  # pragma: no cover
    from typing import Final
else:
    from typing import Final

DEFAULT_FILE_TO_GRAB_VERSION: Final = 'pyproject.toml'
