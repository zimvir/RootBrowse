"""MCP 使用指南"""

MCP_GUIDE = """# RootBrowseMCP 使用指南

## 初始化
1. init_browser(headless=True) — 初始化浏览器（必须先调用）
   - headless=True: 无头模式（默认）
   - headless=False: 有头浏览器

## 基本工作流
init_browser() → get_page(url) → get_page_regions() → match_element(...)

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

### 标签页
- new_tab(url) — 打开新标签页
- close_tab() — 关闭当前标签页
- switch_tab(index) — 切换标签页
- get_tabs_count() — 获取标签页数量

### 状态
- save_state(path) — 保存浏览器状态（cookies）
- load_state(path) — 恢复浏览器状态

## run_js 万能接口

所有元素操作都通过 run_js 完成，不单独封装。

### 常用操作示例

```python
# 点击元素
run_js('''
var ele = document.evaluate("xpath=...", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (ele) ele.click();
''')

# 输入文字
run_js('''
var ele = document.evaluate("xpath=...", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (ele) {
    ele.value = arguments[0];
    ele.dispatchEvent(new Event('input', {bubbles: true}));
}
''', "要输入的文字")

# 获取元素信息
run_js('''
var ele = document.evaluate("xpath=...", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
if (ele) return {tag: ele.tagName, text: ele.innerText, attrs: {...ele.attributes}};
''')
```

### xpath 获取方式
1. get_page_regions() → 返回 region xpath
2. match_element(...) → 返回 {xpath, text, attrs_preview}
3. 直接手写 xpath

### 绕过 DOM 传输限制
- run_js("return document.body.innerText.substring(0, 2000)")
- run_js("return document.body.innerText.substring(2000, 5000)")
"""