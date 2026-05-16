# RootBrowse

Python 浏览器自动化 MCP 框架，为 AI Agent 提供结构化的浏览器交互能力。基于 DrissionPage 构建。

## 核心特性

- **区域化拆分** — 将页面 DOM 按语义区块分组，解决复杂页面的信息过载问题
- **ref 精确引用** — 为每个可交互元素生成内部 ID (r1, r2, r3...)，避免文字匹配的不确定性
- **渐进式获取** — get_regions → get_region_summary → match_element → get_element，按需逐步深入
- **TabManager 状态自管理** — 内部维护标签页状态，不依赖 DrissionPage API 查询

## 安装

```bash
pip install rootbrowse
```

## 快速开始

```python
from DrissionPage import ChromiumPage
from rootbrowse import Browser

# 创建浏览器实例
page = ChromiumPage()
browser = Browser(page)

# 打开网页
browser.get('https://example.com')

# 获取页面区块
regions = browser.view.get_regions()
print(regions)  # [Region(id='main', label='主内容', node_count=100), ...]

# 获取区块统计摘要
summary = browser.view.get_region_summary('main')
print(f"元素数量: {summary.count}")

# 按条件筛选元素
elements = browser.view.match_element(tag='a', text_contains='Python', limit=20)
print(elements)  # [ElementPreview(ref='r5', text='Python 入门', ...), ...]

# 获取完整元素信息
ele = browser.view.get_element('r5')
print(f"点击: {ele.text} -> {ele.attrs['href']}")

# 执行操作
result = browser.act.click('r5')
print(f"点击结果: {result.success}")

# 关闭浏览器
browser.close()
```

## AI 工作流

```
用户指令
    ↓
get_regions()              → 查看页面有哪些区块
get_region_summary(id)     → 查看区块统计（标签分布、role 分布）
match_element(id, ...)     → 按条件筛选元素（摘要列表）
get_element(ref)          → 获取元素完整信息
ElementOperator 操作      → 点击、输入、悬停等
```

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

## API 概览

### Browse — 主入口

```python
browser.get(url)                  # 打开 URL
browser.screenshot(path)          # 截图
browser.save_state(path)          # 保存会话状态
browser.load_state(path)          # 恢复会话状态
browser.close()                   # 关闭浏览器
```

### TabManager — 标签页管理

```python
browser.tabs.new_tab(url)         # 新建标签页
browser.tabs.close_tab(index)     # 关闭标签页
browser.tabs.switch_to_tab(index) # 切换标签页
browser.tabs.tabs_count()         # 获取标签页数量
browser.tabs.current_index()     # 获取当前索引
```

### PageScanner — 页面扫描

```python
browser.view.get_regions()                    # 获取区块列表
browser.view.get_region_summary(region_id)    # 获取区块统计
browser.view.match_element(**filters)         # 筛选元素
browser.view.get_element(ref)                # 获取完整元素
browser.view.find_element(by, value)         # 精确定位
```

### ElementOperator — 元素操作

```python
browser.act.click(ref)              # 点击
browser.act.input_by_ref(ref, text) # 输入
browser.act.hover(ref)             # 悬停
browser.act.double_click(ref)      # 双击
browser.act.right_click(ref)       # 右键
browser.act.submit(ref)            # 提交表单
browser.act.clear(ref)             # 清空输入框
browser.act.send_enter()            # 发送回车
```

## 数据类型

| 类型 | 说明 |
|------|------|
| `Region` | 页面语义区块 `{id, label, node_count}` |
| `Element` | 可交互元素 `{ref, tag, role, text, xpath, attrs}` |
| `RegionSummary` | 区域统计 `{count, tag_counts, role_counts, text_preview}` |
| `ElementPreview` | 元素摘要 `{ref, text, attrs_preview}` |
| `OperationResult` | 操作结果 `{success, error?, new_url?}` |

## 异常

| 异常 | 说明 |
|------|------|
| `BrowserError` | 浏览器相关错误 |
| `ElementNotFoundError` | 元素未找到 |
| `RegionNotFoundError` | 区域未找到 |
| `TabNotFoundError` | 标签页未找到 |
| `OperationError` | 操作失败 |
| `StateFileError` | 状态文件错误 |
| `PageLoadError` | 页面加载失败 |

## 技术栈

- **底层引擎**: [DrissionPage](https://github.com/g18792951860/DrissionPage) — Python CDP 连接，无需驱动
- **MCP 框架**: FastMCP（官方 Python MCP SDK）
- **Python 版本**: >= 3.10

## License

MIT
