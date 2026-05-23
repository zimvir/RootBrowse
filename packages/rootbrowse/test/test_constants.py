"""constants 常量测试"""

import pytest

from rootbrowse.constants import (
    INTERACTIVE_TAGS,
    INPUT_TAGS,
    CLICKABLE_TAGS,
    ROLE_TAG_MAP,
    REGION_ID_HEADER,
    REGION_ID_MAIN,
    REGION_ID_SIDEBAR,
    REGION_ID_FOOTER,
    REGION_ID_NAV,
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    DEFAULT_TIMEOUT,
    REF_PREFIX,
    STATE_FILE_EXTENSION,
)


class TestInteractiveTags:
    """可交互标签测试"""

    def test_interactive_tags_not_empty(self):
        """测试可交互标签列表非空"""
        assert len(INTERACTIVE_TAGS) > 0

    def test_interactive_tags_contains_common(self):
        """测试包含常见可交互标签"""
        for tag in ['a', 'button', 'input', 'select', 'textarea']:
            assert tag in INTERACTIVE_TAGS

    def test_interactive_tags_is_list(self):
        """测试是可交互标签列表"""
        assert isinstance(INTERACTIVE_TAGS, list)
        assert all(isinstance(t, str) for t in INTERACTIVE_TAGS)


class TestInputTags:
    """输入标签测试"""

    def test_input_tags_not_empty(self):
        """测试输入标签列表非空"""
        assert len(INPUT_TAGS) > 0

    def test_input_tags_subset_of_interactive(self):
        """测试输入标签是可交互标签的子集"""
        assert all(tag in INTERACTIVE_TAGS for tag in INPUT_TAGS)

    def test_input_tags_contains_input_and_textarea(self):
        """测试包含 input 和 textarea"""
        assert 'input' in INPUT_TAGS
        assert 'textarea' in INPUT_TAGS


class TestClickableTags:
    """可点击标签测试"""

    def test_clickable_tags_not_empty(self):
        """测试可点击标签列表非空"""
        assert len(CLICKABLE_TAGS) > 0

    def test_clickable_tags_subset_of_interactive(self):
        """测试可点击标签是可交互标签的子集"""
        assert all(tag in INTERACTIVE_TAGS for tag in CLICKABLE_TAGS)

    def test_clickable_tags_contains_anchor_and_button(self):
        """测试包含 a 和 button"""
        assert 'a' in CLICKABLE_TAGS
        assert 'button' in CLICKABLE_TAGS


class TestRoleTagMap:
    """ARIA role 映射测试"""

    def test_role_tag_map_not_empty(self):
        """测试 role 映射非空"""
        assert len(ROLE_TAG_MAP) > 0

    def test_role_tag_map_structure(self):
        """测试 role 映射结构"""
        assert isinstance(ROLE_TAG_MAP, dict)
        assert all(isinstance(k, str) and isinstance(v, str) for k, v in ROLE_TAG_MAP.items())

    def test_role_tag_map_common_roles(self):
        """测试包含常见 role 映射"""
        assert ROLE_TAG_MAP.get('link') == 'a'
        assert ROLE_TAG_MAP.get('button') == 'button'
        assert ROLE_TAG_MAP.get('textbox') == 'input'


class TestRegionIds:
    """区域 ID 常量测试"""

    def test_region_ids_are_strings(self):
        """测试区域 ID 都是字符串"""
        assert isinstance(REGION_ID_HEADER, str)
        assert isinstance(REGION_ID_MAIN, str)
        assert isinstance(REGION_ID_SIDEBAR, str)
        assert isinstance(REGION_ID_FOOTER, str)
        assert isinstance(REGION_ID_NAV, str)

    def test_region_ids_have_correct_values(self):
        """测试区域 ID 值正确"""
        assert REGION_ID_HEADER == "header"
        assert REGION_ID_MAIN == "main"
        assert REGION_ID_SIDEBAR == "sidebar"
        assert REGION_ID_FOOTER == "footer"
        assert REGION_ID_NAV == "nav"


class TestDefaultConfig:
    """默认配置测试"""

    def test_default_limit_positive(self):
        """测试 DEFAULT_LIMIT 为正整数"""
        assert isinstance(DEFAULT_LIMIT, int)
        assert DEFAULT_LIMIT > 0

    def test_default_offset_zero(self):
        """测试 DEFAULT_OFFSET 为零"""
        assert DEFAULT_OFFSET == 0

    def test_default_timeout_positive(self):
        """测试 DEFAULT_TIMEOUT 为正数"""
        assert isinstance(DEFAULT_TIMEOUT, (int, float))
        assert DEFAULT_TIMEOUT > 0


class TestRefPrefix:
    """ref 前缀测试"""

    def test_ref_prefix_is_r(self):
        """测试 ref 前缀是 'r'"""
        assert REF_PREFIX == 'r'

    def test_ref_prefix_single_char(self):
        """测试 ref 前缀是单字符"""
        assert len(REF_PREFIX) == 1


class TestStateFileExtension:
    """状态文件扩展名测试"""

    def test_state_file_extension_format(self):
        """测试状态文件扩展名格式"""
        assert STATE_FILE_EXTENSION.startswith('.')
        assert STATE_FILE_EXTENSION.endswith('.json')
