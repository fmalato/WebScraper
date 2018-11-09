from lxml import html
import csv, os, json
import requests
from time import sleep
from pprint import pprint


def AmzonParser(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError('Captcha Required.')
            data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'AVAILABILITY': AVAILABILITY,
                'URL': url,
            }

            return data
        except Exception as e:
            print(e)


def ReadAsin(gpu_model):
    print("{gpu} prices from https://www.amazon.it/".format(gpu=gpu_model))
    sleep(1)
    if gpu_model == "GTX 1070Ti":
        AsinList = ['B076VNJX2G',
                    'B0775GL84Z',
                    'B076VWFDC1',
                    'B076S4RT1J',
                    'B078MVFXFL',
                    'B076VSXDH4',
                    'B076VTXR5S']
    elif gpu_model == "GTX 1080":
        AsinList = ['B01GCAW1IA',
                    'B01GCAVSIO',
                    'B072L3C8SN',
                    'B01GLYD7MG',
                    'B01FTZEBDW',
                    'B072LX16GX',
                    'B01GBX8K60']
    elif gpu_model == "GTX 1080Ti":
        AsinList = ['B06XSB4NW2',
                    'B072WBS76K',
                    'B071Y78QG7',
                    'B06XWXQX6T',
                    'B06XSJJK4M',
                    'B06XWY767M',
                    'B074N9Q5W3',
                    'B07113WJPC',
                    'B06XXC4J6T',
                    'B06XT3TVKP',
                    'B071XP4MBS',
                    'B06XXVVQYH']
    extracted_data = []
    for i in AsinList:
        url = "https://www.amazon.it/dp/" + i
        print("Processing: " + url)
        extracted_data.append(AmzonParser(url))
    f = open('{gpu}.json'.format(gpu=gpu_model), 'w')
    json.dump(extracted_data, f, indent=4)

if __name__ == "__main__":
    gpu_models = ['GTX 1070Ti', 'GTX 1080', 'GTX 1080Ti']
    for model in gpu_models:
        ReadAsin(model)
        with open("{model}.json".format(model=model)) as f:
            data = json.load(f)
            print("Prices list for {model}:".format(model=model))
            for price in data:
                pprint(price["SALE_PRICE"])