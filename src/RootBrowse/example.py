from rootbrowse.browser import Browser
from DrissionPage.common import Keys

browser = Browser(headless=False)
regions = browser.page.get_regions()


browser.page.get_region_summary("main")

browser.page.match_element(tag="input")
browser.page.get_element()

browser.act.input_by_ref('r78',"python")
browser.act.input_by_ref('r78',text=Keys.ENTER)
browser.page.get_regions()
browser.close()
