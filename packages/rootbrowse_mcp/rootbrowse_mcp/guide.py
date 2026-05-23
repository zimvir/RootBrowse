"""MCP 使用指南"""

MCP_GUIDE = """# RootBrowseMCP 使用指南

## 初始化
1. init_browser(headless=True) — 初始化浏览器（必须先调用）
   - headless=True: 无头模式（默认）
   - headless=False: 有头浏览器

## 基本工作流
init_browser() → get_page(url) → get_page_regions() → match_element(...) → get_element(xpath) → click_element(xpath)

## 工具列表

### 浏览器
- init_browser(headless) — 初始化浏览器
- get_page(url, timeout) — 打开URL
- take_screenshot(path) — 截图
- close_browser() — 关闭浏览器
- run_js(code, args) — 在浏览器端执行 JavaScript

### 页面扫描
- get_page_regions() — 获取页面区域列表
- get_region_summary(region_xpath) — 获取区域统计摘要
- match_element(region_xpath, tag, role, text_contains, query, limit) — 按条件筛选元素
- get_element(xpath) — 获取元素完整信息

### 元素操作
- click_element(xpath) — 点击元素
- input_text(xpath, text, clear) — 向输入框输入文字
- send_enter() — 发送回车

### 标签页
- new_tab(url) — 打开新标签页
- close_tab() — 关闭当前标签页
- switch_tab(index) — 切换标签页
- get_tabs_count() — 获取标签页数量

### 状态
- save_state(path) — 保存浏览器状态（cookies）
- load_state(path) — 恢复浏览器状态

## 数据类型

### Region（区域）
{xpath, label}

### Element（元素）
{tag, role, text, xpath, attrs}

### ElementPreview（元素摘要）
{xpath, text, attrs_preview}

### OperationResult（操作结果）
{success, error?, new_url?}

## xpath 使用说明

所有元素操作使用 xpath 定位，直接查询实时 DOM，不会过期。

### 获取 xpath 的方式
1. get_page_regions() → 返回 region xpath
2. match_element(...) → 返回 {xpath, text, attrs_preview}
3. 直接手写 xpath

### run_js 特殊用法
绕过 DOM 传输限制获取长文本：
- run_js("return document.body.innerText.substring(0, 2000)")
- run_js("return document.body.innerText.substring(2000, 5000)")
"""