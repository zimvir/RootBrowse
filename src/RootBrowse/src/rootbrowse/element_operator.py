"""元素操作器"""

from typing import Any

from .types import Element, OperationResult
from .exceptions import ElementNotFoundError


class ElementOperator:
    """元素操作器，执行点击、输入、悬停等操作"""

    def __init__(self, page: Any, element_map: dict[str, Element]):
        """
        初始化 ElementOperator

        Args:
            page: DrissionPage ChromiumPage 实例
            element_map: ref -> Element 映射表
        """
        self._page = page
        self._element_map = element_map

    def click(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        点击元素

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型，不指定则自动推断

        Returns:
            OperationResult: {success, new_url?, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            self._page.ele(f'xpath={xpath}').click()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def input_by_ref(
        self, locator: str, text: str, clear: bool = False, locator_type: str | None = None
    ) -> OperationResult:
        """
        向输入框写入文字

        Args:
            locator: 定位符（ref / xpath / role / text）
            text: 要输入的文字
            clear: 是否先清空输入框
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            ele = self._page.ele(f'xpath={xpath}')
            if clear:
                ele.clear()
            ele.input(text)
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def hover(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        悬停在元素上

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            self._page.ele(f'xpath={xpath}').hover()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def double_click(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        双击元素

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            self._page.ele(f'xpath={xpath}').double_click()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def right_click(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        右键点击元素

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            self._page.ele(f'xpath={xpath}').right_click()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def submit(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        提交表单

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
            self._page.ele(f'xpath={xpath}').submit()
            return OperationResult(success=True)
        except Exception as e:
            return OperationResult(success=False, error=str(e))

    def clear(self, locator: str, locator_type: str | None = None) -> OperationResult:
        """
        清空输入框

        Args:
            locator: 定位符（ref / xpath / role / text）
            locator_type: 定位类型

        Returns:
            OperationResult: {success, error?}
        """
        try:
            xpath = self._resolve_locator(locator, locator_type)
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

    def ref_to_xpath(self, ref: str) -> str:
        """
        通过 ref 获取 xpath（内部方法，供外部调用）

        Args:
            ref: 元素引用 ID

        Returns:
            xpath 路径

        Raises:
            ElementNotFoundError: 元素不存在
        """
        if ref not in self._element_map:
            raise ElementNotFoundError(f"Element not found: {ref}")
        return self._element_map[ref].xpath

    def _resolve_locator(self, locator: str, locator_type: str | None = None) -> str:
        """
        解析定位符，ref 需要查表转 xpath，其他直接返回

        Args:
            locator: 定位符
            locator_type: 定位类型

        Returns:
            xpath 字符串

        Raises:
            ElementNotFoundError: ref 不存在
        """
        # 指定了类型
        if locator_type == "ref":
            return self.ref_to_xpath(locator)
        elif locator_type:
            return locator

        # 自动推断：ref 查表，其他直接返回
        if self._is_ref(locator):
            return self.ref_to_xpath(locator)
        return locator

    def _is_ref(self, locator: str) -> bool:
        """
        判断是否为 ref（格式：r + 数字）

        Args:
            locator: 定位符

        Returns:
            是否为 ref
        """
        if not locator:
            return False
        if locator.startswith("r") and locator[1:].isdigit():
            return True
        return False