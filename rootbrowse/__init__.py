"""RootBrowse - Python浏览器自动化 MCP 框架"""

__author__ = "zimvir"
__email__ = "zimvir@qq.com"

from .core import (
    __version__,
    Browser,
    TabManager,
    ElementOperator,
    PageScanner,
    Region,
    Element,
    RegionSummary,
    ElementPreview,
    OperationResult,
    RootBrowseError,
    BrowserError,
    ElementNotFoundError,
    RegionNotFoundError,
    TabNotFoundError,
    OperationError,
    StateFileError,
    PageLoadError,
    View,
    Operation,
    Tab
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
    "View",
    "Operation",
    "Tab"
]