import scrapy
import os
from scrapydemo.scrapydemo.items import ScrapySectionCategoriesItem


class ReutersSectionsSpider(scrapy.Spider):
    name = 'reuters_sections'
    allowed_domains = ['reuters.com']
    start_urls = ['http://reuters.com/']

    data_dir = 'data'
    base_url = 'https://www.reuters.com/'

    def parse(self, response):
        
        with open(os.path.join(self.data_dir,'reuters_sections.txt'),'r') as f:
            sections = f.readlines()[0].split(',')

        for section in sections:
            item = ScrapySectionCategoriesItem()
            item['section_name'] = section

            section_url = self.base_url + section
            yield scrapy.Request(section_url,
                                 self.parse_section,
                                 meta={'item':item})

    def parse_section(self, response):

        item = response.meta['item']

        item['section_cats'] = response.xpath("//div[@class='SectionPageHeader__selector___3aPGYE']/nav/ul/li/button/div/span/text()").getall()
        item['section_cats_url'] = response.xpath("//div[@class='SectionPageHeader__selector___3aPGYE']/nav/ul/li/button/@data-id").getall()

        yield item
        

    

