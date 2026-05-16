"""常量配置"""

# 默认 URL
DEFAULT_URL = "https://www.bing.com"

# 可交互的 HTML 标签（可被点击、输入、选择的元素）
INTERACTIVE_TAGS = [
    'a',           # 链接
    'button',      # 按钮
    'input',       # 输入框
    'select',      # 下拉框
    'textarea',    # 文本域
    'details',     # 可折叠
    'summary',     # 可折叠标题
    'menuitem',    # 菜单项
]

# 可输入的 HTML 标签
INPUT_TAGS = [
    'input',
    'textarea',
    'select',
]

# 可点击的 HTML 标签
CLICKABLE_TAGS = [
    'a',
    'button',
    'input',
    'details',
    'summary',
    'menuitem',
]

# ARIA role 映射
ROLE_TAG_MAP = {
    'link': 'a',
    'button': 'button',
    'textbox': 'input',
    'searchbox': 'input',
    'checkbox': 'input',
    'radio': 'input',
    'menuitem': 'menuitem',
}

# 区域 ID 命名
REGION_ID_HEADER = 'header'
REGION_ID_MAIN = 'main'
REGION_ID_SIDEBAR = 'sidebar'
REGION_ID_FOOTER = 'footer'
REGION_ID_NAV = 'nav'

# 默认配置
DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0
DEFAULT_TIMEOUT = 10

# ref 前缀
REF_PREFIX = 'r'

# 状态文件扩展名
STATE_FILE_EXTENSION = '.state.json'