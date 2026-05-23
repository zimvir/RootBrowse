"""RootBrowse - Python 浏览器自动化 MCP 框架"""

from ._version import __version__
from .browser import Browser
from .tab_manager import TabManager
from .element_operator import ElementOperator
from .page_scanner import PageScanner
from .types import Region, Element, RegionSummary, ElementPreview, OperationResult
from .exceptions import (
    RootBrowseError,
    BrowserError,
    ElementNotFoundError,
    RegionNotFoundError,
    TabNotFoundError,
    OperationError,
    StateFileError,
    PageLoadError,
)

__all__ = [
    "__version__",
    "Browser",
    "TabManager",
    "ElementOperator",
    "PageScanner",
    "Region",
    "Element",
    "RegionSummary",
    "ElementPreview",
    "OperationResult",
    "RootBrowseError",
    "BrowserError",
    "ElementNotFoundError",
    "RegionNotFoundError",
    "TabNotFoundError",
    "OperationError",
    "StateFileError",
    "PageLoadError",
]
