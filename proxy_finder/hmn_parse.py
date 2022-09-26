from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from loguru import logger


hidemy_base_url = 'https://hidemy.name'
useragent = UserAgent().chrome


def get_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=useragent)
        page = context.new_page()
        page.goto(url)
        html = page.content()
        soup = BeautifulSoup(html, 'html5lib')
        return soup


def hidemy_name_parse(url):
    # Функция извлекает список всех доступных прокси, сохраняет в словарь.
    hmn_list = []
    proxy_dict = {}
    table = get_content(url).findChildren('table')
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
    return proxy_dict


def page_search_hmn(url):
    # Функция извлекает значение максимальной страницы списка прокси.
    table = get_content(url).find_all('div', {'class': 'pagination'})
    link = table[0].find_all('a', href=True)
    return link[-2]['href']


def parse_all():
    final_list = []
    proxy_url = hidemy_base_url + '/ru/proxy-list/'
    logger.info('Search max_page element, wait...')
    max_page_url = page_search_hmn(proxy_url)
    max_item = max_page_url.split('start=')[1].split('#')[0]
    max_page = int(max_item)
    work_page = 0
    while work_page <= int(max_page):
        init_page = hidemy_base_url + f'/ru/proxy-list/?start={work_page}#list'
        parse_dict = hidemy_name_parse(init_page)
        num = work_page / 64
        logger.info(f'Parse hidemy.name proxy-list number {num}')
        final_list.append(parse_dict)
        work_page += 64
    return final_list

