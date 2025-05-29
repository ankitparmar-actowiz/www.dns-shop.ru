from curl_cffi import requests
# import sys

# sys.path.append(r"E:\API - Scrape.do")

# from key import KEY
key= '2d76727898034978a3091185c24a5df27a030fdc3f8'
response = requests.get(f'https://api.scrape.do/?token={key}&super=true&render=false&url=https://www.dns-shop.ru/product/c20513f468edd21a/678-smartfon-poco-c61-64-gb-belyj/')

print(response.text)
print(response.status_code)