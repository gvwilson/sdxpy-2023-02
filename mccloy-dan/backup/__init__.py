"""Not a real package, just want relative imports."""

__version__ = '0.1'

from .compare_manifests import compare_manifests
from .file_history import file_history, parse_entry
from .finddup import find_duplicates
