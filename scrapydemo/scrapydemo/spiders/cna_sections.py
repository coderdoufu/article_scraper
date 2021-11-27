import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapydemo.scrapydemo.items import ArticleItem
from twisted.internet import reactor

import sys, os
from urllib.parse import quote_plus
import json
from datetime import datetime as dt

def get_request_payload():

    query = {
                "maxValuesPerFacet": 40,
                "page": 0,
                "hitsPerPage": 1,
                "highlightPreTag": quote_plus("__ais-highlight__"),
                "highlightPostTag": quote_plus("__/ais-highlight__"),
                "attributesToRetrieve": [],
                "attributesToHighlight": [],
                "attributesToSnippet": [],
                "facets": "categories",
                "facetFilters": quote_plus(str([[f"type:article"]])).replace("%27","%22")
            }

    query_url = "query=&"+ "&".join("%s=%s" % (k,v) for k,v in query.items())

    query_string = {
                    "requests":
                        [{
                            "indexName":"cnarevamp-ezrqv5hx",
                            "params":query_url
                        }]
                    }

    query_string_url = json.dumps(query_string)

    return query_string_url

class CnaSectionsSpider(scrapy.Spider):
    name = 'cna_sections'
    allowed_domains = ['channelnewsasia.com']
    start_urls = ['https://www.channelnewsasia.com']

    custom_settings = {
        "ITEM_PIPELINES" : {}
    }

    def start_requests(self):

        url = 'https://kkwfbq38xf-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.0.0)%3B%20JS%20Helper%20(0.0.0-5a0352a)&x-algolia-application-id=KKWFBQ38XF&x-algolia-api-key=e5eb600a29d13097eef3f8da05bf93c1'
        headers = {
                    "accept": 'application/json',
                    "Accept-Encoding": 'gzip, deflate, br',
                    "Accept-Language": 'en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                    "Connection": 'keep-alive',
                    "content-type": 'application/x-www-form-urlencoded',
                    "Host": 'kkwfbq38xf-dsn.algolia.net',
                    "Origin": 'https://www.channelnewsasia.com',
                    "Referer": 'https://www.channelnewsasia.com/',
                    "Sec-Fetch-Mode": 'cors',
				    "Sec-Fetch-Site": 'cross-site',
                  }

        yield scrapy.Request(url,
                             callback=self.parse_api,
                             method="POST",
                             body=get_request_payload(),
                             headers=headers)

    def parse(self,response):
        pass

    def parse_api(self, response):
        categories = json.loads(response.body.decode('utf-8'))['results'][0]['facets']['categories']
        with open('scrapydemo/data/cna_sections.txt', 'wb') as f:
            f.write(','.join(list(categories.keys())))

if __name__ == "__main__":

    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())

    d = runner.crawl(CnaSectionsSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    # close reactor after finishing crawling
    os.execl(sys.executable, *sys.argv)