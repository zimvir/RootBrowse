# RootBrowse

**AI Agent 的浏览器** — 一个 AI 可以直接操控的浏览器。

## 它解决什么问题？

传统浏览器自动化（Selenium/Playwright）是为了**人操作浏览器**设计的：先写脚本，跑完结束。AI 时代需要的是**让 AI 实时操控浏览器**——AI 说"点这个按钮"，浏览器就要立刻响应。

RootBrowse 为 AI 重新设计：

| | 传统自动化测试 | RootBrowse |
|---|---|---|
| 目标 | 跑完脚本，输出报告 | AI 实时操控 |
| 定位方式 | CSS selector（易失效） | xpath 直接操作 DOM |
| 返回数据 | 全量 DOM（海量噪声） | 渐进式（区块→统计→元素） |
| 操作接口 | click/input 封装（不可靠） | run_js 万能接口 |
| 适用场景 | 回归测试 | AI Agent 实时交互 |

**核心区别**：传统框架是给人用的，RootBrowse 是给 AI 用的。

## MCP 快速开始

### 配置 Claude Code


#### step 1

```
pip install rootbrowse-mcp
```

#### step 2

在 `C:\Users\你的用户名\.claude.json` 的 `mcpServers` 中添加：

```json
{
  "mcpServers": {
    "RootBrowseMCP": {
      "command": "python.exe",
      "args": ["-m", "rootbrowse_mcp.server"]
    }
  }
}
```
"command" 里需要填电脑里真实的 python 解释器路径(此解释器的环境必须已下载 rootbrowse-mcp)

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

## MCP 工具（11 个）

| 类别 | 工具 | 说明 |
|---|---|---|
| 页面扫描 | `get_page_regions()` | 获取页面语义区域 |
| | `get_region_summary(xpath)` | 区域统计 |
| | `match_element(...)` | 按条件筛选元素 |
| 浏览器 | `init_browser(headless)` | 初始化（必选） |
| | `get_page(url)` | 打开 URL |
| | `take_screenshot(path)` | 截图 |
| | `close_browser()` | 关闭浏览器 |
| | `run_js(code, args)` | 执行 JavaScript |
| 标签页 | `new_tab(url)` | 新建标签页 |
| | `close_tab()` | 关闭标签页 |
| | `switch_tab(index)` | 切换标签页 |
| 状态 | `save_state(path)` | 保存会话 |
| | `load_state(path)` | 恢复会话 |

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

## 安装

```bash
pip install rootbrowse-mcp
```

## 技术栈

- Python >= 3.10
- [DrissionPage](https://github.com/g18792951860/DrissionPage) — 底层 CDP 引擎

## License

MIT