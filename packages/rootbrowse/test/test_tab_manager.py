"""TabManager 标签页管理器测试"""

import pytest
from unittest.mock import MagicMock

from rootbrowse.tab_manager import TabManager
from rootbrowse.exceptions import TabNotFoundError


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.tab_ids = ['tab-1']  # property (list)
    page.tab_id = 'tab-1'     # property (str)
    page.new_tab = MagicMock()
    page.close = MagicMock()
    page.activate_tab = MagicMock()
    return page


@pytest.fixture
def tab_manager(mock_page):
    """创建 TabManager 实例"""
    tm = TabManager.__new__(TabManager)
    tm._page = mock_page
    return tm


class TestTabManagerInit:
    """TabManager 初始化测试"""

    def test_tabs_property_returns_tab_ids(self, tab_manager, mock_page):
        """测试 _tabs 属性实时返回 page.tab_ids"""
        mock_page.tab_ids = ['tab-1', 'tab-2']
        assert tab_manager._tabs == ['tab-1', 'tab-2']


class TestNewTab:
    """new_tab 方法测试"""

    def test_new_tab_calls_page_new_tab(self, tab_manager, mock_page):
        """测试 new_tab 调用 page.new_tab"""
        tab_manager.new_tab('https://example.com')
        mock_page.new_tab.assert_called_once_with('https://example.com')


class TestCloseTab:
    """close_tab 方法测试"""

    def test_close_tab_raises_on_last_tab(self, tab_manager, mock_page):
        """测试关闭最后一个标签页时抛出异常"""
        mock_page.tab_ids = ['tab-1']
        with pytest.raises(TabNotFoundError):
            tab_manager.close_tab()

    def test_close_tab_success(self, tab_manager, mock_page):
        """测试成功关闭标签页"""
        mock_page.tab_ids = ['tab-1', 'tab-2']
        tab_manager.close_tab(0)
        mock_page.close.assert_called()

    def test_close_tab_switches_before_close(self, tab_manager, mock_page):
        """测试关闭非当前标签页前先切换"""
        mock_page.tab_ids = ['tab-1', 'tab-2']
        mock_page.tab_id = 'tab-2'
        tab_manager.close_tab(0)
        mock_page.activate_tab.assert_called_with(0)

    def test_close_tab_raises_out_of_range(self, tab_manager, mock_page):
        """测试关闭越界索引抛出异常"""
        mock_page.tab_ids = ['tab-1']
        with pytest.raises(TabNotFoundError):
            tab_manager.close_tab(99)


class TestSwitchToTab:
    """switch_to_tab 方法测试"""

    def test_switch_to_tab_success(self, tab_manager, mock_page):
        """测试成功切换标签页"""
        mock_page.tab_ids = ['tab-1', 'tab-2']
        tab_manager.switch_to_tab(1)
        mock_page.activate_tab.assert_called_with(1)

    def test_switch_to_tab_raises_out_of_range_negative(self, tab_manager, mock_page):
        """测试切换负索引抛出异常"""
        mock_page.tab_ids = ['tab-1']
        with pytest.raises(TabNotFoundError):
            tab_manager.switch_to_tab(-1)

    def test_switch_to_tab_raises_out_of_range_large(self, tab_manager, mock_page):
        """测试切换大索引抛出异常"""
        mock_page.tab_ids = ['tab-1']
        with pytest.raises(TabNotFoundError):
            tab_manager.switch_to_tab(99)


class TestTabsCount:
    """tabs_count 方法测试"""

    def test_tabs_count_empty(self, tab_manager, mock_page):
        """测试空状态时标签页数量为 0"""
        mock_page.tab_ids = []
        assert tab_manager.tabs_count() == 0

    def test_tabs_count_after_new_tab(self, tab_manager, mock_page):
        """测试新建标签页后数量正确"""
        mock_page.tab_ids = ['tab-1']
        assert tab_manager.tabs_count() == 1

    def test_tabs_count_multiple(self, tab_manager, mock_page):
        """测试多个标签页数量正确"""
        mock_page.tab_ids = ['tab-1', 'tab-2', 'tab-3']
        assert tab_manager.tabs_count() == 3


class TestCurrentIndex:
    """current_index 方法测试"""

    def test_current_index_returns_correct(self, tab_manager, mock_page):
        """测试当前索引正确"""
        mock_page.tab_ids = ['tab-1', 'tab-2']
        mock_page.tab_id = 'tab-2'
        assert tab_manager.current_index() == 1
