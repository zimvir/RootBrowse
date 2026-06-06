# RootBrowse

## 项目定位

Python 浏览器自动化 MCP 框架，为 AI Agent 提供结构化的浏览器交互能力。基于 DrissionPage 构建。

## 解决什么问题

| 问题 | 现状 | RootBrowse |
|------|------|------------|
| DOM 超限 | 复杂页面直接报错 | 区域化拆分 + 截图兜底 |
| 点击不精确 | `click_by_containing_text` 模糊匹配 | ref 引用精确点击 |
| 信息噪音大 | 原始 DOM 转储 | 可交互元素树（无噪音） |
| 搜索场景弱 | 返回单节点 | 结构化搜索结果列表 |
| 状态管理 | 每次重新登录 | save/load state |

**本质：让 AI Agent 能稳定、准确地操作浏览器。**

## 核心价值

**信息密度优先** — 不是把 DOM 整个吐给 AI，而是转换成 AI 友好的结构：
- 可交互元素组成的树（而非完整 DOM）
- 搜索返回 `{title, url, snippet, xpath, ref}` 列表
- 页面按语义区块拆分，不用一次全量获取
- 截图作为降级兜底方案

**渐进式获取** — 先拿高层概览，必要时再深入。

---

## 整体工作流

```
用户（AI Agent）
    │
    │ "帮我登录 Twitter"
    │
    ▼
MCP Server 接收请求
    │
    │ get_page_regions()
    │ → 返回页面有哪些区块
    │
    ▼
AI 看到：sidebar(导航), main(登录框), header(Logo)
    │
    │ get_region_tree("main")
    │ → 返回该区域的可交互元素
    │
    ▼
AI 看到：
  r1: input[type="text"]  → 用户名
  r2: input[type="password"] → 密码
  r3: button[type="submit"] → 登录
    │
    │ input_by_ref("r1", "user@example.com")
    │
    │ input_by_ref("r2", "password")
    │
    │ click("r3")
    │
    ▼
页面跳转 / 登录成功 or 失败
    │
    │ save_state() → 保存登录态
    │
    ▼
完成
```

---

## AI Agent 完整决策示例

```
Task: 在 Twitter 搜索"AI 新闻"

1. get_page_regions()
   → 页面分区概览

2. AI 判断：搜索框在 header 区域
   → get_region_tree("header")

3. AI 找到搜索输入框的 ref
   → search_input_ref

4. input_by_ref(search_input_ref, "AI 新闻")

5. send_enter() / 或找搜索按钮 click()

6. get_page_regions()  → 确认进入搜索结果页

7. search("AI 新闻") → 返回结构化搜索结果列表

8. AI 选择要点击的结果 ref
   → click(result_ref)
```

---

## 核心循环

```
AI 发出指令
    │
    ▼
MCP Tool 执行
    │
    ▼
返回结构化结果
    │
    ▼
AI 决策
    │
    ▼
下一条指令
    │
    ▼
...循环直到任务完成
```

---

## Tool 与返回值

| Tool | 返回 |
|------|------|
| `get_page_regions()` | `[{region_id, label, node_count}]` |
| `get_region_tree(id)` | `{nodes: [{ref, tag, role, text, xpath}]}` |
| `search(query)` | `[{ref, title, url, snippet}]` |
| `find_element()` | `{ref, tag, role, text, xpath, attrs}` |
| `click(ref)` | `{success, new_url, error}` |
| `screenshot()` | base64 / 文件路径 |

每一步的返回都是**精简的、可决策的**，不是原始 DOM。

---

## 架构

```
rootbrowse/
├── core/                      # 纯 Python，无 MCP 依赖
│   ├── src/rootbrowse_core/
│   │   ├── __init__.py
│   │   ├── browser.py        # 浏览器基础操作封装
│   │   ├── tree.py           # 结构化树构建（Accessibility-like）
│   │   ├── search.py         # 搜索结果解析
│   │   └── types.py          # 数据类型定义
│   ├── tests/
│   ├── pyproject.toml        # name="rootbrowse-core"
│   └── CHANGELOG.md
│
├── mcp/                       # MCP 层（协议转换）
│   ├── src/rootbrowse_mcp/
│   │   ├── __init__.py
│   │   ├── server.py         # MCP Server 入口
│   │   └── tools.py          # Tool 定义
│   ├── tests/
│   ├── pyproject.toml        # name="rootbrowse-mcp"
│   └── CHANGELOG.md
│
└── pyproject.toml             # workspace 定义（PDM/uv）
```

---

## 版本管理

- 每个包独立版本号（`rootbrowse-core`、`rootbrowse-mcp`）
- Git 标签前缀区分：`core@v1.0.0`、`mcp@v0.1.0`
- 各自独立发布 PyPI

---

## 技术选型

- **底层引擎**: DrissionPage（Python CDP 连接，无需驱动）
- **MCP 框架**: FastMCP（官方 Python MCP SDK）
- **Python 版本**: >= 3.10

---

## 对比

| | Playwright MCP | DrissionPageMCP | RootBrowse |
|--|----------------|-----------------|------------|
| 语言 | Node.js | Python | Python |
| 信息载体 | Accessibility Tree | 原始 DOM | 结构化树 + 区域化 |
| 搜索 | 无 | 模糊匹配 | 结构化结果 |
| 截断处理 | — | 报错 | 区域化拆分 + 截图兜底 |

---

## 开发状态

**当前阶段：规划中**

核心模块尚未实现，按优先级排序：
1. `core/tree.py` — 结构化树构建
2. `core/search.py` — 搜索结果解析
3. `mcp/tools.py` — Tool 定义与注册
4. `mcp/server.py` — Server 启动