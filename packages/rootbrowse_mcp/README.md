# RootBrowse MCP

MCP Server for RootBrowse browser automation framework. 为 AI Agent 提供结构化的浏览器操控能力。

## 安装

```bash
pip install rootbrowse-mcp
```

## Claude Code 配置

在 `settings.json` 中添加：

```json
{
  "mcpServers": {
    "rootbrowse": {
      "command": "rootbrowse-mcp"
    }
  }
}
```

或指定路径：

```json
{
  "mcpServers": {
    "rootbrowse": {
      "command": "D:\\path\\to\\.venv\\Scripts\\python.exe",
      "args": ["-m", "rootbrowse_mcp.server"]
    }
  }
}
```

## Tools

### 页面扫描
- `get_page_regions()` — 获取页面所有语义区域
- `get_region_summary(region_xpath)` — 获取区域统计摘要
- `match_element(region_xpath, tag, role, text_contains, query, limit)` — 按条件筛选元素
- `get_element(xpath)` — 获取元素完整信息

### 元素操作
- `click_element(xpath)` — 点击元素
- `input_text(xpath, text, clear)` — 向输入框输入文字
- `send_enter()` — 发送回车键

### 浏览器
- `init_browser(headless)` — 初始化浏览器（必选，headless 默认 True）
- `get_page(url, timeout)` — 打开 URL
- `take_screenshot(path)` — 页面截图
- `close_browser()` — 关闭浏览器
- `run_js(code, args)` — 在浏览器端执行 JavaScript

**注意：** 使用其他工具前必须先调用 `init_browser()` 初始化浏览器。

### 标签页
- `new_tab(url)` — 打开新标签页
- `close_tab()` — 关闭当前标签页
- `switch_tab(index)` — 切换标签页
- `get_tabs_count()` — 获取标签页数量

### 状态
- `save_state(path)` — 保存浏览器状态
- `load_state(path)` — 恢复浏览器状态

## 数据类型

### Region（区域）
```
{xpath, label}
```

### Element（元素）
```
{tag, role, text, xpath, attrs}
```

### ElementPreview（元素摘要）
```
{xpath, text, attrs_preview}
```

## run_js 特殊用法

绕过 DOM 传输限制获取长文本：

```
run_js("return document.body.innerText.substring(0, 2000)")
run_js("return document.body.innerText.substring(2000, 5000)")
```

## 依赖

- Python >= 3.10
- rootbrowse >= 0.4.0
- mcp >= 1.0.0