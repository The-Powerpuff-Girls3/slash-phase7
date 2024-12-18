"""
Copyright (c) 2021 Rohan Shah
This code is licensed under MIT license (see LICENSE.MD for details)

@author: Slash
"""

import requests
from threading import Thread
from datetime import datetime

from ebaysdk.finding import Connection

from src.formattr import formatTitle


# configs
WALMART = {
    'site': 'walmart',
    'url': 'https://www.walmart.com/search?q=',
    'item_component': 'div',
    'item_indicator': {
        'data-item-id': True
    },
    'title_indicator': 'span.lh-title',
    'price_indicator': {'data-automation-id': 'product-price'},
    'link_indicator': 'a',
    'rating_indicator': 'div.flex.items-center.mt2 span.w_iUH7',
    'img_indicator': 'div.relative.overflow-hidden img'
}

COSTCO = {
    'site': 'costco',
    'url': 'https://www.costco.com/s?dept=All&keyword=',
}

BESTBUY = {
    'site': 'bestbuy',
    'url': 'https://www.bestbuy.com/site/searchpage.jsp?st=',
    'item_component': 'li',
    'item_indicator': {
        'class': 'sku-item'
    },
    'title_indicator': 'h4.sku-title a',
    'price_indicator': 'div.priceView-customer-price span',
    'link_indicator': 'a.image-link',
    'img_indicator': 'div.shop-sku-list-item div div a img'
}

TARGET = {
    'site': 'target',
    'url': 'https://www.target.com/s?searchTerm=',
    'item_component': 'div',
    'item_indicator': {
        'data-item-id': True
    },
    'title_indicator': 'span.lh-title',
    'price_indicator': {'data-automation-id': 'product-price'},
    'link_indicator': 'a',
    'rating_indicator': 'div.flex.items-center.mt2 span.w_iUH7',
    'img_indicator': 'div.relative.overflow-hidden img'
}

TARGET_CONFIG = {
    'url': 'https://www.target.com/s?searchTerm=',
    'site': 'target',
}


# individual scrapers
class scrape_target(Thread):
    def __init__(self, query):
        self.result = {}
        self.query = query
        super(scrape_target, self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """
        params = {
            'api_key': 'xxx',
            'type': 'search',
            'search_term': self.query,
        }
        # make the http GET request to RedCircle API
        api_result = requests.get('https://api.redcircleapi.com/request', params)

        # print the JSON response from RedCircle API
        data = api_result.json()

        itemNum = len(data["search_results"])
        items = []
        for i in range(itemNum):
            item = {'timestamp': data['request_metadata']['processed_at'],
                    'title': data["search_results"][i]['product']["title"],
                    "price": data["search_results"][i]['offers']["primary"]["price"],
                    'link': data["search_results"][i]['product']["link"],
                    }
            items.append(item)

        self.result = items


class scrape_ebay(Thread):
    def __init__(self, query):
        self.result = {}
        self.query = query
        super(scrape_ebay, self).__init__()

    def run(self):
        """Scrape Target's api for data

        Parameters
        ----------
        query: str
            Item to look for in the api

        Returns
        ----------
        items: list
            List of items from the dict
        """

        EBAY_APP = 'BradleyE-slash-PRD-2ddd2999f-2ae39cfa'

        try:
            api = Connection(appid=EBAY_APP, config_file=None, siteid='EBAY-US')
            response = api.execute('findItemsByKeywords', {'keywords': self.query})
        except ConnectionError as e:
            print(e)
            self.result = []

        data = response.dict()

        items = []
        for p in data['searchResult']['item']:
            item = {
                'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'title': formatTitle(p['title']),
                'price': '$' + p['sellingStatus']['currentPrice']['value'],
                'website': 'ebay',
                # 'link': shorten_url(p['viewItemURL'])
                'link': p['viewItemURL'],
                'img_link': p['galleryURL']
            }

            items.append(item)

        self.result = items


CONFIGS = [WALMART, BESTBUY, TARGET]
