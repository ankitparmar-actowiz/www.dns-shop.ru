from undetected_chromedriver import Chrome, ChromeOptions
import requests, math, time
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed

# -------------------- Setup Chrome Driver --------------------
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
time.sleep(2)

# -------------------- Get Session Cookies --------------------
tempCookies = driver.get_cookies()
cookies = {cookie['name']: cookie['value'] for cookie in tempCookies}
driver.quit()

# -------------------- Define Headers --------------------
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

# -------------------- Define Functions --------------------
Urls = []

def getLinks(tree):
    links = tree.xpath('//a[@class="catalog-product__name ui-link ui-link_black"]/@href')
    return ['https://www.dns-shop.ru' + link for link in links]

# Fetch first page to determine total pages
response = requests.get('https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p=1', cookies=cookies, headers=headers)
mainTree = etree.HTML(response.text)
totalRecords = int(mainTree.xpath('//span[@data-role="items-count"]')[0].text.split(' ')[0].strip())
totalPages = math.ceil(totalRecords / 18)

# Save links from page 1
Urls.extend(getLinks(mainTree))

# -------------------- Parallel Fetch for Remaining Pages --------------------
def fetch_and_parse(page):
    url = f'https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/?p={page}'
    resp = requests.get(url, cookies=cookies, headers=headers)
    tree = etree.HTML(resp.text)
    return getLinks(tree)

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_and_parse, page) for page in range(2, totalPages + 1)]
    for future in as_completed(futures):
        try:
            Urls.extend(future.result())
        except Exception as e:
            print("Error on thread:", e)

# -------------------- Save to File --------------------
with open('links.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(Urls))

print(f"✅ Scraped {len(Urls)} product links across {totalPages} pages.")
