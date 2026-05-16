from rootbrowse.browser import Browser

browser = Browser(headless=False)
browser.get('https://www.baidu.com')

print("=== 页面区域 ===")
regions = browser.view.get_regions()
for r in regions:
    print(f"  {r.id}: {r.label} ({r.node_count} 个元素)")

print("\n=== 搜索区域详情 ===")
if regions:
    summary = browser.view.get_region_summary(regions[0].id)
    print(f"  总元素数: {summary.count}")
    print(f"  标签分布: {summary.tag_counts}")

print("\n=== 内容区域链接 ===")
if len(regions) > 1:
    links = browser.view.match_element(region_id=regions[1].id, tag='a', limit=5)
    for link in links:
        print(f"  {link.ref}: {link.text[:30]} - {link.attrs_preview}")

browser.close()