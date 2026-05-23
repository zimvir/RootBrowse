"""ElementOperator 元素操作器测试"""

import pytest
from unittest.mock import MagicMock

from rootbrowse.element_operator import ElementOperator


@pytest.fixture
def mock_page():
    """创建模拟的 DrissionPage"""
    page = MagicMock()
    page.ele = MagicMock()
    return page


@pytest.fixture
def element_operator(mock_page):
    """创建 ElementOperator 实例"""
    return ElementOperator(mock_page)


class TestElementOperatorInit:
    """ElementOperator 初始化测试"""

    def test_init_with_page(self, element_operator, mock_page):
        """测试用 page 初始化"""
        assert element_operator._page is mock_page


class TestClick:
    """click 方法测试"""

    def test_click_success(self, element_operator, mock_page):
        """测试点击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.click("/html/body/button[1]")
        assert result.success is True
        mock_ele.click.assert_called_once()

    def test_click_failure(self, element_operator, mock_page):
        """测试点击失败"""
        mock_page.ele.side_effect = Exception("element not found")

        result = element_operator.click("/html/body/nonexistent")
        assert result.success is False
        assert result.error is not None


class TestInputByXPath:
    """input_by_xpath 方法测试"""

    def test_input_success(self, element_operator, mock_page):
        """测试输入成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.input_by_xpath("/html/body/input[1]", "hello world")
        assert result.success is True
        mock_ele.input.assert_called_once_with("hello world")

    def test_input_with_clear(self, element_operator, mock_page):
        """测试先清空再输入"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.input_by_xpath("/html/body/input[1]", "new text", clear=True)
        assert result.success is True
        mock_ele.clear.assert_called_once()
        mock_ele.input.assert_called_once_with("new text")

    def test_input_failure(self, element_operator, mock_page):
        """测试输入失败"""
        mock_page.ele.side_effect = Exception("element not found")

        result = element_operator.input_by_xpath("/html/body/nonexistent", "text")
        assert result.success is False


class TestHover:
    """hover 方法测试"""

    def test_hover_success(self, element_operator, mock_page):
        """测试悬停成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.hover("/html/body/div[1]")
        assert result.success is True
        mock_ele.hover.assert_called_once()

    def test_hover_failure(self, element_operator, mock_page):
        """测试悬停失败"""
        mock_page.ele.side_effect = Exception("hover failed")

        result = element_operator.hover("/html/body/nonexistent")
        assert result.success is False


class TestDoubleClick:
    """double_click 方法测试"""

    def test_double_click_success(self, element_operator, mock_page):
        """测试双击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.double_click("/html/body/div[1]")
        assert result.success is True
        mock_ele.double_click.assert_called_once()


class TestRightClick:
    """right_click 方法测试"""

    def test_right_click_success(self, element_operator, mock_page):
        """测试右键点击成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.right_click("/html/body/div[1]")
        assert result.success is True
        mock_ele.right_click.assert_called_once()


class TestSubmit:
    """submit 方法测试"""

    def test_submit_success(self, element_operator, mock_page):
        """测试提交表单成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.submit("/html/body/form[1]")
        assert result.success is True
        mock_ele.submit.assert_called_once()


class TestClear:
    """clear 方法测试"""

    def test_clear_success(self, element_operator, mock_page):
        """测试清空输入框成功"""
        mock_ele = MagicMock()
        mock_page.ele.return_value = mock_ele

        result = element_operator.clear("/html/body/input[1]")
        assert result.success is True
        mock_ele.clear.assert_called_once()


class TestSendEnter:
    """send_enter 方法测试"""

    def test_send_enter(self, element_operator, mock_page):
        """测试发送回车键"""
        element_operator.send_enter()
        mock_page.run_js.assert_called_once()
        mock_page.wait.assert_called_once()