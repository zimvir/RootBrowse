"""自定义异常"""


class RootBrowseError(Exception):
    """RootBrowse 基异常"""
    pass


class BrowserError(RootBrowseError):
    """浏览器相关错误"""
    pass


class ElementNotFoundError(RootBrowseError):
    """元素未找到"""
    pass


class RegionNotFoundError(RootBrowseError):
    """区域未找到"""
    pass


class TabNotFoundError(RootBrowseError):
    """标签页未找到"""
    pass


class OperationError(RootBrowseError):
    """操作失败"""
    pass


class StateFileError(RootBrowseError):
    """状态文件相关错误"""
    pass


class PageLoadError(RootBrowseError):
    """页面加载失败"""
    pass