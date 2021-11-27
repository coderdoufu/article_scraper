import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

class ReutersSpider(scrapy.Spider):
    name = 'reuters'

    allowed_domains = ['reuters.com']
    
    def __init__(self,
                 section='world',
                 section_category_url='/world/africa/',
                 number_articles=2):

        self.section = section.lower()
        self.section_category_url = section_category_url
        self.number_articles = number_articles

        # initial Request
        self.start_urls = [f'https://www.reuters.com{self.section_category_url}']

    def parse(self, response):

        # get all the story cards
        articles = response.xpath(f'//a[contains(@href, "{self.section_category_url}")]')

        for article in articles[:self.number_articles]:
            
            # scrape url, title and store them in item dictionary
            # item = ArticleItem()
            item = {}
            item['url']   = 'https://www.reuters.com' + article.xpath('./@href').get()
            item['section'] = self.section
            item['section_url'] = self.section_category_url

            # send the next Request to crawl more information at article level
            # for example: author, published time, updated time, body
            yield scrapy.Request(item['url'],
                                 callback=self.parse_article,
                                 meta={'item':item})

    def parse_article(self, response):

        # item with url and title information is brought over from previous Response
        item = response.meta['item']

        # scrape author, published time and updated time using the header meta field
        item['title']          = response.xpath('//meta[@property="og:title"]/@content').get()
        item['author']         = response.xpath('//meta[@name="article:author"]/@content').get()
        item['published_time'] = response.xpath('//meta[@name="article:published_time"]/@content').get()
        item['updated_time']   = response.xpath('//meta[@name="article:modified_time"]/@content').get()
        item['image']          = response.xpath('//meta[@property="og:image"]/@content').get()

        # scrape body
        item['body'] = response.xpath('//p[contains(@data-testid,"paragraph")]/text()').getall()

        # pass item to item pipeline
        yield item
