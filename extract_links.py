# from selenium.webdriver import Chrome
from undetected_chromedriver import Chrome, ChromeOptions
import requests, math, time
from lxml import etree

options = ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--profile-directory=Default")
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = Chrome(options=options)
time.sleep(2)

driver.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p=1')
driver.maximize_window()
time.sleep(2)

tempCookies = driver.get_cookies()

cookies = {cookie['name']: cookie['value'] for cookie in tempCookies}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

response = requests.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p=1', 
                        cookies=cookies,
                        headers=headers)

def getLinks(tree):
    links = tree.xpath('//a[@class="catalog-product__name ui-link ui-link_black"]/@href')
    for link in links:
        Urls.append('https://www.dns-shop.ru' + link)

# file = open('content.html', 'w')
# file.write(response.text)
# file.close()

Urls = []
mainTree = etree.HTML(response.text)
totalRecords = int(mainTree.xpath('//span[@data-role="items-count"]')[0].text.split(' ')[0].strip())
totalPages = math.ceil(totalRecords / 18)

for page in range(1, totalPages + 1):
    if page == 1:
        getLinks(mainTree)
    else:
        response = requests.get(f'https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p={page}', 
                        cookies=cookies,
                        headers=headers)
        tree = etree.HTML(response.text)
        getLinks(tree)
    print(page)
# print(Urls)

file = open('links.txt', 'w')
file.write('\n'.join(Urls))
file.close()