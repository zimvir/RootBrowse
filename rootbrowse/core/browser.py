"""浏览器主入口"""

import json
from typing import Any

from .constants import DEFAULT_URL
from .tab_manager import TabManager
from .element_operator import ElementOperator
from .page_scanner import PageScanner
from .types import Region, RegionSummary, Element, ElementPreview, OperationResult
from .exceptions import BrowserError, StateFileError, PageLoadError


class Browser:
    """
    浏览器主入口，组合 TabManager、ElementOperator、PageScanner

    AI 调用方式：
        browser = Browser()                    # 默认打开 bing.com
        browser = Browser('https://example.com') # 指定 URL
        browser.view.get_regions()
        browser.act.click('r1')
    """

    def __init__(self, page: Any | None = None, url: str | None = None, headless: bool = True):
        """
        初始化 Browser

        Args:
            page: DrissionPage ChromiumPage 实例，None 则自动创建
            url: 默认打开的 URL，配合 page 为 None 时使用
            headless: 是否使用无头模式，默认 Ture（无头浏览器）
        """
        page_2 = page
        if page is None:
            from DrissionPage import ChromiumPage, ChromiumOptions
            opts = ChromiumOptions()
            # 有头还是无头浏览器
            if headless:
                opts.set_argument('--headless=new', value=True)
                opts.set_argument('--disable-gpu')
                opts.set_argument('--no-sandbox')

            page = ChromiumPage(addr_or_opts=opts)

        self._page = page
        self._closed = False

        # 初始化子模块
        self._page_scanner = PageScanner(self._page)
        self._tab_manager = TabManager(self._page)
        self._element_operator = ElementOperator(self._page)

        # 打开默认 URL（只有当 page 和 url 都没提供时才自动打开）
        if page_2 is None and url is None:
            self.get(DEFAULT_URL)

    @classmethod
    def create(cls, url: str | None = None) -> "Browser":
        """
        工厂方法：创建 Browser 并打开指定 URL

        Args:
            url: 目标 URL，None 则打开 DEFAULT_URL (bing.com)

        Returns:
            Browser 实例
        """
        if url is None:
            url = DEFAULT_URL
        return cls(url=url)

    @property
    def tabs(self) -> TabManager:
        """标签页管理器"""
        return self._tab_manager

    @property
    def view(self) -> PageScanner:
        """页面扫描器"""
        return self._page_scanner

    @property
    def act(self) -> ElementOperator:
        """元素操作器"""
        return self._element_operator

    def get(self, url: str, timeout: float = 30) -> dict:
        """
        打开 URL

        Args:
            url: 目标 URL
            timeout: 超时时间（秒）

        Returns:
            dict: {url, title}

        Raises:
            PageLoadError: 页面加载失败
        """
        try:
            self._page.get(url, timeout=timeout)
            self._page_scanner.clear_cache()  # 清空缓存，换页面了
            title = self._page.title or ""
            return {"url": url, "title": title}
        except Exception as e:
            raise PageLoadError(f"Failed to load page: {url}, error: {e}")

    def screenshot(
        self,
        path: str | None = None,
        annotate: list[list[int]] | None = None
    ) -> str:
        """
        页面截图

        Args:
            path: 保存路径，None 则返回 base64 字符串
            annotate: 标注区域列表 [[x1,y1,x2,y2], ...]

        Returns:
            str: 文件路径或 base64 字符串
        """
        if path:
            self._page.get_screenshot(path=path)
            return path
        else:
            return self._page.screenshot()

    def save_state(self, path: str) -> None:
        """
        保存浏览器状态（cookies）

        Args:
            path: 保存路径

        Raises:
            StateFileError: 保存失败
        """
        try:
            cookies = self._page.cookies()
            data = {
                'version': '0.1.0',
                'cookies': cookies if isinstance(cookies, list) else list(cookies),
                'saved_at': self._get_timestamp(),
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise StateFileError(f"Failed to save state: {e}")

    def load_state(self, path: str) -> None:
        """
        恢复浏览器状态（cookies）

        Args:
            path: 状态文件路径

        Raises:
            StateFileError: 恢复失败
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cookies = data.get('cookies', [])
            if cookies:
                self._page.set.cookies(cookies)
        except Exception as e:
            raise StateFileError(f"Failed to load state: {e}")

    @staticmethod
    def _get_timestamp() -> str:
        """返回当前时间戳 ISO 格式"""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()

    def close(self) -> None:
        """关闭浏览器"""
        if not self._closed:
            self._page.quit()
            self._closed = True

    def run_js(self, code: str, *args) -> Any:
        """
        在浏览器端执行 JavaScript

        Args:
            code: JavaScript 代码
            *args: 传递给 JS 的参数

        Returns:
            任意类型: JS 执行结果
        """
        return self._page.run_js(code, *args)
