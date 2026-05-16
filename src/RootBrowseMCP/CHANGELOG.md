# Changelog

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