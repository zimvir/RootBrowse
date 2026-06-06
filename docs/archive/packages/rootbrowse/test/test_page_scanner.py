"""PageScanner 页面扫描器测试"""

import pytest
from unittest.mock import MagicMock

from rootbrowse.page_scanner import PageScanner
from rootbrowse.types import Element, Region
from rootbrowse.exceptions import ElementNotFoundError, RegionNotFoundError


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.run_js = MagicMock(return_value=[])
    page.ele = MagicMock()
    page.eles = MagicMock(return_value=[])
    return page


@pytest.fixture
def page_scanner(mock_page):
    """创建 PageScanner 实例"""
    return PageScanner(mock_page)


class TestPageScannerInit:
    """PageScanner 初始化测试"""

    def test_init_with_page(self, page_scanner, mock_page):
        """测试用 page 初始化"""
        assert page_scanner._page is mock_page

    def test_init_empty_regions(self, page_scanner):
        """测试初始化时区域列表为空"""
        assert page_scanner._regions == []


class TestGetRegions:
    """get_regions 方法测试"""

    def test_get_regions_empty_body(self, page_scanner, mock_page):
        """测试 body 为空时返回默认区域"""
        mock_page.run_js.return_value = []

        regions = page_scanner.get_regions()
        assert len(regions) == 1
        assert regions[0].xpath == "/html/body"
        assert regions[0].label == "主内容"

    def test_get_regions_with_children(self, page_scanner, mock_page):
        """测试 body 有子元素时正确划分区域"""
        mock_page.run_js.return_value = [
            {'xpath': '/html/body/div[1]', 'label': '区块'}
        ]

        regions = page_scanner.get_regions()
        assert len(regions) == 1
        assert regions[0].xpath == "/html/body/div[1]"


class TestGetRegionSummary:
    """get_region_summary 方法测试"""

    def test_get_region_summary_nonexistent(self, page_scanner, mock_page):
        """测试区域不存在时抛出异常"""
        mock_body = MagicMock()
        mock_body.tag = 'body'
        mock_body.children.return_value = []
        mock_page.ele.return_value = mock_body
        page_scanner.get_regions()

        with pytest.raises(RegionNotFoundError):
            page_scanner.get_region_summary("/html/body/nonexistent")

    def test_get_region_summary_success(self, page_scanner, mock_page):
        """测试获取区域摘要成功"""
        mock_page.run_js.return_value = [
            {'xpath': '/html/body/div[1]', 'label': '区块'}
        ]

        page_scanner.get_regions()
        # get_region_summary 内部也用 run_js
        summary = page_scanner.get_region_summary("/html/body/div[1]")

        assert summary.count >= 0


class TestMatchElement:
    """match_element 方法测试"""

    def test_match_element_empty_regions(self, page_scanner, mock_page):
        """测试无区域时返回空"""
        mock_page.run_js.return_value = []

        page_scanner.get_regions()
        results = page_scanner.match_element(tag="a")
        assert results == []


class TestGetElement:
    """get_element 方法测试"""

    def test_get_element_success(self, page_scanner, mock_page):
        """测试获取元素成功"""
        mock_ele = MagicMock()
        mock_ele.tag = "a"
        mock_ele.attr.return_value = "link"
        mock_ele.text = "链接"
        mock_ele.xpath = "/html/body/a[1]"
        mock_ele.attrs = {"href": "/page1"}

        mock_page.ele.return_value = mock_ele

        ele = page_scanner.get_element("/html/body/a[1]")
        assert ele.tag == "a"
        assert ele.text == "链接"
        assert ele.xpath == "/html/body/a[1]"

    def test_get_element_not_found(self, page_scanner, mock_page):
        """测试元素不存在时抛出异常"""
        mock_page.ele.return_value = None

        with pytest.raises(ElementNotFoundError):
            page_scanner.get_element("/html/body/nonexistent")


class TestFindElement:
    """find_element 方法测试"""

    def test_find_element_by_xpath(self, page_scanner, mock_page):
        """测试按 xpath 查找元素"""
        mock_ele = MagicMock()
        mock_ele.tag = "div"
        mock_ele.attr.return_value = None
        mock_ele.text = ""
        mock_ele.xpath = "/html/body/div[1]"
        mock_ele.attrs = {}

        mock_page.ele.return_value = mock_ele

        result = page_scanner.find_element(by="xpath", value="/html/body/div[1]")
        assert result is not None
        assert result.tag == "div"

    def test_find_element_by_role(self, page_scanner, mock_page):
        """测试按 role 查找元素"""
        mock_ele = MagicMock()
        mock_ele.tag = "button"
        mock_ele.attr.return_value = "button"
        mock_ele.text = "提交"
        mock_ele.xpath = "/html/body/button[1]"
        mock_ele.attrs = {}

        mock_page.ele.return_value = mock_ele

        result = page_scanner.find_element(by="role", value="button")
        assert result is not None
        assert result.role == "button"

    def test_find_element_not_found(self, page_scanner, mock_page):
        """测试查找元素不存在"""
        mock_page.ele.return_value = None

        result = page_scanner.find_element(by="xpath", value="//nonexistent")
        assert result is None


class TestClearCache:
    """clear_cache 方法测试"""

    def test_clear_cache(self, page_scanner, mock_page):
        """测试清空缓存"""
        mock_body = MagicMock()
        mock_body.tag = 'body'
        mock_body.children.return_value = []
        mock_page.ele.return_value = mock_body

        page_scanner.get_regions()
        assert len(page_scanner._regions) > 0

        page_scanner.clear_cache()
        assert page_scanner._regions == []