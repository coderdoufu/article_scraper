import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

import sys, os

class CnbcDateSpider(scrapy.Spider):
    name = 'cnbc_date'
    allowed_domains = ['cnbc.com']
    start_urls = ['https://www.cnbc.com/site-map/']

    custom_settings = {
        "ITEM_PIPELINES" : 
        {
            'scrapydemo.pipelines.CnbcPipeline': 100,
        }
    }
    
    def parse(self, response):
        years = response.xpath('//div[@class="SiteMapYear-yearData"]/ul/li/a/text()').getall()
        year_urls = response.xpath('//div[@class="SiteMapYear-yearData"]/ul/li/a/@href').getall()
        for year, year_url in zip(years,year_urls):
            item = {}
            item['year'] = year
            yield scrapy.Request("http:"+year_url,
                                 callback=self.parse_year,
                                 meta={'item':item})
    
    def parse_year(self, response):
        item = response.meta['item']
        item['month_day'] = {}

        months = response.xpath('//div[@class="SiteMapMonth-monthData"]/ul/li/a/text()').getall()
        month_urls = response.xpath('//div[@class="SiteMapMonth-monthData"]/ul/li/a/@href').getall()
        
        for month, month_url in zip(months,month_urls):
            item['month_day'][month] = []
            yield scrapy.Request("http:"+month_url,
                                 callback=self.parse_month,
                                 meta={'item':item,'month':month})

    def parse_month(self, response):
        item = response.meta['item']
        month = response.meta['month']
        item['month_day'][month] = response.xpath('//div[@class="SiteMapDay-fullDate"]/ul/li/a/text()').getall()

        yield item

if __name__ == "__main__":

    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())

    d = runner.crawl(CnbcDateSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    # close reactor after finishing crawling
    os.execl(sys.executable, *sys.argv)

