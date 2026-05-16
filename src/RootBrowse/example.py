from rootbrowse.browser import Browser
from DrissionPage.common import Keys

browser = Browser(headless=False)
regions = browser.view.get_regions()


browser.view.get_region_summary("main")

print(browser.view.match_element(tag="input"))
browser.view.get_element("r78")

browser.act.input_by_ref('r78',"python")
browser.act.input_by_ref('r78',text=Keys.ENTER)
browser.view.get_regions()
browser.close()
