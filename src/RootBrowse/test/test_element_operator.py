"""ElementOperator 元素操作器测试"""

import pytest
from unittest.mock import MagicMock

from rootbrowse.element_operator import ElementOperator
from rootbrowse.types import Element
from rootbrowse.exceptions import ElementNotFoundError


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.ele = MagicMock()
    return page


@pytest.fixture
def element_map():
    """创建模拟的元素映射"""
    return {
        "r1": Element(ref="r1", tag="a", role="link", text="链接1", xpath="/html/body/a[1]", attrs={"href": "/page1"}),
        "r2": Element(ref="r2", tag="button", role="button", text="按钮", xpath="/html/body/button[1]", attrs={}),
    }


@pytest.fixture
def element_operator(mock_page, element_map):
    """创建 ElementOperator 实例"""
    return ElementOperator(mock_page, element_map)


class TestElementOperatorInit:
    """ElementOperator 初始化测试"""

    def test_init_with_page(self, element_operator, mock_page):
        """测试用 page 初始化"""
        assert element_operator._page is mock_page

    def test_init_with_element_map(self, element_operator, element_map):
        """测试用 element_map 初始化"""
        assert element_operator._element_map is element_map


class TestRefToXPath:
    """ref_to_xpath 方法测试"""

    def test_ref_to_xpath_success(self, element_operator):
        """测试 ref 转 xpath 成功"""
        xpath = element_operator.ref_to_xpath("r1")
        assert xpath == "/html/body/a[1]"

    def test_ref_to_xpath_raises_not_found(self, element_operator):
        """测试 ref 不存在时抛出异常"""
        with pytest.raises(ElementNotFoundError):
            element_operator.ref_to_xpath("r99")

    def test_ref_to_xpath_r2(self, element_operator):
        """测试 r2 转 xpath"""
        xpath = element_operator.ref_to_xpath("r2")
        assert xpath == "/html/body/button[1]"


class TestResolveLocator:
    """_resolve_locator 方法测试"""

    def test_resolve_locator_with_ref_type(self, element_operator, mock_page):
        """测试指定 ref 类型"""
        result = element_operator._resolve_locator("r1", "ref")
        assert result == "/html/body/a[1]"

    def test_resolve_locator_with_xpath_type(self, element_operator):
        """测试指定 xpath 类型直接返回"""
        xpath = "//div/button"
        result = element_operator._resolve_locator(xpath, "xpath")
        assert result == xpath

    def test_resolve_locator_auto_ref(self, element_operator, mock_page):
        """测试自动识别 ref"""
        result = element_operator._resolve_locator("r1")
        assert result == "/html/body/a[1]"

    def test_resolve_locator_auto_xpath(self, element_operator):
        """测试自动识别 xpath"""
        xpath = "//div/span"
        result = element_operator._resolve_locator(xpath)
        assert result == xpath


class TestIsRef:
    """_is_ref 方法测试"""

    def test_is_ref_valid(self, element_operator):
        """测试有效的 ref 格式"""
        assert element_operator._is_ref("r1") is True
        assert element_operator._is_ref("r99") is True
        assert element_operator._is_ref("r12345") is True

    def test_is_ref_invalid(self, element_operator):
        """测试无效的 ref 格式"""
        assert element_operator._is_ref("x1") is False
        assert element_operator._is_ref("ref1") is False
        assert element_operator._is_ref("1") is False
        assert element_operator._is_ref("") is False
        assert element_operator._is_ref("r") is False
        assert element_operator._is_ref("rabc") is False


class TestClick:
    """click 方法测试"""

    def test_click_by_ref_success(self, element_operator, mock_page):
        """测试通过 ref 点击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.click("r1", "ref")
        assert result.success is True
        mock_ele.click.assert_called_once()

    def test_click_by_xpath_success(self, element_operator, mock_page):
        """测试通过 xpath 点击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.click("//div/button", "xpath")
        assert result.success is True

    def test_click_failure(self, element_operator, mock_page):
        """测试点击失败"""
        mock_page.ele.side_effect = Exception("element not found")

        result = element_operator.click("r1")
        assert result.success is False
        assert result.error is not None


class TestInputByRef:
    """input_by_ref 方法测试"""

    def test_input_by_ref_success(self, element_operator, mock_page):
        """测试通过 ref 输入成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.input_by_ref("r1", "hello world")
        assert result.success is True
        mock_ele.input.assert_called_once_with("hello world")

    def test_input_by_ref_with_clear(self, element_operator, mock_page):
        """测试先清空再输入"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.input_by_ref("r1", "new text", clear=True)
        assert result.success is True
        mock_ele.clear.assert_called_once()
        mock_ele.input.assert_called_once_with("new text")

    def test_input_by_ref_failure(self, element_operator, mock_page):
        """测试输入失败"""
        mock_page.ele.side_effect = Exception("element not found")

        result = element_operator.input_by_ref("r1", "text")
        assert result.success is False


class TestHover:
    """hover 方法测试"""

    def test_hover_success(self, element_operator, mock_page):
        """测试悬停成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.hover("r1")
        assert result.success is True
        mock_ele.hover.assert_called_once()

    def test_hover_failure(self, element_operator, mock_page):
        """测试悬停失败"""
        mock_page.ele.side_effect = Exception("hover failed")

        result = element_operator.hover("r1")
        assert result.success is False


class TestDoubleClick:
    """double_click 方法测试"""

    def test_double_click_success(self, element_operator, mock_page):
        """测试双击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.double_click("r1")
        assert result.success is True
        mock_ele.double_click.assert_called_once()


class TestRightClick:
    """right_click 方法测试"""

    def test_right_click_success(self, element_operator, mock_page):
        """测试右键点击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.right_click("r1")
        assert result.success is True
        mock_ele.right_click.assert_called_once()


class TestSubmit:
    """submit 方法测试"""

    def test_submit_success(self, element_operator, mock_page):
        """测试提交表单成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.submit("r1")
        assert result.success is True
        mock_ele.submit.assert_called_once()


class TestClear:
    """clear 方法测试"""

    def test_clear_success(self, element_operator, mock_page):
        """测试清空输入框成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.clear("r1")
        assert result.success is True
        mock_ele.clear.assert_called_once()


class TestSendEnter:
    """send_enter 方法测试"""

    def test_send_enter(self, element_operator, mock_page):
        """测试发送回车键"""
        element_operator.send_enter()
        mock_page.run_js.assert_called_once()
        mock_page.wait.assert_called_once()
