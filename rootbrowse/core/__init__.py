"""RootBrowse - Python 浏览器自动化 MCP 框架"""

from ._version import __version__
from .browser import Browser
from .view import View
from .tab import Tab
from .operation import Operation
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

# 别名，保持向后兼容
TabManager = Tab
ElementOperator = Operation
PageScanner = View

__all__ = [
    "__version__",
    "Browser",
    "View",
    "Tab",
    "Operation",
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
    # 别名
    "TabManager",
    "ElementOperator",
    "PageScanner",
]