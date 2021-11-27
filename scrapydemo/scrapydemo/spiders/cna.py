import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor

import argparse, sys, os
from urllib.parse import quote_plus
import json
from datetime import datetime as dt

def get_request_payload(section='Asia', number_articles=1):

    query = {
                "maxValuesPerFacet": 40,
                "page": 0,
                "hitsPerPage": number_articles,
                "highlightPreTag": quote_plus("__ais-highlight__"),
                "highlightPostTag": quote_plus("__/ais-highlight__"),
                "facetFilters": quote_plus(str([[f"categories:{section}"],["type:article"]])).replace("%27","%22")
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

class CnaSpider(scrapy.Spider):
    name = 'cna'
    allowed_domains = ['channelnewsasia.com']
    start_urls = ['https://www.channelnewsasia.com']

    def __init__(self,
                 section='Business',
                 number_articles=3):

        self.section = section
        self.number_articles = number_articles

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
                             body=get_request_payload(self.section, self.number_articles),
                             headers=headers)

    def parse(self,response):
        pass

    def parse_api(self, response):
        # item = ArticleItem()
        item = {}

        articles = json.loads(response.body.decode('utf-8'))['results'][0]['hits']

        for article in articles:
            item["url"] = article.get('link_absolute','')
            item["section"] = article.get('categories','')
            item["section_url"] = article.get('categories_url','')
            item["title"] = article.get('title','')
            item['image'] = article.get('hero_image_org_url','')
            item["author"] = article.get('author',None)
            item["published_time"] = dt.fromtimestamp(int(article.get('field_release_date'))) if article.get('field_release_date',"") else None
            item["updated_time"]  = dt.fromtimestamp(int(article.get('changed'))) if article.get('changed',"") else None
            item["body"] = article.get('paragraph_text','')
            if not isinstance(item["body"],list):
                item["body"] = [item["body"]]
            yield item

# if __name__ == "__main__":
#     parser=argparse.ArgumentParser()

#     parser.add_argument('--section', type=str, help='section to be crawled')
#     parser.add_argument('--number_articles', type=int, help='number of articles to be crawled')
#     args=parser.parse_args()

#     configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
#     runner = CrawlerRunner(get_project_settings())

#     d = runner.crawl(CnaSpider, 
#                      section=args.section,
#                      number_articles=args.number_articles)
#     d.addBoth(lambda _: reactor.stop())
#     reactor.run()

#     # close reactor after finishing crawling
#     os.execl(sys.executable, *sys.argv)