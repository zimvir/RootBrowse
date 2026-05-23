# Changelog

## [0.2.1] - 2026-05-23

### Fixed

- **close_browser 异常处理** — 增强异常处理避免 NoneType 属性错误
  - 多层 try-except 包裹

## [0.2.0] - 2026-05-23

### Breaking Changes

- **移除 ref 机制** — 所有元素定位改为直接使用 xpath
  - `get_element(ref)` → `get_element(xpath)`
  - `click_element(ref)` → `click_element(xpath)`
  - `input_text(ref, text)` → `input_text(xpath, text)`
  - `match_element()` 返回 `{xpath, text, attrs_preview}` 而不是 `{ref, ...}`

### Added

- **run_js(code, args)** — 在浏览器端执行 JavaScript
  - 绕过 DOM 传输限制，长文本分段提取
  - args 为 JSON 字符串格式

### Changed

- 适配 rootbrowse 0.4.0：移除 ref 相关逻辑
- `get_page_regions()` 返回 `{xpath, label}` 而不是 `{id, label}`

## [0.1.4] - 2026-05-17

- 适配 rootbrowse 0.3.2：wait.doc_loaded() 兼容

## [0.1.3] - 2026-05-17

- 更新依赖： rootbrowse（>= 0.3.0） -> rootbrowse（>= 0.3.1）
- 使用指南: get_guide() MCP tool + 独立 guide.py

## [0.1.2] - 2026-05-17

- 更新依赖： rootbrowse（>= 0.2.0） -> rootbrowse（>= 0.3.0）

## [0.1.1] - 2026-05-17

### Changed

- **浏览器初始化** — 新增 `init_browser(headless)` tool，必选
- 其他 tools 需要先调用 `init_browser()` 才能使用

## [0.1.0] - 2026-05-17

### Added

- **server.py** — FastMCP Server 入口
- **tools.py** — 15 个 MCP Tools

#### Tools 列表

- **页面扫描**: `get_page_regions`, `get_region_summary`, `match_element`, `get_element`
- **元素操作**: `click_element`, `input_text`, `send_enter`
- **浏览器**: `get_page`, `take_screenshot`, `close_browser`
- **标签页**: `new_tab`, `close_tab`, `switch_tab`, `get_tabs_count`
- **状态**: `save_state`, `load_state`