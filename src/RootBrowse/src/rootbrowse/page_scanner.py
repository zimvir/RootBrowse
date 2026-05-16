"""页面扫描器"""

from typing import Any

from .types import Element, ElementPreview, Region, RegionSummary
from .constants import CLICKABLE_TAGS, REF_PREFIX, DEFAULT_LIMIT, DEFAULT_OFFSET
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
        self._element_map: dict[str, Element] = {}
        self._regions: list[Region] = []

    def get_regions(self) -> list[Region]:
        """
        返回页面语义区块列表

        Returns:
            list[Region]: [{id, label, node_count}, ...]
        """
        self._scan_page()
        return self._regions

    def get_region_summary(self, region_id: str | list[str] | None = None) -> RegionSummary:
        """
        返回区域摘要

        Args:
            region_id: 区域 ID，str 单区域，list 多区域，None 全部区域

        Returns:
            RegionSummary: {count, tag_counts, role_counts, text_preview}

        Raises:
            RegionNotFoundError: 区域不存在
        """
        # 确定要搜索的区域列表
        if region_id is None:
            target_region_ids = [r.id for r in self._regions]
        elif isinstance(region_id, str):
            target_region_ids = [region_id]
        else:
            target_region_ids = region_id

        # 验证所有区域都存在
        for rid in target_region_ids:
            self._find_region(rid)

        # 收集所有目标区域的元素
        all_elements = []
        for rid in target_region_ids:
            all_elements.extend(self._get_elements_in_region(rid))

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
                    "ref": ele.ref
                })

        return RegionSummary(
            count=len(all_elements),
            tag_counts=tag_counts,
            role_counts=role_counts,
            text_preview=text_preview
        )

    def match_element(
        self,
        region_id: str | list[str] | None = None,
        query: str | None = None,
        tag: str | None = None,
        role: str | None = None,
        text_contains: str | None = None,
        limit: int = DEFAULT_LIMIT,
        offset: int = DEFAULT_OFFSET
    ) -> list[ElementPreview]:
        """
        按 region/keyword/tag/role/text 筛选元素，返回摘要列表

        Args:
            region_id: 搜索区域，可单选/多选/None（全部）
            query: 关键词搜索
            tag: HTML 标签筛选
            role: ARIA role 筛选
            text_contains: 文字包含筛选
            limit: 最多返回数量
            offset: 分页偏移

        Returns:
            list[ElementPreview]: [{ref, text, attrs_preview}, ...]
        """
        self._scan_page()

        # 确定搜索区域
        if region_id is None:
            target_refs = set(self._element_map.keys())
        elif isinstance(region_id, str):
            target_refs = self._get_refs_in_region(region_id)
        else:
            target_refs = set()
            for rid in region_id:
                target_refs |= self._get_refs_in_region(rid)

        # 筛选
        results = []
        for ref, ele in self._element_map.items():
            if ref not in target_refs:
                continue

            if tag and ele.tag != tag:
                continue
            if role and ele.role != role:
                continue
            if text_contains and text_contains not in ele.text:
                continue
            if query and query not in ele.text and query not in str(ele.attrs):
                continue

            results.append(ElementPreview(
                ref=ele.ref,
                text=ele.text[:100] if ele.text else "",
                attrs_preview=self._get_attrs_preview(ele)
            ))

        # 分页
        return results[offset:offset + limit]

    def get_element(self, locator: str, locator_type: str | None = None) -> Element:
        """
        通过定位符获取完整元素信息

        Args:
            locator: 定位符（ref / xpath / role / text / aria_label）
            locator_type: 定位类型，不指定则自动推断

        Returns:
            Element

        Raises:
            ElementNotFoundError: 元素不存在
        """
        # 自动推断 locator 类型
        if locator_type is None:
            if self._is_ref(locator):
                locator_type = "ref"
            else:
                locator_type = "xpath"

        # ref 查表
        if locator_type == "ref":
            if locator not in self._element_map:
                raise ElementNotFoundError(f"Element not found: {locator}")
            return self._element_map[locator]

        # 其他类型直接查询 DrissionPage
        try:
            if locator_type == "xpath":
                driss_ele = self._page.ele(f'xpath={locator}')
            elif locator_type == "role":
                driss_ele = self._page.ele(f'@role:{locator}')
            elif locator_type == "aria_label":
                driss_ele = self._page.ele(f'@aria-label:{locator}')
            elif locator_type == "text":
                driss_ele = self._page.ele(f'text={locator}')
            else:
                raise ElementNotFoundError(f"Unknown locator type: {locator_type}")

            if driss_ele is None:
                raise ElementNotFoundError(f"Element not found: {locator}")

            # 添加到 element_map 并返回
            new_ref = f"{REF_PREFIX}{len(self._element_map) + 1}"
            element = Element(
                ref=new_ref,
                tag=driss_ele.tag,
                role=driss_ele.attr("role") or "",
                text=driss_ele.text or "",
                xpath=driss_ele.xpath,
                attrs=dict(driss_ele.attrs) if hasattr(driss_ele, 'attrs') else {}
            )
            self._element_map[new_ref] = element
            return element
        except Exception as e:
            if isinstance(e, ElementNotFoundError):
                raise
            raise ElementNotFoundError(f"Element not found: {locator}, error: {e}")

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
        self._scan_page()

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

            # 为 DrissionPage 元素生成新 ref，加入 element_map
            new_ref = f"{REF_PREFIX}{len(self._element_map) + 1}"
            element = Element(
                ref=new_ref,
                tag=driss_ele.tag,
                role=driss_ele.attr("role") or "",
                text=driss_ele.text or "",
                xpath=driss_ele.xpath,
                attrs=dict(driss_ele.attrs) if hasattr(driss_ele, 'attrs') else {}
            )
            self._element_map[new_ref] = element
            return element
        except Exception:
            return None

    def _is_ref(self, locator: str) -> bool:
        """判断是否为 ref 格式（r + 数字）"""
        if not locator:
            return False
        if locator.startswith("r") and locator[1:].isdigit():
            return True
        return False

    def _scan_page(self) -> None:
        """扫描页面，构建元素映射和区域列表"""
        self._element_map.clear()
        self._regions.clear()

        # 扫描可交互元素（DrissionPage 用 tag: 前缀）
        ref_counter = 1
        for tag in CLICKABLE_TAGS:
            for ele in self._page.eles(f'tag:{tag}', timeout=0.5):
                try:
                    xpath = ele.xpath
                except Exception:
                    xpath = ""  # xpath 获取失败时用空字符串

                try:
                    text = ele.text or ""
                except Exception:
                    text = ""

                self._element_map[f"{REF_PREFIX}{ref_counter}"] = Element(
                    ref=f"{REF_PREFIX}{ref_counter}",
                    tag=ele.tag,
                    role=ele.attr("role") or "",
                    text=text,
                    xpath=xpath,
                    attrs=dict(ele.attrs) if hasattr(ele, 'attrs') else {}
                )
                ref_counter += 1

        # 临时区域划分（按 body 直接子元素）
        self._regions = [
            Region(id="main", label="主内容", node_count=len(self._element_map))
        ]

    def _find_region(self, region_id: str) -> Region:
        """查找区域"""
        for region in self._regions:
            if region.id == region_id:
                return region
        raise RegionNotFoundError(f"Region not found: {region_id}")

    def _get_refs_in_region(self, region_id: str) -> set[str]:
        """获取区域内所有元素的 ref"""
        # TODO: 实现按区域过滤
        # 目前返回所有 ref
        return set(self._element_map.keys())

    def _get_elements_in_region(self, region_id: str) -> list[Element]:
        """获取区域内所有元素"""
        refs = self._get_refs_in_region(region_id)
        return [self._element_map[ref] for ref in refs if ref in self._element_map]

    def _get_attrs_preview(self, ele: Element) -> dict:
        """获取元素的属性预览"""
        preview = {}
        key_attrs = ['href', 'src', 'alt', 'title', 'name', 'type', 'value']
        for key in key_attrs:
            if key in ele.attrs:
                preview[key] = ele.attrs[key]
        return preview