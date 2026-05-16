"""MCP Tools for RootBrowse"""

from rootbrowse import Browser


# 全局 Browser 实例，MCP 进程内复用
_browser: Browser | None = None


def get_browser() -> Browser:
    """获取或创建 Browser 实例"""
    global _browser
    if _browser is None:
        _browser = Browser()
    return _browser


def close_browser():
    """关闭 Browser 实例"""
    global _browser
    if _browser:
        _browser.close()
        _browser = None


def register_tools(mcp):
    """注册所有 MCP tools"""

    # ========== 页面扫描 ==========

    @mcp.tool()
    def get_page_regions():
        """获取页面所有语义区域

        Returns:
            list[dict]: 区域列表 [{id, label, node_count}, ...]
        """
        browser = get_browser()
        regions = browser.view.get_regions()
        return [{"id": r.id, "label": r.label, "node_count": r.node_count} for r in regions]

    @mcp.tool()
    def get_region_summary(region_id: str):
        """获取指定区域的统计摘要

        Args:
            region_id: 区域 ID，如 'region_1'

        Returns:
            dict: {count, tag_counts, role_counts, text_preview}
        """
        browser = get_browser()
        summary = browser.view.get_region_summary(region_id)
        return {
            "count": summary.count,
            "tag_counts": summary.tag_counts,
            "role_counts": summary.role_counts,
            "text_preview": summary.text_preview,
        }

    @mcp.tool()
    def match_element(
        region_id: str | None = None,
        tag: str | None = None,
        role: str | None = None,
        text_contains: str | None = None,
        query: str | None = None,
        limit: int = 20,
    ):
        """按条件筛选元素，返回摘要列表

        Args:
            region_id: 搜索区域，None 表示全部区域
            tag: HTML 标签，如 'a', 'button', 'input'
            role: ARIA role，如 'link', 'button'
            text_contains: 文字包含的关键词
            query: 综合搜索关键词
            limit: 最多返回数量，默认 20

        Returns:
            list[dict]: [{ref, text, attrs_preview}, ...]
        """
        browser = get_browser()
        results = browser.view.match_element(
            region_id=region_id,
            tag=tag,
            role=role,
            text_contains=text_contains,
            query=query,
            limit=limit,
        )
        return [
            {
                "ref": r.ref,
                "text": r.text,
                "attrs_preview": r.attrs_preview,
            }
            for r in results
        ]

    @mcp.tool()
    def get_element(ref: str):
        """获取元素的完整信息

        Args:
            ref: 元素引用 ID，如 'r5'

        Returns:
            dict: {ref, tag, role, text, xpath, attrs}
        """
        browser = get_browser()
        ele = browser.view.get_element(ref)
        return {
            "ref": ele.ref,
            "tag": ele.tag,
            "role": ele.role,
            "text": ele.text,
            "xpath": ele.xpath,
            "attrs": ele.attrs,
        }

    # ========== 元素操作 ==========

    @mcp.tool()
    def click_element(ref: str):
        """点击元素

        Args:
            ref: 元素引用 ID

        Returns:
            dict: {success, new_url, error}
        """
        browser = get_browser()
        result = browser.act.click(ref)
        return {
            "success": result.success,
            "new_url": result.new_url,
            "error": result.error,
        }

    @mcp.tool()
    def input_text(ref: str, text: str, clear: bool = False):
        """向输入框输入文字

        Args:
            ref: 元素引用 ID
            text: 要输入的文字
            clear: 是否先清空，默认 False

        Returns:
            dict: {success, error}
        """
        browser = get_browser()
        result = browser.act.input_by_ref(ref, text, clear=clear)
        return {
            "success": result.success,
            "error": result.error,
        }

    @mcp.tool()
    def send_enter():
        """发送回车键"""
        browser = get_browser()
        browser.act.send_enter()
        return {"success": True}

    # ========== 浏览器 ==========

    @mcp.tool()
    def get_page(url: str, timeout: float = 30):
        """打开 URL

        Args:
            url: 目标 URL
            timeout: 超时时间（秒），默认 30

        Returns:
            dict: {url, title}
        """
        browser = get_browser()
        result = browser.get(url, timeout=timeout)
        return {"url": result["url"], "title": result["title"]}

    @mcp.tool()
    def take_screenshot(path: str | None = None):
        """页面截图

        Args:
            path: 保存路径，None 则返回 base64

        Returns:
            str: 文件路径或 base64 字符串
        """
        browser = get_browser()
        return browser.screenshot(path=path)

    @mcp.tool()
    def close_browser():
        """关闭浏览器"""
        close_browser()
        return {"success": True}

    # ========== 标签页 ==========

    @mcp.tool()
    def new_tab(url: str):
        """打开新标签页

        Args:
            url: 目标 URL

        Returns:
            int: 新标签页索引
        """
        browser = get_browser()
        return browser.tabs.new_tab(url)

    @mcp.tool()
    def close_tab():
        """关闭当前标签页"""
        browser = get_browser()
        browser.tabs.close_tab()
        return {"success": True}

    @mcp.tool()
    def switch_tab(index: int):
        """切换到指定标签页

        Args:
            index: 标签页索引（从 0 开始）
        """
        browser = get_browser()
        browser.tabs.switch_to_tab(index)
        return {"success": True}

    @mcp.tool()
    def get_tabs_count():
        """获取标签页数量"""
        browser = get_browser()
        return {"count": browser.tabs.tabs_count(), "current": browser.tabs.current_index()}

    # ========== 状态 ==========

    @mcp.tool()
    def save_state(path: str):
        """保存浏览器状态（cookies）

        Args:
            path: 保存文件路径
        """
        browser = get_browser()
        browser.save_state(path)
        return {"success": True, "path": path}

    @mcp.tool()
    def load_state(path: str):
        """恢复浏览器状态（cookies）

        Args:
            path: 状态文件路径
        """
        browser = get_browser()
        browser.load_state(path)
        return {"success": True}