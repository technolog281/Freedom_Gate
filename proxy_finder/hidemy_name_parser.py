from bs4 import BeautifulSoup
from loguru import logger


hidemy_base_url = 'https://hidemy.name'


# def hidemy_name_parse(url):
#     proxy_dict = {}
#     # Функция извлекает список всех доступных прокси, сохраняет в словарь.
#     hmn_list = []
#     soup = BeautifulSoup(requiredHtml, 'html5lib')
#     table = soup.findChildren('table')
#     rows = table[0].findChildren(['thead', 'tr'])
#     for row in rows:
#         cells = row.findChildren('td')
#         for cell in cells:
#             hmn_list.append(cell.text)
#     del hmn_list[0:14]
#     while len(hmn_list) >= 1:
#         ip_key = hmn_list[0]
#         attr_value = []
#         for i in range(1, 7):
#             attr_value.append(hmn_list[i])
#         proxy_dict[ip_key] = attr_value
#         del hmn_list[0:7]
#     return proxy_dict


def page_search_hmn(url):
    # Функция извлекает значение максимальной страницы списка прокси.
    driver.get(url)
    requiredHtml = driver.page_source
    soup = BeautifulSoup(requiredHtml, 'html5lib')
    table = soup.find_all('div', {'class': 'pagination'})
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
    driver.close()
    return final_list


if __name__ == '__main__':
    print(page_search_hmn(hidemy_base_url))
