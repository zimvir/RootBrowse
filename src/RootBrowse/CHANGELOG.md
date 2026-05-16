# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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