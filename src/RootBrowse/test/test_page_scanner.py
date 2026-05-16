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
    page.get_ele_tree = MagicMock(return_value={})
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

    def test_init_empty_element_map(self, page_scanner):
        """测试初始化时元素映射为空"""
        assert page_scanner._element_map == {}

    def test_init_empty_regions(self, page_scanner):
        """测试初始化时区域列表为空"""
        assert page_scanner._regions == []


class TestScanPage:
    """_scan_page 方法测试"""

    def test_scan_page_clears_existing_data(self, page_scanner, mock_page):
        """测试扫描前清空现有数据"""
        page_scanner._element_map["r1"] = Element(ref="r1", tag="a", role="link", text="old", xpath="//a", attrs={})
        page_scanner._regions = [Region(id="old_region", label="旧区域", node_count=1)]

        page_scanner._scan_page()

        assert page_scanner._element_map == {}
        # _scan_page 会重新填充 _regions 为默认的 "main" 区域
        assert page_scanner._regions[0].id == "main"

    def test_scan_page_with_clickable_elements(self, page_scanner, mock_page):
        """测试扫描可交互元素"""
        mock_ele1 = MagicMock()
        mock_ele1.tag = "a"
        mock_ele1.attr.return_value = "link"
        mock_ele1.text = "链接"
        mock_ele1.xpath = "/html/body/a[1]"
        mock_ele1.attrs = {"href": "/page1"}

        mock_ele2 = MagicMock()
        mock_ele2.tag = "button"
        mock_ele2.attr.return_value = "button"
        mock_ele2.text = "按钮"
        mock_ele2.xpath = "/html/body/button[1]"
        mock_ele2.attrs = {}

        # 新实现：eles 被每个 tag 调用一次
        def eles_side_effect(selector, timeout=None):
            if selector == 'tag:a':
                return [mock_ele1]
            elif selector == 'tag:button':
                return [mock_ele2]
            return []
        mock_page.eles.side_effect = eles_side_effect

        page_scanner._scan_page()

        assert len(page_scanner._element_map) == 2
        assert "r1" in page_scanner._element_map
        assert "r2" in page_scanner._element_map


class TestGetRegions:
    """get_regions 方法测试"""

    def test_get_regions_calls_scan(self, page_scanner, mock_page):
        """测试 get_regions 调用扫描"""
        mock_page.eles.return_value = []
        page_scanner.get_regions()
        mock_page.eles.assert_called()

    def test_get_regions_returns_list(self, page_scanner, mock_page):
        """测试返回区域列表"""
        mock_page.eles.return_value = []
        regions = page_scanner.get_regions()
        assert isinstance(regions, list)


class TestGetRegionSummary:
    """get_region_summary 方法测试"""

    def test_get_region_summary_raises_not_found(self, page_scanner, mock_page):
        """测试区域不存在时抛出异常"""
        mock_page.eles.return_value = []
        page_scanner._scan_page()

        with pytest.raises(RegionNotFoundError):
            page_scanner.get_region_summary("nonexistent")

    def test_get_region_summary_success(self, page_scanner, mock_page):
        """测试获取区域摘要成功"""
        mock_ele1 = MagicMock()
        mock_ele1.tag = "a"
        mock_ele1.attr.return_value = "link"
        mock_ele1.text = "链接1"
        mock_ele1.xpath = "/html/body/a[1]"
        mock_ele1.attrs = {"href": "/page1"}

        mock_ele2 = MagicMock()
        mock_ele2.tag = "button"
        mock_ele2.attr.return_value = "button"
        mock_ele2.text = "按钮"
        mock_ele2.xpath = "/html/body/button[1]"
        mock_ele2.attrs = {}

        def eles_side_effect(selector, timeout=None):
            if selector == 'tag:a':
                return [mock_ele1]
            elif selector == 'tag:button':
                return [mock_ele2]
            return []
        mock_page.eles.side_effect = eles_side_effect
        page_scanner._scan_page()

        summary = page_scanner.get_region_summary("main")
        assert summary.count == 2
        assert "a" in summary.tag_counts
        assert "button" in summary.tag_counts


class TestMatchElement:
    """match_element 方法测试"""

    def test_match_element_with_tag_filter(self, page_scanner, mock_page):
        """测试按标签筛选元素"""
        mock_ele1 = MagicMock()
        mock_ele1.tag = "a"
        mock_ele1.attr.return_value = "link"
        mock_ele1.text = "链接"
        mock_ele1.xpath = "/html/body/a[1]"
        mock_ele1.attrs = {"href": "/page1"}

        mock_ele2 = MagicMock()
        mock_ele2.tag = "button"
        mock_ele2.attr.return_value = "button"
        mock_ele2.text = "按钮"
        mock_ele2.xpath = "/html/body/button[1]"
        mock_ele2.attrs = {}

        def eles_side_effect(selector, timeout=None):
            if selector == 'tag:a':
                return [mock_ele1]
            elif selector == 'tag:button':
                return [mock_ele2]
            return []
        mock_page.eles.side_effect = eles_side_effect
        page_scanner._scan_page()

        results = page_scanner.match_element(tag="a")
        assert len(results) == 1
        assert results[0].ref == "r1"

    def test_match_element_with_text_contains(self, page_scanner, mock_page):
        """测试按文字包含筛选"""
        mock_ele1 = MagicMock()
        mock_ele1.tag = "a"
        mock_ele1.attr.return_value = "link"
        mock_ele1.text = "Python 入门"
        mock_ele1.xpath = "/html/body/a[1]"
        mock_ele1.attrs = {"href": "/python"}

        mock_ele2 = MagicMock()
        mock_ele2.tag = "a"
        mock_ele2.attr.return_value = "link"
        mock_ele2.text = "Java 入门"
        mock_ele2.xpath = "/html/body/a[2]"
        mock_ele2.attrs = {"href": "/java"}

        def eles_side_effect(selector, timeout=None):
            if selector == 'tag:a':
                return [mock_ele1, mock_ele2]
            return []
        mock_page.eles.side_effect = eles_side_effect
        page_scanner._scan_page()

        results = page_scanner.match_element(text_contains="Python")
        assert len(results) == 1
        assert results[0].text == "Python 入门"

    def test_match_element_limit(self, page_scanner, mock_page):
        """测试分页限制"""
        for i in range(5):
            mock_ele = MagicMock()
            mock_ele.tag = "a"
            mock_ele.attr.return_value = "link"
            mock_ele.text = f"链接{i}"
            mock_ele.xpath = f"/html/body/a[{i}]"
            mock_ele.attrs = {}
            mock_page.eles.return_value = []

        mock_page.eles.return_value = []
        page_scanner._scan_page()

        results = page_scanner.match_element(limit=3)
        assert len(results) <= 3


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

        mock_page.eles.return_value = [mock_ele]
        page_scanner._scan_page()

        ele = page_scanner.get_element("r1")
        assert ele.ref == "r1"
        assert ele.tag == "a"

    def test_get_element_not_found(self, page_scanner, mock_page):
        """测试元素不存在时抛出异常"""
        mock_page.eles.return_value = []
        page_scanner._scan_page()

        with pytest.raises(ElementNotFoundError):
            page_scanner.get_element("r999")


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
        page_scanner._scan_page()

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
        page_scanner._scan_page()

        result = page_scanner.find_element(by="role", value="button")
        assert result is not None
        assert result.role == "button"

    def test_find_element_not_found(self, page_scanner, mock_page):
        """测试查找元素不存在"""
        mock_page.ele.return_value = None
        page_scanner._scan_page()

        result = page_scanner.find_element(by="xpath", value="//nonexistent")
        assert result is None


class TestGetAttrsPreview:
    """_get_attrs_preview 方法测试"""

    def test_get_attrs_preview(self, page_scanner):
        """测试获取属性预览"""
        ele = Element(
            ref="r1",
            tag="a",
            role="link",
            text="链接",
            xpath="//a",
            attrs={"href": "/page1", "title": "标题", "class": "link", "id": "main"}
        )

        preview = page_scanner._get_attrs_preview(ele)
        assert "href" in preview
        assert preview["href"] == "/page1"
        assert preview.get("title") == "标题"
        assert "id" not in preview
        assert "class" not in preview
