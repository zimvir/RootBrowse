# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.7.0] - 2026-06-06

### Fixed

- **--headless=new 改为 --headless** — DrissionPage auto_port() 在 Chrome 145 下与 `--headless=new` 不兼容，WebSocket 握手失败，改用旧版 `--headless` 参数
- **take_screenshot() 修复** — 之前调用不存在的 `page.screenshot()` 方法，改为 `_get_screenshot(as_base64=True)` 返回 base64

## [0.6.1] - 2026-06-06

### Changed

- **auto_port() 独立浏览器** — `Browser.__init__` 调用 `opts.auto_port()`，每个进程自动分配独立端口，多 Agent 并行不干扰
- **模块重命名** — `page_scanner` → `view`，`element_operator` → `operation`，`tab_manager` → `tab`

## [0.6.0] - 2026-06-06

### Changed

- **合并 rootbrowse-mcp 到主包** — 单一包 `rootbrowse`，含 MCP server
  - `packages/rootbrowse/` → `rootbrowse/core/`
  - `packages/rootbrowse-mcp/` → `rootbrowse/mcp/`
  - 版本统一为 0.6.0
  - `rootbrowse-mcp` 命令保留

## [0.5.1] - 2026-05-23

### Fixed

- **TabManager DrissionPage 4.x 兼容** — API 变更
  - `tab_ids()` → `tab_ids` property
  - `tab_id()` → `tab_id` property
  - `to_tab()` → `activate_tab()`

## [0.5.0] - 2026-05-23

### Changed

- **ElementOperator 全 JS 化** — 所有操作改用 JS 实现
  - `click()` → JS `ele.click()`
  - `hover()` → JS `dispatchEvent(mouseover)`
  - `double_click()` → JS `dispatchEvent(dblclick)`
  - `right_click()` → JS `dispatchEvent(contextmenu)`
  - `submit()` → JS `ele.form.submit()`
  - `clear()` → JS `ele.value = ''`
  - 只有 `input_by_xpath()` 保留 DrissionPage（需要处理中文输入法）

- **PageScanner._detect_regions() 改为 JS** — 一次 `run_js` 获取所有区域

## [0.4.1] - 2026-05-23

### Fixed

- **close_browser 异常处理** — 增强异常处理避免 NoneType 属性错误
  - 多层 try-except 包裹，即使 `_browser._page` 为 None 或已关闭也不会报错

- **match_element 性能优化** — 用 JS 一次性查询替代逐元素 CDP 往返
  - `_query_elements_in_region()` 改为 `run_js` 单次 CDP 往返
  - 区域内所有标签一次查询：`querySelectorAll("a,button,input,...")`
  - 内部实现 `getXPath()` 生成 xpath，不再依赖 DrissionPage

## [0.4.0] - 2026-05-23

### Breaking Changes

- **移除 ref 机制** — 所有元素定位改为直接使用 xpath，不再维护快照式 ref
  - `Element.ref` 字段删除
  - `ElementPreview.ref` 字段删除
  - `Region.id` 改为 `Region.xpath`
  - 所有工具参数从 `ref` 改为 `xpath`
  - 解决了动态页面（懒加载、SPA）上 ref 缓存 xpath 过期失效的问题

### Added

- **run_js 方法** — 在浏览器端执行 JavaScript
  - `browser.run_js(code, *args)` — 返回 JS 执行结果
  - 绕过 DOM 传输限制，长文本分段提取：`innerText.substring(0, 2000)`
  - MCP tool：`run_js(code, args)` — args 为 JSON 字符串格式

### Changed

- **PageScanner 改为实时查询** — 不再依赖预扫描缓存
- **ElementOperator 简化** — 删除 ref 解析逻辑
- **TabManager 实时同步** — `_tabs` 属性委托 DrissionPage.tab_ids()

## [0.3.2] - 2026-05-17

### Fixed

- **DrissionPage 4.x 兼容** — `wait.ready()` 被移除
  - 替换为 `wait.doc_loaded()`，等待文档加载完成

## [0.3.1] - 2026-05-17

### Fixed

- **close_browser 无限递归** — 本地函数改名为 `_close_browser()`
- **switch_tab / close_tab API 错误** — DrissionPage 4.x API 变更
- **动态JS页面内容缺失** — 添加等待策略

## [0.3.0] - 2026-05-17

### Added

- **惰性扫描缓存** — 元素扫描结果缓存，避免重复扫描
- **全局 ref 计数器** — 统一元素 ref 生成逻辑

### Changed

- **`get_regions()` 性能优化** — 不再扫描元素，只检测区域
- **`_scan_elements()` 优化** — 6 次查询代替 30 次

## [0.2.0] - 2026-05-16

### Added

- **区域识别** — `browser.page` → `browser.view`，body 直接子元素动态检测
- **save_state / load_state** — cookies 序列化到 JSON 文件

## [0.1.0] - 2026-05-10

### Added

- **完整核心功能** — Browser、View、Tab、Operation、types、exceptions
- **124 tests** covering all modules