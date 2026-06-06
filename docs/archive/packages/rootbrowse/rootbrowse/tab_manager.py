"""标签页管理器"""

from typing import Any

from .exceptions import TabNotFoundError


class TabManager:
    """标签页管理器，管理浏览器标签页（新增、切换、关闭）"""

    def __init__(self, page: Any):
        """
        初始化 TabManager

        Args:
            page: DrissionPage ChromiumPage 实例
        """
        self._page = page

    @property
    def _tabs(self) -> list:
        """实时获取 DrissionPage 标签页列表"""
        return self._page.tab_ids

    def new_tab(self, url: str) -> int:
        """
        打开新标签页

        Args:
            url: 目标 URL

        Returns:
            新标签页索引
        """
        self._page.new_tab(url)
        # 返回新标签页的索引（切换过去了所以就是当前）
        return self.current_index()

    def close_tab(self, index: int | None = None) -> None:
        """
        关闭指定标签页

        Args:
            index: 目标标签页索引，None 表示关闭当前标签页
        """
        total = self.tabs_count()
        if total <= 1:
            raise TabNotFoundError("Cannot close the last tab")

        target = index if index is not None else self.current_index()

        if target < 0 or target >= total:
            raise TabNotFoundError(f"Tab index out of range: {target}")

        # 先切换到目标标签页再关闭
        if target != self.current_index():
            self._page.activate_tab(target)
        self._page.close()

    def switch_to_tab(self, index: int) -> None:
        """
        切换到指定标签页

        Args:
            index: 目标标签页索引

        Raises:
            TabNotFoundError: 索引越界
        """
        total = self.tabs_count()
        if index < 0 or index >= total:
            raise TabNotFoundError(f"Tab index out of range: {index}")
        self._page.activate_tab(index)

    def tabs_count(self) -> int:
        """
        返回标签页数量

        Returns:
            标签页数量
        """
        return len(self._tabs)

    def current_index(self) -> int:
        """
        返回当前标签页索引

        Returns:
            当前标签页索引
        """
        current_tab = self._page.tab_id
        for i, tid in enumerate(self._tabs):
            if tid == current_tab:
                return i
        return 0