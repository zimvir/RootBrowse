# RootBrowse

## 项目定位

Python 浏览器自动化 MCP 框架，为 AI Agent 提供结构化的浏览器交互能力。基于 DrissionPage 构建。

## 解决什么问题

| 问题 | 现状 | RootBrowse |
|------|------|------------|
| DOM 超限 | 复杂页面直接报错 | 区域化拆分 + 截图兜底 |
| 点击不精确 | 文字匹配模糊，点击错位置 | ref 引用精确点击 |
| 信息噪音大 | 原始 DOM 转储，AI 无法处理 | 可交互元素树（无噪音） |
| 搜索场景弱 | 返回单节点 | 结构化搜索结果列表 |
| 状态管理 | 每次重新登录 | save/load state |

**本质：让 AI Agent 能稳定、准确地操作浏览器。**

---

## 核心概念

### ref（内部引用 ID）

HTML 元素大多数没有 `id` 属性。RootBrowse 为每个可交互元素生成 `ref`（r1, r2, r3...），作为内部引用。

```python
# 原始 HTML: <a href="/python">Python 入门</a>
# 生成 ref 后
Element(ref="r1", tag="a", text="Python 入门", xpath="...", attrs={...})
```

AI 用 `ref` 操作元素，不依赖原始 HTML 的 id 或文字匹配。

### 区域化拆分

页面 DOM 有几千个节点，直接给 AI 无法处理。RootBrowse 按语义区块拆分：

```
页面 DOM
    ↓ 按语义区域分组（header, main, sidebar 等）
    ↓ 过滤噪音（script, style, meta）
    ↓ 统计每个区域的节点数
返回：Region 列表，AI 选择进入哪个区域
```

### 渐进式获取

```
get_regions()           → 看有哪些区块
get_region_summary()     → 看区块统计（tag 分布）
match_element()           → 按条件筛选元素（摘要）
get_element()             → 最后才看完整信息
```

每一步都返回精简数据，AI 按需逐步深入。

### TabManager 状态自管理

TabManager **不依赖 DrissionPage API 查询标签页列表**，自身维护状态：

- `_tabs` — 所有标签页信息 `[{url, title}, ...]`
- `_current_index` — 当前标签页索引

每次调用 DrissionPage 方法后，同步更新内部状态。

---

## AI 工作流

### 核心流程

```
用户指令 → get_regions() → get_region_summary() → match_element() → get_element() → ElementOperator 操作
```

### 具体例子

**场景：在新闻网站搜索"Python"文章**

```
1. get_regions()
   → [Region(id="header", node_count=15), Region(id="main", node_count=347), ...]

2. get_region_summary("main")
   → {count: 347, tag_counts: {a: 280, button: 23, input: 12}, role_counts: {link: 280, button: 23}}

3. match_element("main", tag="a", text_contains="Python", limit=20)
   → [{ref: "r5", text: "Python 入门", attrs_preview: {href: "/python"}}, ...]

4. get_element("r5")
   → Element(ref="r5", tag="a", role="link", text="Python 入门", xpath="...", attrs={...})

5. ElementOperator.click("r5")
   → {success: true, new_url: "...", error: null}
```

**场景：截图兜底**

```
操作后页面崩溃 / DOM 超限
    ↓
screenshot(annotate=[[x1,y1,x2,y2]])
    ↓
返回 base64 图片，高亮标注指定区域
AI 从截图看页面状态，不依赖 DOM
```

---

## 类结构

### TabManager — 标签页管理器

**职责**：管理浏览器标签页（新增、切换、关闭）

**内部状态**：

```python
_page         # DrissionPage 底层实例
_tabs         # [{url, title}, ...] 所有标签页信息
_current_index  # 当前标签页索引
```

**方法**：

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `new_tab` | `url: str` | `int` | 打开新标签页，返回索引 |
| `close_tab` | — | `None` | 关闭当前标签页 |
| `switch_to_tab` | `index: int` | `None` | 切换到指定标签页 |
| `tabs_count` | — | `int` | 返回标签页数量 |
| `current_index` | — | `int` | 返回当前标签页索引 |

---

### ElementOperator — 元素操作器

**职责**：对元素执行点击、输入、悬停等操作

**内部状态**：

```python
_element_map  # ref -> Element 映射表
```

**方法**：

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `click` | `ref: str` | `dict` | 通过 ref 精确点击 |
| `input_by_ref` | `ref: str, text: str, clear: bool = False` | `dict` | 向输入框写入文字 |
| `hover` | `ref: str` | `dict` | 悬停 |
| `double_click` | `ref: str` | `dict` | 双击 |
| `right_click` | `ref: str` | `dict` | 右键 |
| `submit` | `ref: str` | `dict` | 提交表单 |
| `clear` | `ref: str` | `dict` | 清空输入框 |
| `send_enter` | — | `None` | 发送回车键 |

**返回值格式**：`{success, new_url?, error?}`

---

### PageScanner — 页面扫描器

**职责**：获取页面结构化信息（区块、元素摘要、完整元素）

**内部状态**：

```python
_page         # DrissionPage 底层实例
_element_map  # ref -> Element 映射表
```

**方法**：

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `get_regions` | — | `list[Region]` | 返回页面语义区块列表 |
| `get_region_summary` | `region_id: str` | `dict` | 返回区域统计摘要 |
| `match_element` | 见下表 | `list[dict]` | 按条件筛选元素摘要 |
| `get_element` | `ref: str` | `Element` | 返回完整元素信息 |
| `find_element` | `by, value, filter` | `Element \| None` | 多维度精确定位 |

**match_element 参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `region_id` | `str \| list[str] \| None` | 搜索区域，可单选/多选/全选 |
| `query` | `str \| None` | 关键词搜索 |
| `tag` | `str \| None` | HTML 标签筛选 |
| `role` | `str \| None` | ARIA role 筛选 |
| `text_contains` | `str \| None` | 文字包含筛选 |
| `limit` | `int = 20` | 最多返回数量 |
| `offset` | `int = 0` | 分页偏移 |

**返回值"元素摘要"结构**：
```python
{"ref": "r1", "text": "文章标题", "attrs_preview": {"href": "/article/1"}}
```

**get_region_summary 返回值结构**：
```python
{
    "count": 347,
    "tag_counts": {"a": 280, "button": 23, "input": 12},
    "role_counts": {"link": 280, "button": 23},
    "text_preview": [{"tag": "a", "text": "标题1", "ref": "r1"}, ...]
}
```

---

### Browse — 主入口

**职责**：组合 TabManager、ElementOperator、PageScanner，提供统一入口

**方法**：

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `get` | `url: str` | `dict` | 打开 URL，返回 {url, title} |
| `screenshot` | `path, annotate` | `str` | 截图，可高亮标注区域 |
| `save_state` | `path: str` | `None` | 保存 cookies + localStorage |
| `load_state` | `path: str` | `None` | 恢复会话状态 |

**AI 调用方式**：

```python
browser.tabs.new_tab('https://example.com')  # TabManager
browser.page.get_regions()                    # PageScanner
browser.act.click('r1')                       # ElementOperator
```

---

## 数据类型

### Region（页面区块）

```python
Region(
    id="main",           # 区块 ID
    label="主内容",       # 人类可读名称
    node_count=347        # 可交互元素数量
)
```

### Element（可交互元素）

```python
Element(
    ref="r1",            # 内部引用 ID
    tag="a",             # HTML 标签
    role="link",         # ARIA role
    text="文章标题",     # 显示文字
    xpath="/html/body/div[2]/a",  # 元素路径
    attrs={"href": "/article/1", "target": "_blank"}
)
```

### 返回值 dict

| 方法 | 返回结构 |
|------|---------|
| `get` | `{url, title}` |
| `screenshot` | 文件路径或 base64 字符串 |
| `click` | `{success, new_url, error}` |
| `input_by_ref` | `{success, error}` |
| `get_region_summary` | `{count, tag_counts, role_counts, text_preview}` |
| `match_element` | `[{ref, text, attrs_preview}, ...]` |

---

## 目录结构

```
src/RootBrowse/src/rootbrowse/
├── __init__.py          # 包导出
├── _version.py          # 版本信息
├── browser.py           # Browse 主类
├── tab_manager.py       # TabManager 类
├── element_operator.py  # ElementOperator 类
├── page_scanner.py      # PageScanner 类
├── types.py             # Region, Element 数据类
├── constants.py         # 可交互标签列表等常量
└── exceptions.py        # 自定义异常
```

---

## 技术选型

- **底层引擎**: DrissionPage（Python CDP 连接，无需驱动）
- **MCP 框架**: FastMCP（官方 Python MCP SDK）
- **Python 版本**: >= 3.10

---

## 开发状态

**当前阶段：实现完成**

- [x] project_tree.json — 类结构定义（JSON Schema）
- [x] types.py — Region, Element 数据类
- [x] constants.py — 可交互标签列表
- [x] exceptions.py — 自定义异常
- [x] tab_manager.py — TabManager 实现
- [x] element_operator.py — ElementOperator 实现
- [x] page_scanner.py — PageScanner 实现
- [x] browser.py — Browse 主类实现
- [x] _version.py — 版本信息
- [x] __init__.py — 包导出