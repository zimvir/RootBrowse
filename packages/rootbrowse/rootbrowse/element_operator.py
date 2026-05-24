"""元素操作器"""

from typing import Any

from .types import Element, OperationResult
from .exceptions import ElementNotFoundError


class ElementOperator:
    """元素操作器，执行点击、输入、悬停等操作（纯 JS 实现）"""

    def __init__(self, page: Any):
        """
        初始化 ElementOperator

        Args:
            page: DrissionPage ChromiumPage 实例
        """
        self._page = page

    def _xpath_to_js(self, xpath: str, js_code: str) -> str:
        """
        将 xpath 包装成 JS 代码，在元素上执行操作

        Args:
            xpath: 元素 xpath
            js_code: 在 ele 变量上执行的 JS 代码（用 ele 表示元素）

        Returns:
            完整的 JS 字符串
        """
        return f"""
        var ele = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (!ele) return 'not found';
        {js_code}
        return 'ok';
        """

    def click(self, xpath: str) -> OperationResult:
        """
        点击元素

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, new_url?, error?}
        """
        try:
            self._page.wait.doc_loaded()
            js = self._xpath_to_js(xpath, "ele.click();")
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def input_by_xpath(
        self, xpath: str, text: str, clear: bool = False
    ) -> OperationResult:
        """
        向输入框写入文字（保留 DrissionPage，因为需要处理中文输入法）

        Args:
            xpath: 元素 xpath 路径
            text: 要输入的文字
            clear: 是否先清空输入框

        Returns:
            OperationResult: {success, error?}
        """
        try:
            ele = self._page.ele(f'xpath={xpath}')
            if clear:
                ele.clear()
            ele.input(text)
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def hover(self, xpath: str) -> OperationResult:
        """
        悬停在元素上

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, error?}
        """
        try:
            js = self._xpath_to_js(xpath, """
            var event = new MouseEvent('mouseover', {bubbles: true, cancelable: true, view: window});
            ele.dispatchEvent(event);
            """)
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def double_click(self, xpath: str) -> OperationResult:
        """
        双击元素

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, error?}
        """
        try:
            js = self._xpath_to_js(xpath, """
            var event = new MouseEvent('dblclick', {bubbles: true, cancelable: true, view: window});
            ele.dispatchEvent(event);
            """)
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def right_click(self, xpath: str) -> OperationResult:
        """
        右键点击元素

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, error?}
        """
        try:
            js = self._xpath_to_js(xpath, """
            var event = new MouseEvent('contextmenu', {bubbles: true, cancelable: true, view: window});
            ele.dispatchEvent(event);
            """)
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def submit(self, xpath: str) -> OperationResult:
        """
        提交表单

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, error?}
        """
        try:
            js = self._xpath_to_js(xpath, "if (ele.form) ele.form.submit();")
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def clear(self, xpath: str) -> OperationResult:
        """
        清空输入框

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, error?}
        """
        try:
            js = self._xpath_to_js(xpath, "ele.value = '';")
            result = self._page.run_js(js)
            if result == 'ok':
                return OperationResult(success=True)
            return OperationResult(success=False, error=f"元素未找到: {xpath}")
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def send_enter(self) -> None:
        """发送回车键"""
        self._page.run_js(
            "document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13}));"
        )
        self._page.wait(0.1)