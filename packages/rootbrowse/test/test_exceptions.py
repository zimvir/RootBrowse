"""exceptions 异常测试"""

import pytest

from rootbrowse.exceptions import (
    RootBrowseError,
    BrowserError,
    ElementNotFoundError,
    RegionNotFoundError,
    TabNotFoundError,
    OperationError,
    StateFileError,
    PageLoadError,
)


class TestRootBrowseError:
    """RootBrowse 基异常测试"""

    def test_raise_base_error(self):
        """测试抛出基异常"""
        with pytest.raises(RootBrowseError):
            raise RootBrowseError("base error")

    def test_base_error_message(self):
        """测试基异常消息"""
        msg = "test message"
        try:
            raise RootBrowseError(msg)
        except RootBrowseError as e:
            assert str(e) == msg


class TestBrowserError:
    """BrowserError 测试"""

    def test_browser_error_inherits_from_base(self):
        """测试 BrowserError 继承自 RootBrowseError"""
        assert issubclass(BrowserError, RootBrowseError)

    def test_raise_browser_error(self):
        """测试抛出 BrowserError"""
        with pytest.raises(BrowserError):
            raise BrowserError("browser failed")


class TestElementNotFoundError:
    """ElementNotFoundError 测试"""

    def test_element_not_found_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(ElementNotFoundError, RootBrowseError)

    def test_raise_element_not_found_error(self):
        """测试抛出 ElementNotFoundError"""
        with pytest.raises(ElementNotFoundError):
            raise ElementNotFoundError("r123")


class TestRegionNotFoundError:
    """RegionNotFoundError 测试"""

    def test_region_not_found_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(RegionNotFoundError, RootBrowseError)

    def test_raise_region_not_found_error(self):
        """测试抛出 RegionNotFoundError"""
        with pytest.raises(RegionNotFoundError):
            raise RegionNotFoundError("main")


class TestTabNotFoundError:
    """TabNotFoundError 测试"""

    def test_tab_not_found_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(TabNotFoundError, RootBrowseError)

    def test_raise_tab_not_found_error(self):
        """测试抛出 TabNotFoundError"""
        with pytest.raises(TabNotFoundError):
            raise TabNotFoundError("tab index out of range")

    def test_tab_not_found_error_with_index(self):
        """测试带索引的错误消息"""
        try:
            raise TabNotFoundError("Tab index out of range: 99")
        except TabNotFoundError as e:
            assert "99" in str(e)


class TestOperationError:
    """OperationError 测试"""

    def test_operation_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(OperationError, RootBrowseError)

    def test_raise_operation_error(self):
        """测试抛出 OperationError"""
        with pytest.raises(OperationError):
            raise OperationError("click failed")


class TestStateFileError:
    """StateFileError 测试"""

    def test_state_file_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(StateFileError, RootBrowseError)

    def test_raise_state_file_error(self):
        """测试抛出 StateFileError"""
        with pytest.raises(StateFileError):
            raise StateFileError("failed to save state")


class TestPageLoadError:
    """PageLoadError 测试"""

    def test_page_load_error_inherits(self):
        """测试继承自 RootBrowseError"""
        assert issubclass(PageLoadError, RootBrowseError)

    def test_raise_page_load_error(self):
        """测试抛出 PageLoadError"""
        with pytest.raises(PageLoadError):
            raise PageLoadError("timeout")


class TestExceptionHierarchy:
    """异常层次结构测试"""

    def test_all_exceptions_inherit_from_base(self):
        """测试所有异常都继承自 RootBrowseError"""
        exceptions = [
            BrowserError,
            ElementNotFoundError,
            RegionNotFoundError,
            TabNotFoundError,
            OperationError,
            StateFileError,
            PageLoadError,
        ]
        for exc in exceptions:
            assert issubclass(exc, RootBrowseError)

    def test_all_exceptions_can_be_caught_by_base(self):
        """测试所有异常都能被基类捕获"""
        exceptions = [
            BrowserError,
            ElementNotFoundError,
            RegionNotFoundError,
            TabNotFoundError,
            OperationError,
            StateFileError,
            PageLoadError,
        ]
        for exc in exceptions:
            with pytest.raises(RootBrowseError):
                raise exc("test")
