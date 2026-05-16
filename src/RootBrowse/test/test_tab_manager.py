"""TabManager 标签页管理器测试"""

import pytest
from unittest.mock import MagicMock, patch

from rootbrowse.tab_manager import TabManager
from rootbrowse.exceptions import TabNotFoundError


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.new_tab = MagicMock()
    page.close_tab = MagicMock()
    page.switch_to_tab = MagicMock()
    return page


@pytest.fixture
def tab_manager(mock_page):
    """创建 TabManager 实例"""
    return TabManager(mock_page)


class TestTabManagerInit:
    """TabManager 初始化测试"""

    def test_init_empty_tabs(self, tab_manager):
        """测试初始化时标签页列表为空"""
        assert tab_manager._tabs == []

    def test_init_current_index_zero(self, tab_manager):
        """测试初始化时当前索引为 0"""
        assert tab_manager._current_index == 0


class TestNewTab:
    """new_tab 方法测试"""

    def test_new_tab_calls_page_new_tab(self, tab_manager, mock_page):
        """测试 new_tab 调用 page.new_tab"""
        tab_manager.new_tab('https://example.com')
        mock_page.new_tab.assert_called_once_with('https://example.com')

    def test_new_tab_returns_index(self, tab_manager, mock_page):
        """测试 new_tab 返回标签页索引"""
        index = tab_manager.new_tab('https://example.com')
        assert index == 0

    def test_new_tab_increments_index(self, tab_manager, mock_page):
        """测试 new_tab 正确增加标签页索引"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        assert tab_manager._current_index == 1
        assert len(tab_manager._tabs) == 2

    def test_new_tab_updates_tabs_list(self, tab_manager, mock_page):
        """测试 new_tab 更新内部标签页列表"""
        tab_manager.new_tab('https://example.com')
        assert len(tab_manager._tabs) == 1
        assert tab_manager._tabs[0]['url'] == 'https://example.com'


class TestCloseTab:
    """close_tab 方法测试"""

    def test_close_tab_raises_on_last_tab(self, tab_manager, mock_page):
        """测试关闭最后一个标签页时抛出异常"""
        tab_manager.new_tab('https://example.com')
        with pytest.raises(TabNotFoundError):
            tab_manager.close_tab()

    def test_close_tab_success(self, tab_manager, mock_page):
        """测试成功关闭标签页"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        tab_manager.close_tab(0)
        mock_page.close_tab.assert_called()

    def test_close_tab_switches_before_close(self, tab_manager, mock_page):
        """测试关闭非当前标签页前先切换"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        tab_manager.close_tab(0)
        mock_page.switch_to_tab.assert_called_with(0)

    def test_close_tab_raises_out_of_range(self, tab_manager, mock_page):
        """测试关闭越界索引抛出异常"""
        tab_manager.new_tab('https://example.com')
        with pytest.raises(TabNotFoundError):
            tab_manager.close_tab(99)


class TestSwitchToTab:
    """switch_to_tab 方法测试"""

    def test_switch_to_tab_success(self, tab_manager, mock_page):
        """测试成功切换标签页"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        tab_manager.switch_to_tab(1)
        mock_page.switch_to_tab.assert_called_with(1)
        assert tab_manager._current_index == 1

    def test_switch_to_tab_raises_out_of_range_negative(self, tab_manager, mock_page):
        """测试切换负索引抛出异常"""
        with pytest.raises(TabNotFoundError):
            tab_manager.switch_to_tab(-1)

    def test_switch_to_tab_raises_out_of_range_large(self, tab_manager, mock_page):
        """测试切换大索引抛出异常"""
        tab_manager.new_tab('https://example.com')
        with pytest.raises(TabNotFoundError):
            tab_manager.switch_to_tab(99)


class TestTabsCount:
    """tabs_count 方法测试"""

    def test_tabs_count_empty(self, tab_manager):
        """测试空状态时标签页数量为 0"""
        assert tab_manager.tabs_count() == 0

    def test_tabs_count_after_new_tab(self, tab_manager, mock_page):
        """测试新建标签页后数量正确"""
        tab_manager.new_tab('https://example.com')
        assert tab_manager.tabs_count() == 1

    def test_tabs_count_multiple(self, tab_manager, mock_page):
        """测试多个标签页数量正确"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        tab_manager.new_tab('https://github.com')
        assert tab_manager.tabs_count() == 3


class TestCurrentIndex:
    """current_index 方法测试"""

    def test_current_index_initially_zero(self, tab_manager):
        """测试初始当前索引为 0"""
        assert tab_manager.current_index() == 0

    def test_current_index_after_switch(self, tab_manager, mock_page):
        """测试切换后当前索引正确"""
        tab_manager.new_tab('https://example.com')
        tab_manager.new_tab('https://google.com')
        tab_manager.switch_to_tab(1)
        assert tab_manager.current_index() == 1
