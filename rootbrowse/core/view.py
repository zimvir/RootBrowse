"""页面扫描器"""

from typing import Any

from .types import Element, ElementPreview, Region, RegionSummary
from .constants import CLICKABLE_TAGS, DEFAULT_LIMIT, DEFAULT_OFFSET, KEY_ATTRS_PREVIEW, REGION_LABEL_KEYWORDS, TAG_LABELS, REGION_NOISE_TAGS
from .exceptions import RegionNotFoundError, ElementNotFoundError


class View:
    """页面扫描器，获取页面结构化信息（区块、元素摘要、完整元素）"""

    def __init__(self, page: Any):
        """
        初始化 View

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
        """检测页面语义区域（body 直接子元素，用 JS 一次获取）"""
        self._regions.clear()
        try:
            js = """
            var body = document.body;
            if (!body) return [];
            var results = [];
            var children = body.children;
            for (var i = 0; i < children.length; i++) {
                var child = children[i];
                var tag = child.tagName || '';
                var excludeTags = ['SCRIPT', 'STYLE', 'META', 'LINK', 'HEAD'];
                if (excludeTags.indexOf(tag) !== -1) continue;
                var id = child.getAttribute('id') || '';
                var cls = child.getAttribute('class') || '';
                var combined = (id + ' ' + cls).toLowerCase();
                var label = '区块';
                var keywordMap = {
                    'header': '头部', 'nav': '导航', 'footer': '底部',
                    'sidebar': '侧边栏', 'aside': '侧边栏', 'main': '主内容',
                    'content': '内容', 'article': '文章', 'section': '区块'
                };
                for (var key in keywordMap) {
                    if (combined.indexOf(key) !== -1) { label = keywordMap[key]; break; }
                }
                if (!id && !cls) label = tag.toLowerCase() || '区块';
                results.push({tag: tag, id: id, cls: cls, label: label, xpath: getXPath(child)});
            }
            return results;

            function getXPath(ele) {
                if (!ele || ele.nodeType !== 1) return '';
                var path = [];
                while (ele && ele.nodeType === 1) {
                    var index = 1;
                    for (var sibling = ele.previousSibling; sibling; sibling = sibling.previousSibling) {
                        if (sibling.nodeType === 1 && sibling.tagName === ele.tagName) index++;
                    }
                    var tag = ele.tagName.toLowerCase();
                    path.unshift(tag + '[' + index + ']');
                    ele = ele.parentElement;
                }
                return '/' + path.join('/');
            }
            """
            result = self._page.run_js(js)
            if not result:
                self._regions = [Region(xpath="/html/body", label="主内容")]
                return

            for item in result:
                self._regions.append(Region(
                    xpath=item['xpath'],
                    label=item['label']
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
        """用 JS 一次性查询区域内所有元素"""
        tags = CLICKABLE_TAGS if tag is None else [tag]
        selector = ','.join(tags)

        js = f"""
        function getXPath(ele) {{
            if (!ele || ele.nodeType !== 1) return '';
            var path = [];
            while (ele && ele.nodeType === 1) {{
                var index = 1;
                for (var sibling = ele.previousSibling; sibling; sibling = sibling.previousSibling) {{
                    if (sibling.nodeType === 1 && sibling.tagName === ele.tagName) index++;
                }}
                var tag = ele.tagName.toLowerCase();
                path.unshift(tag + '[' + index + ']');
                ele = ele.parentElement;
            }}
            return '/' + path.join('/');
        }}

        var region = document.evaluate("{region_xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (!region) return [];
        var results = [];
        var nodes = region.querySelectorAll("{selector}");
        for (var i = 0; i < nodes.length; i++) {{
            var ele = nodes[i];
            var attrs = {{}};
            var attrs_list = ele.attributes;
            for (var j = 0; j < attrs_list.length; j++) {{
                var attr = attrs_list[j];
                if (attr.name === 'href' || attr.name === 'src' || attr.name === 'class' || attr.name === 'id') {{
                    attrs[attr.name] = attr.value;
                }}
            }}
            results.push({{
                tag: ele.tagName.toLowerCase(),
                role: ele.getAttribute('role') || '',
                text: (ele.textContent || '').trim().substring(0, 100),
                xpath: getXPath(ele),
                attrs: attrs
            }});
        }}
        return results;
        """

        try:
            result = self._page.run_js(js)
            if not result:
                return []
            return [Element(**item) for item in result]
        except Exception:
            return []

    def _get_attrs_preview(self, ele: Element) -> dict:
        """获取元素的属性预览"""
        preview = {}
        for key in KEY_ATTRS_PREVIEW:
            if key in ele.attrs:
                preview[key] = ele.attrs[key]
        return preview