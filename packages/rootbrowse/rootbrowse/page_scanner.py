"""页面扫描器"""

from typing import Any

from .types import Element, ElementPreview, Region, RegionSummary
from .constants import CLICKABLE_TAGS, DEFAULT_LIMIT, DEFAULT_OFFSET, KEY_ATTRS_PREVIEW, REGION_LABEL_KEYWORDS, TAG_LABELS, REGION_NOISE_TAGS
from .exceptions import RegionNotFoundError, ElementNotFoundError


class PageScanner:
    """页面扫描器，获取页面结构化信息（区块、元素摘要、完整元素）"""

    def __init__(self, page: Any):
        """
        初始化 PageScanner

        Args:
            page: DrissionPage ChromiumPage 实例
        """
        self._page = page
        self._regions: list[Region] = []

    def get_regions(self) -> list[Region]:
        """
        返回页面语义区块列表

        Returns:
            list[Region]: [{xpath, label}, ...]
        """
        self._detect_regions()
        return self._regions

    def get_region_summary(self, region_xpath: str | list[str] | None = None) -> RegionSummary:
        """
        返回区域摘要

        Args:
            region_xpath: 区域 xpath，str 单区域，list 多区域，None 全部区域

        Returns:
            RegionSummary: {count, tag_counts, role_counts, text_preview}

        Raises:
            RegionNotFoundError: 区域不存在
        """
        # 确定要搜索的区域列表
        if region_xpath is None:
            target_xpaths = [r.xpath for r in self._regions]
        elif isinstance(region_xpath, str):
            target_xpaths = [region_xpath]
        else:
            target_xpaths = region_xpath

        # 验证所有区域都存在
        for xp in target_xpaths:
            self._find_region_by_xpath(xp)

        # 收集所有目标区域的元素
        all_elements = []
        for xp in target_xpaths:
            all_elements.extend(self._query_elements_in_region(xp))

        # 统计
        tag_counts: dict[str, int] = {}
        role_counts: dict[str, int] = {}
        text_preview = []

        for ele in all_elements:
            tag_counts[ele.tag] = tag_counts.get(ele.tag, 0) + 1
            role_counts[ele.role] = role_counts.get(ele.role, 0) + 1

            if ele.text and len(text_preview) < 10:
                text_preview.append({
                    "tag": ele.tag,
                    "text": ele.text[:50],
                    "xpath": ele.xpath
                })

        return RegionSummary(
            count=len(all_elements),
            tag_counts=tag_counts,
            role_counts=role_counts,
            text_preview=text_preview
        )

    def match_element(
        self,
        region_xpath: str | list[str] | None = None,
        query: str | None = None,
        tag: str | None = None,
        role: str | None = None,
        text_contains: str | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = DEFAULT_OFFSET
    ) -> list[ElementPreview]:
        """
        按条件筛选元素，返回摘要列表

        Args:
            region_xpath: 搜索区域 xpath，可单选/多选/None（全部）
            query: 关键词搜索
            tag: HTML 标签筛选
            role: ARIA role 筛选
            text_contains: 文字包含筛选
            limit: 最多返回数量
            offset: 分页偏移

        Returns:
            list[ElementPreview]: [{xpath, text, attrs_preview}, ...]
        """
        # 确定搜索区域 xpath 列表
        if region_xpath is None:
            region_xpaths = [r.xpath for r in self._regions] if self._regions else [""]
        elif isinstance(region_xpath, str):
            region_xpaths = [region_xpath]
        else:
            region_xpaths = region_xpath

        # 对每个区域做查询
        results = []
        for rxp in region_xpaths:
            elements = self._query_elements_in_region(rxp, tag=tag)
            for ele in elements:
                if tag and ele.tag != tag:
                    continue
                if role and ele.role != role:
                    continue
                if text_contains and text_contains not in ele.text:
                    continue
                if query and query not in ele.text and query not in str(ele.attrs):
                    continue

                results.append(ElementPreview(
                    xpath=ele.xpath,
                    text=ele.text[:100] if ele.text else "",
                    attrs_preview=self._get_attrs_preview(ele)
                ))

        return results[offset:offset + limit]

    def get_element(self, xpath: str) -> Element:
        """
        通过 xpath 获取完整元素信息

        Args:
            xpath: 元素 xpath 路径

        Returns:
            Element

        Raises:
            ElementNotFoundError: 元素不存在
        """
        try:
            driss_ele = self._page.ele(f'xpath={xpath}')
            if driss_ele is None:
                raise ElementNotFoundError(f"Element not found: {xpath}")

            return Element(
                tag=driss_ele.tag,
                role=driss_ele.attr("role") or "",
                text=driss_ele.text or "",
                xpath=driss_ele.xpath or xpath,
                attrs=dict(driss_ele.attrs) if hasattr(driss_ele, 'attrs') else {}
            )
        except ElementNotFoundError:
            raise
        except Exception as e:
            raise ElementNotFoundError(f"Element not found: {xpath}, error: {e}")

    def find_element(
        self,
        by: str,
        value: str,
        filter: dict | None = None
    ) -> Element | None:
        """
        多维度定位元素

        Args:
            by: 定位方式（xpath / role / aria_label / text）
            value: 定位值
            filter: 额外过滤条件

        Returns:
            Element | None
        """
        try:
            if by == "xpath":
                driss_ele = self._page.ele(f'xpath={value}')
            elif by == "role":
                driss_ele = self._page.ele(f'@role:{value}')
            elif by == "aria_label":
                driss_ele = self._page.ele(f'@aria-label:{value}')
            elif by == "text":
                driss_ele = self._page.ele(f'text={value}')
            else:
                return None

            if driss_ele is None:
                return None

            return Element(
                tag=driss_ele.tag,
                role=driss_ele.attr("role") or "",
                text=driss_ele.text or "",
                xpath=driss_ele.xpath or "",
                attrs=dict(driss_ele.attrs) if hasattr(driss_ele, 'attrs') else {}
            )
        except Exception:
            return None

    def clear_cache(self) -> None:
        """清空缓存，换页面时调用"""
        self._regions.clear()

    def _detect_regions(self) -> None:
        """检测页面语义区域（body 直接子元素）"""
        self._regions.clear()
        try:
            body = self._page.ele('tag:body')
            if body is None:
                self._regions = [Region(xpath="/html/body", label="主内容")]
                return

            children = body.children()

            for child in children:
                tag = child.tag or ""
                if tag in REGION_NOISE_TAGS:
                    continue

                region_label = self._guess_region_label(child)
                self._regions.append(Region(
                    xpath=child.xpath,
                    label=region_label
                ))

            if not self._regions:
                self._regions = [Region(xpath="/html/body", label="主内容")]

        except Exception:
            self._regions = [Region(xpath="/html/body", label="主内容")]

    def _guess_region_label(self, element: Any) -> str:
        """根据元素属性猜测区域标签"""
        region_id = element.attr('id') or ""
        region_class = element.attr('class') or ""

        combined = (region_id + ' ' + region_class).lower()
        for keyword, label in REGION_LABEL_KEYWORDS.items():
            if keyword in combined:
                return label

        tag = element.tag or '区域'
        return TAG_LABELS.get(tag, tag)

    def _find_region_by_xpath(self, xpath: str) -> Region:
        """通过 xpath 查找区域"""
        for region in self._regions:
            if region.xpath == xpath:
                return region
        raise RegionNotFoundError(f"Region not found: {xpath}")

    def _query_elements_in_region(self, region_xpath: str, tag: str | None = None) -> list[Element]:
        """查询区域内符合条件的元素"""
        elements = []

        # 如果指定了 tag，直接用 tag 查询
        tags_to_query = [tag] if tag else CLICKABLE_TAGS

        for t in tags_to_query:
            try:
                # 先尝试在区域内查询
                region_ele = self._page.ele(f'xpath={region_xpath}')
                if region_ele:
                    for ele in region_ele.eles(f'tag:{t}', timeout=0.5):
                        try:
                            elements.append(Element(
                                tag=ele.tag,
                                role=ele.attr("role") or "",
                                text=ele.text or "",
                                xpath=ele.xpath or "",
                                attrs=dict(ele.attrs) if hasattr(ele, 'attrs') else {}
                            ))
                        except Exception:
                            continue
            except Exception:
                continue

        return elements

    def _get_attrs_preview(self, ele: Element) -> dict:
        """获取元素的属性预览"""
        preview = {}
        for key in KEY_ATTRS_PREVIEW:
            if key in ele.attrs:
                preview[key] = ele.attrs[key]
        return preview