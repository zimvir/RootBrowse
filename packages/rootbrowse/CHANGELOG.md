# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
  - 删除 `_element_map`、`_ref_counter`、`_scan_elements()`、`_ensure_elements_scanned()`
  - `match_element()` 改为实时查询 DOM
  - `get_element()` 直接接受 xpath，不再有 ref 查表

- **ElementOperator 简化** — 删除 ref 解析逻辑
  - `input_by_ref()` → `input_by_xpath()`
  - 删除 `ref_to_xpath()`、`_is_ref()`、`_resolve_locator()`

- **TabManager 实时同步** — `_tabs` 属性委托 DrissionPage.tab_ids()
  - 不再自维护状态，标签页数、当前索引都实时查询

### Fixed

- **动态页面点击失效** — 根本原因是 ref 快照在 DOM 变化后过期
  - 现改为 xpath 实时查询，每次都从当前 DOM 重新定位

## [0.3.2] - 2026-05-17

### Fixed

- **DrissionPage 4.x 兼容** — `wait.ready()` 被移除
  - 替换为 `wait.doc_loaded()`，等待文档加载完成

## [0.3.1] - 2026-05-17

### Fixed

- **close_browser 无限递归** — MCP server 的 close_browser 函数自调用导致递归溢出
  - 本地函数改名为 `_close_browser()`，避免与 @mcp.tool 装饰的函数同名冲突

- **switch_tab / close_tab API 错误** — DrissionPage 4.x API 变更
  - `switch_to_tab()` → `to_tab()`
  - `close_tab()` → `close()`

- **动态JS页面内容缺失** — 页面未渲染完就扫描
  - `_ensure_elements_scanned()` 前加等待策略，支持 `wait` 参数
  - `"ready"`（默认）等页面完全就绪 / `"doc_loaded"` 等文档加载完 / `"none"` 不等
  - 新增 `timeout` 参数保底超时时间

## [0.3.0] - 2026-05-17

### Added

- **惰性扫描缓存** — 元素扫描结果缓存，避免重复扫描
  - `_ensure_elements_scanned()`: 首次调用时才扫描，后续直接用缓存
  - `clear_cache()`: 换页面时清空缓存
  - `browser.get()` 内部自动清缓存，确保换页后不用旧数据

- **全局 ref 计数器** — 统一元素 ref 生成逻辑
  - `_ref_counter`: 全局计数器，`get_element`/`find_element` 也用同一计数器
  - 所有元素都有 `_element_to_region` 记录，区域归属完整

### Changed

- **`get_regions()` 性能优化** — 不再扫描元素，只检测区域
  - 只调用 `_detect_regions()`，不调 `_scan_elements()`
  - 返回速度大幅提升

- **`_scan_elements()` 优化** — 6 次查询代替 30 次
  - 旧：区域数 × 标签数 = 30 次 `xpath=root_xpath//tag` 查询
  - 新：标签数 = 6 次 `tag:xxx` 全局查询
  - 用 xpath 前缀匹配（`startswith`）判断区域归属

- **`Region` 数据结构调整**
  - `node_count` 字段移除
  - 新增 `root_xpath` 字段，存储区域根元素 xpath

- **`REGION_NOISE_TAGS`** — 噪音标签常量移到 `constants.py`

- **`ele.xpath` 异常处理** — 防止元素已离开 DOM 时报错

## [0.2.1] - 2026-05-16

- 添加依赖说明

## [0.2.0] - 2026-05-16

### Added

- **区域识别** — 实现真正的语义区域检测
  - `browser.page` → `browser.view` 属性重命名
  - `_detect_regions()`: body 直接子元素动态检测，排除噪音标签
  - `_guess_region_label()`: 根据 id/class 关键词猜测区域名称
  - `_element_to_region`: 记录元素与区域的归属关系
  - `_get_refs_in_region()`: 按 region_id 过滤元素
  - `save_state(path)`: cookies 序列化到 JSON 文件
  - `load_state(path)`: 从 JSON 文件恢复 cookies

### Changed

- `Browser.page` 属性重命名为 `Browser.view`
- Region id 格式从 `"main"` 改为 `"region_N"`

## [0.1.0] - 2026-05-10

### Added

- **types.py** — 数据类定义
  - `Region`: 页面语义区块
  - `Element`: 可交互元素
  - `RegionSummary`: 区域摘要
  - `ElementPreview`: 元素摘要
  - `OperationResult`: 操作结果

- **constants.py** — 常量配置
  - `INTERACTIVE_TAGS`: 可交互 HTML 标签列表
  - `INPUT_TAGS`: 可输入标签列表
  - `CLICKABLE_TAGS`: 可点击标签列表
  - `ROLE_TAG_MAP`: ARIA role 映射
  - `DEFAULT_LIMIT`, `DEFAULT_OFFSET`: 分页配置
  - `REF_PREFIX`: ref 前缀 ('r')

- **exceptions.py** — 自定义异常
  - `RootBrowseError` (基异常)
  - `BrowserError`, `ElementNotFoundError`, `RegionNotFoundError`
  - `TabNotFoundError`, `OperationError`, `StateFileError`, `PageLoadError`

- **tab_manager.py** — 标签页管理器
  - `new_tab(url)`: 打开新标签页
  - `close_tab(index)`: 关闭标签页
  - `switch_to_tab(index)`: 切换标签页
  - `tabs_count()`: 获取标签页数量
  - `current_index()`: 获取当前索引

- **element_operator.py** — 元素操作器
  - `click(locator)`: 点击元素
  - `input_by_ref(locator, text, clear)`: 向输入框写入文字
  - `hover(locator)`: 悬停
  - `double_click(locator)`: 双击
  - `right_click(locator)`: 右键
  - `submit(locator)`: 提交表单
  - `clear(locator)`: 清空输入框
  - `send_enter()`: 发送回车键
  - `ref_to_xpath(ref)`: 通过 ref 获取 xpath

- **page_scanner.py** — 页面扫描器
  - `get_regions()`: 获取页面语义区块列表
  - `get_region_summary(region_id)`: 获取区域统计摘要
  - `match_element(**filters)`: 按条件筛选元素摘要列表
  - `get_element(ref)`: 获取完整元素信息
  - `find_element(by, value, filter)`: 多维度精确定位元素

- **browser.py** — 浏览器主入口
  - `get(url, timeout)`: 打开 URL
  - `screenshot(path, annotate)`: 页面截图
  - `save_state(path)`: 保存浏览器状态
  - `load_state(path)`: 恢复浏览器状态
  - `close()`: 关闭浏览器

- **test/** — 完整测试套件
  - 124 tests covering all modules