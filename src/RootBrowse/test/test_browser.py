"""Browse 浏览器主入口测试"""

import pytest
from unittest.mock import MagicMock, patch

from rootbrowse.browser import Browser
from rootbrowse.exceptions import PageLoadError, StateFileError


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.get = MagicMock()
    page.title = "Test Page"
    page.get_screenshot = MagicMock()
    page.screenshot = MagicMock(return_value="base64_screenshot_data")
    page.quit = MagicMock()
    return page


@pytest.fixture
def browser(mock_page):
    """创建 Browser 实例"""
    return Browser(mock_page)


class TestBrowserInit:
    """Browser 初始化测试"""

    def test_init_with_page(self, browser, mock_page):
        """测试用 page 初始化"""
        assert browser._page is mock_page

    def test_init_closed_false(self, browser):
        """测试初始化时 closed 为 False"""
        assert browser._closed is False

    def test_tabs_property(self, browser):
        """测试 tabs 属性"""
        assert browser.tabs is not None

    def test_page_property(self, browser):
        """测试 page 属性"""
        assert browser.page is not None

    def test_act_property(self, browser):
        """测试 act 属性"""
        assert browser.act is not None


class TestGet:
    """get 方法测试"""

    def test_get_success(self, browser, mock_page):
        """测试成功打开 URL"""
        result = browser.get('https://example.com')
        mock_page.get.assert_called_once_with('https://example.com', timeout=30)
        assert result['url'] == 'https://example.com'
        assert result['title'] == 'Test Page'

    def test_get_with_custom_timeout(self, browser, mock_page):
        """测试带自定义超时"""
        browser.get('https://example.com', timeout=60)
        mock_page.get.assert_called_once_with('https://example.com', timeout=60)

    def test_get_failure(self, browser, mock_page):
        """测试打开 URL 失败"""
        mock_page.get.side_effect = Exception("network error")
        with pytest.raises(PageLoadError):
            browser.get('https://example.com')


class TestScreenshot:
    """screenshot 方法测试"""

    def test_screenshot_to_file(self, browser, mock_page):
        """测试保存截图到文件"""
        result = browser.screenshot(path="/tmp/screenshot.png")
        mock_page.get_screenshot.assert_called_once_with(path="/tmp/screenshot.png")
        assert result == "/tmp/screenshot.png"

    def test_screenshot_returns_base64(self, browser, mock_page):
        """测试返回 base64 字符串"""
        result = browser.screenshot()
        mock_page.screenshot.assert_called_once()
        assert result == "base64_screenshot_data"


class TestSaveState:
    """save_state 方法测试"""

    def test_save_state_calls_set_cookies(self, browser, mock_page):
        """测试保存状态调用 cookies 方法"""
        browser.save_state('/tmp/state.json')
        mock_page.set.cookies.assert_called_once()

    def test_save_state_failure(self, browser, mock_page):
        """测试保存状态失败"""
        mock_page.set.cookies.side_effect = Exception("permission denied")
        with pytest.raises(StateFileError):
            browser.save_state('/tmp/state.json')


class TestLoadState:
    """load_state 方法测试"""

    def test_load_state_calls_set_cookies(self, browser, mock_page):
        """测试恢复状态调用 cookies 方法"""
        browser.load_state('/tmp/state.json')
        mock_page.set.cookies.assert_called_once()

    def test_load_state_failure(self, browser, mock_page):
        """测试恢复状态失败"""
        mock_page.set.cookies.side_effect = Exception("file not found")
        with pytest.raises(StateFileError):
            browser.load_state('/tmp/state.json')


class TestClose:
    """close 方法测试"""

    def test_close_calls_page_quit(self, browser, mock_page):
        """测试 close 调用 page.quit"""
        browser.close()
        mock_page.quit.assert_called_once()

    def test_close_sets_closed_flag(self, browser, mock_page):
        """测试 close 设置 closed 标志"""
        browser.close()
        assert browser._closed is True

    def test_close_idempotent(self, browser, mock_page):
        """测试 close 是幂等的（多次调用只执行一次）"""
        browser.close()
        browser.close()
        mock_page.quit.assert_called_once()
