from rootbrowse import Browser

# 创建浏览器实例
browser = Browser(headless=False)
browser.get('https://www.bing.com')

print("=== 页面区域 ===")
regions = browser.view.get_regions()
print(regions)

print("\n=== 搜索区域详情 ===")
if regions:
    # 使用 xpath 获取区域摘要
    summary = browser.view.get_region_summary(regions[0].xpath)
    print(summary)

print("\n=== 内容区域链接 ===")
if len(regions) > 1:
    # 使用 xpath 筛选元素
    links = browser.view.match_element(region_xpath=regions[1].xpath, tag='a', limit=5)
    for link in links:
        print(f"  xpath: {link.xpath[:50]}, text: {link.text[:30]}, attrs: {link.attrs_preview}")

# 直接用 xpath 点击元素
# browser.act.click("/html/body/div[1]/a[1]")

# 使用 run_js 获取长文本（绕过 DOM 限制）
# text = browser.run_js("return document.body.innerText.substring(0, 2000)")

# browser.close()