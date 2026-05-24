# RootBrowse：让 AI 直接操控浏览器

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
pip install rootbrowse-mcp
```

没有 chromedriver，没有几百兆的 playwright install，就一个包。

## 工作流程

```
1. init_browser()           → 初始化（秒开）
2. get_page(url)            → 打开任意网页
3. get_page_regions()       → AI 看到页面有哪些区块
4. match_element(...)       → AI 筛选出想操作的元素
5. run_js(ele.click())      → 执行操作（点击/输入/滚动/...）
```

AI 每次只拿到需要的那部分信息，不会被海量 DOM 节点淹没。

## 为什么不用传统框架

| | Selenium | Playwright | RootBrowse |
|---|---|---|---|
| 安装大小 | 上百 MB（chromedriver） | 几百 MB（playwright） | 几 MB |
| 操作方式 | click() 封装 | click() 封装 | run_js() |
| React 页面 | 容易失效 | 容易失效 | JS 直接操作，稳定 |
| 数据返回 | 全量 DOM | 全量 DOM | 渐进式探索 |
| 定位方式 | CSS selector | CSS selector | xpath 实时 |

Selenium 的 click() 在 React 输入框上经常失效。RootBrowse 让 AI 直接用 JS 操作，最底层的东西最可靠。

## 适用场景

- **AI 助手操控浏览器** — 让 AI 帮你填表单、搜百度、点击按钮
- **网页数据抓取** — AI 判断页面结构，按需提取内容
- **自动发帖/回帖** — 论坛、社交平台的自动化操作

## 技术栈

- Python >= 3.10
- DrissionPage（底层 CDP，直接控制 Chrome，不需要 driver）
- FastMCP（MCP 协议，AI 操控浏览器的标准方式）

## 怎么配置到 Claude Code

安装后，在 `C:\Users\你的用户名\.claude.json` 里添加：

```json
{
  "mcpServers": {
    "RootBrowseMCP": {
      "command": "python",
      "args": ["-m", "rootbrowse_mcp.server"]
    }
  }
}
```

重启 Claude Code，就能用这些工具操控浏览器：

- `get_page_regions()` — 看页面有哪些区块
- `match_element(...)` — 筛选元素
- `run_js(...)` — 执行任意 JS 操作

---

GitHub: https://github.com/zimvir/RootBrowse

有问题欢迎提 issue。