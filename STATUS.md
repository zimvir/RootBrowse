# RootBrowse 项目状态

## 当前版本

| 包 | 版本 | 状态 |
|---|---|---|
| rootbrowse | 0.5.1 | 核心库 |
| rootbrowse-mcp | 0.4.0 | MCP Server |

## 架构

```
AI Agent (Claude Code)
    ↓ MCP (11 个工具)
rootbrowse-mcp
    ↓
rootbrowse (核心库)
    ↓
DrissionPage (底层 CDP 引擎)
```

## 核心设计

1. **run_js 是万能接口** — 不做不可靠的封装层，agent 直接用 JS 操作浏览器
2. **渐进式页面探索** — get_regions → get_region_summary → match_element → run_js
3. **直接 xpath** — 不依赖快照式 ref，每次实时查询 DOM

## 已完成

- 核心库：Browser, PageScanner, ElementOperator, TabManager
- MCP Server：11 个工具（页面扫描、浏览器控制、标签页、状态）
- 所有元素操作通过 run_js 完成，无额外封装
- 测试覆盖（pytest）

## 待做事项（TODO）

1. input_text 问题已解决（用 run_js 替代）
2. click_element 偶发报错排查
3. 测试大页面 get_page_regions 性能
4. MCP init_browser 稳定性增强

## 将来可能的方向

1. **更智能的页面理解** — AI 自动判断页面结构（表单、列表、导航）
2. **多浏览器支持** — Firefox、WebKit
3. **更丰富的 run_js 模板** — 预置常用操作（滚动加载、拖拽）
4. **会话记忆** — 跨对话保持登录状态
5. **截图 + OCR** — 对复杂页面 AI 理解布局
6. **分布式** — 多标签页协同工作

## 技术栈

- Python >= 3.10
- DrissionPage（CDP 底层）
- FastMCP（MCP 框架）
- pytest（测试）