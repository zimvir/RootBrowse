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

# 区域检测时忽略的标签（不是区域，不扫描其中元素）
REGION_NOISE_TAGS = {'script', 'style', 'meta', 'noscript', 'textarea', 'input'}

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

# 元素属性预览需要保留的 key
KEY_ATTRS_PREVIEW = ['href', 'src', 'alt', 'title', 'name', 'type', 'value']

# 区域标签关键词映射 (id/class 关键词 -> 显示名称)
REGION_LABEL_KEYWORDS = {
    'header': '页头',
    'nav': '导航',
    'menu': '菜单',
    'sidebar': '侧边栏',
    'aside': '侧边栏',
    'main': '主内容',
    'content': '内容区',
    'body': '主体',
    'footer': '页脚',
    'search': '搜索',
    'result': '结果',
    'wrapper': '容器',
    'container': '容器',
    'hd': '页头',
    'ft': '页脚',
}

# HTML 标签默认显示名称
TAG_LABELS = {
    'div': '区块',
    'span': '行内',
    'section': '分区',
    'article': '文章',
    'header': '页头',
    'footer': '页脚',
}

# 状态文件扩展名
STATE_FILE_EXTENSION = '.state.json'