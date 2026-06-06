"""数据类型定义"""

from dataclasses import dataclass, field


@dataclass
class Region:
    """页面语义区块"""
    xpath: str
    """区域根元素的 xpath"""
    label: str
    """人类可读名称"""


@dataclass
class Element:
    """可交互元素"""
    tag: str
    """HTML 标签"""
    role: str
    """ARIA role"""
    text: str
    """显示文字"""
    xpath: str
    """元素路径"""
    attrs: dict = field(default_factory=dict)
    """关键属性"""


@dataclass
class RegionSummary:
    """区域摘要"""
    count: int
    """总元素数"""
    tag_counts: dict
    """按标签分类统计 {tag: count}"""
    role_counts: dict
    """按 role 分类统计 {role: count}"""
    text_preview: list
    """文字预览 [{tag, text, xpath}, ...]"""


@dataclass
class ElementPreview:
    """元素摘要（match_element 返回）"""
    xpath: str
    """元素路径"""
    text: str
    """显示文字"""
    attrs_preview: dict
    """关键属性预览"""


@dataclass
class OperationResult:
    """操作结果"""
    success: bool
    """是否成功"""
    error: str | None = None
    """错误信息"""
    new_url: str | None = None
    """操作后的新 URL"""