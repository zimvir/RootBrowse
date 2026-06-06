# RootBrowse

**AI Agent 的浏览器** — 一个 AI 可以直接操控的浏览器。

## 它解决什么问题？

AI 时代，浏览器应该是 AI 的工具。但现在的方案有两个问题：

**1. 能让 AI 操控的浏览器方案太少了**

大部分浏览器自动化框架（Selenium/Playwright）设计目标是给人写脚本用的，不是给 AI 实时操控的。

**2. 安装太重了**

Selenium 要下载 ChromeDriver，Playwright 要安装几百兆的驱动包。跑一个测试先花半小时装环境。

---

RootBrowse 就是来解决这两个痛点的：

- **零驱动** — 基于 DrissionPage，直接用 CDP 控制 Chrome，不需要任何 driver
- **AI 优先** — 专为 AI 实时操控设计，不是给人类写脚本用的

## 安装只需要一行

```bash
pip install rootbrowse
```

没有 chromedriver，没有几百兆的 playwright install，就一个包。

## 对比

| | Selenium | Playwright | RootBrowse |
|---|---|---|---|
| 安装大小 | 上百 MB（chromedriver） | 几百 MB（playwright） | 几 MB |
| 操作方式 | click() 封装 | click() 封装 | run_js() |
| React 页面 | 容易失效 | 容易失效 | JS 直接操作，稳定 |
| 数据返回 | 全量 DOM | 全量 DOM | 渐进式探索 |
| 定位方式 | CSS selector | CSS selector | xpath 实时 |
| AI 友好度 | 低 | 低 | 高 |

**核心区别**：传统框架是给人用的，RootBrowse 是给 AI 用的。

## MCP 快速开始

### 配置 Claude Code

在 `C:\Users\你的用户名\.claude.json` 的 `mcpServers` 中添加：

```json
{
  "mcpServers": {
    "RootBrowse": {
      "type": "stdio",
      "command": "python.exe",
      "args": ["-m", "rootbrowse.mcp.server"]
    }
  }
}
```

`command` 需要填电脑里真实的 python 解释器路径（此解释器的环境必须已安装 rootbrowse）。

### AI 工作流

```
init_browser()                    → 初始化浏览器
get_page(url)                     → 打开页面
get_page_regions()                 → 查看有哪些区块
get_region_summary(xpath)          → 查看区块统计
match_element(...)                 → 筛选目标元素
run_js(...)                       → 万能操作（点击/输入/滚动...）
```

## Python 库快速开始

```python
from rootbrowse import Browser

browser = Browser()
browser.get('https://example.com')

# 渐进式探索
regions = browser.view.get_regions()           # 看区块
summary = browser.view.get_region_summary(regions[0].xpath)  # 看统计
elements = browser.view.match_element(tag='a', limit=20)    # 筛选元素

# 万能操作
browser.run_js("document.evaluate('xpath=...', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue?.click()")

browser.close()
```

## 核心哲学

**封装层不可靠，run_js 是万能接口**。点击、输入、获取元素信息，都通过 `run_js` 完成，AI 自己决定何时用它。

## MCP 工具（15 个）

| 类别 | 工具 | 说明 |
|---|---|---|
| 页面扫描 | `get_page_regions()` | 获取页面语义区域 |
| | `get_region_summary(xpath)` | 区域统计 |
| | `match_element(...)` | 按条件筛选元素 |
| 浏览器 | `init_browser(headless)` | 初始化（必选） |
| | `get_page(url)` | 打开 URL |
| | `take_screenshot(path)` | 截图（返回文件路径或 base64） |
| | `close_browser()` | 关闭浏览器 |
| | `run_js(code, args)` | 执行 JavaScript |
| 标签页 | `new_tab(url)` | 新建标签页 |
| | `close_tab()` | 关闭标签页 |
| | `switch_tab(index)` | 切换标签页 |
| | `get_tabs_count()` | 获取标签页数量 |
| 状态 | `save_state(path)` | 保存会话 |
| | `load_state(path)` | 恢复会话 |
| 其他 | `get_guide()` | 获取 MCP 使用指南 |

## run_js 示例

```javascript
// 点击
var ele = document.evaluate("xpath=...", document, null,
    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (ele) ele.click();

// 输入
var ele = document.evaluate("xpath=...", document, null,
    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (ele) {
    ele.value = arguments[0];
    ele.dispatchEvent(new Event('input', {bubbles: true}));
}

// 长文本分段获取
return document.body.innerText.substring(0, 2000);
```

## 技术栈

- Python >= 3.10
- [DrissionPage](https://github.com/g18792951860/DrissionPage) — 底层 CDP 引擎
- FastMCP（MCP 协议实现）

## License

MIT