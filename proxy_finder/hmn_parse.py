from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


hmn_url = 'https://hidemy.name/ru/proxy-list/?start=0#list'
useragent = UserAgent().chrome


class html_exec:
    def __init__(self, browser_type, url):
        self.browser_type = browser_type
        self.url = url


with sync_playwright() as p:
    proxy_dict = {}
    hmn_list = []
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=useragent)
    page = context.new_page()
    page.goto(hmn_url)
    html = page.content()
    soup = BeautifulSoup(html, 'html5lib')
    table = soup.findChildren('table')
    rows = table[0].findChildren(['thead', 'tr'])
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            hmn_list.append(cell.text)
    del hmn_list[0:14]
    while len(hmn_list) >= 1:
        ip_key = hmn_list[0]
        attr_value = []
        for i in range(1, 7):
            attr_value.append(hmn_list[i])
        proxy_dict[ip_key] = attr_value
        del hmn_list[0:7]
    print(proxy_dict)

