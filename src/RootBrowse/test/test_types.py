"""types 数据类测试"""

import pytest
from dataclasses import dataclass, field

from rootbrowse.types import Region, Element, RegionSummary, ElementPreview, OperationResult


class TestRegion:
    """Region 数据类测试"""

    def test_region_creation(self):
        """测试 Region 创建"""
        region = Region(id="main", label="主内容", node_count=100)
        assert region.id == "main"
        assert region.label == "主内容"
        assert region.node_count == 100


class TestElement:
    """Element 数据类测试"""

    def test_element_creation(self):
        """测试 Element 创建"""
        ele = Element(
            ref="r1",
            tag="a",
            role="link",
            text="点击这里",
            xpath="/html/body/a[1]",
            attrs={"href": "/page1"}
        )
        assert ele.ref == "r1"
        assert ele.tag == "a"
        assert ele.role == "link"
        assert ele.text == "点击这里"
        assert ele.xpath == "/html/body/a[1]"
        assert ele.attrs == {"href": "/page1"}

    def test_element_default_attrs(self):
        """测试 Element 默认 attrs"""
        ele = Element(ref="r2", tag="button", role="button", text="提交", xpath="//button")
        assert ele.attrs == {}


class TestRegionSummary:
    """RegionSummary 数据类测试"""

    def test_region_summary_creation(self):
        """测试 RegionSummary 创建"""
        summary = RegionSummary(
            count=50,
            tag_counts={"a": 30, "button": 20},
            role_counts={"link": 30, "button": 20},
            text_preview=[{"tag": "a", "text": "标题", "ref": "r1"}]
        )
        assert summary.count == 50
        assert summary.tag_counts == {"a": 30, "button": 20}
        assert summary.role_counts == {"link": 30, "button": 20}
        assert len(summary.text_preview) == 1


class TestElementPreview:
    """ElementPreview 数据类测试"""

    def test_element_preview_creation(self):
        """测试 ElementPreview 创建"""
        preview = ElementPreview(
            ref="r5",
            text="搜索",
            attrs_preview={"type": "submit"}
        )
        assert preview.ref == "r5"
        assert preview.text == "搜索"
        assert preview.attrs_preview == {"type": "submit"}


class TestOperationResult:
    """OperationResult 数据类测试"""

    def test_operation_result_success(self):
        """测试成功操作结果"""
        result = OperationResult(success=True)
        assert result.success is True
        assert result.error is None
        assert result.new_url is None

    def test_operation_result_failure(self):
        """测试失败操作结果"""
        result = OperationResult(success=False, error="元素不存在")
        assert result.success is False
        assert result.error == "元素不存在"

    def test_operation_result_with_url(self):
        """测试带新 URL 的操作结果"""
        result = OperationResult(success=True, new_url="https://example.com/page2")
        assert result.success is True
        assert result.new_url == "https://example.com/page2"
