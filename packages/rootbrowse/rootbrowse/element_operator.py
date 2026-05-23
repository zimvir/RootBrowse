"""元素操作器"""

from typing import Any

from .types import Element, OperationResult
from .exceptions import ElementNotFoundError


class ElementOperator:
    """元素操作器，执行点击、输入、悬停等操作"""

    def __init__(self, page: Any):
        """
        初始化 ElementOperator

        Args:
            page: DrissionPage ChromiumPage 实例
        """
        self._page = page

    def click(self, xpath: str) -> OperationResult:
        """
        点击元素

        Args:
            xpath: 元素 xpath 路径

        Returns:
            OperationResult: {success, new_url?, error?}
        """
        try:
            self._page.ele(f'xpath={xpath}').click()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def input_by_xpath(
        self, xpath: str, text: str, clear: bool = False
    ) -> OperationResult:
        """
        向输入框写入文字

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
            self._page.ele(f'xpath={xpath}').hover()
            return OperationResult(success=True)
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
            self._page.ele(f'xpath={xpath}').double_click()
            return OperationResult(success=True)
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
            self._page.ele(f'xpath={xpath}').right_click()
            return OperationResult(success=True)
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
            self._page.ele(f'xpath={xpath}').submit()
            return OperationResult(success=True)
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
            self._page.ele(f'xpath={xpath}').clear()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def send_enter(self) -> None:
        """发送回车键"""
        self._page.run_js(
            "document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13}));"
        )
        self._page.wait(0.1)