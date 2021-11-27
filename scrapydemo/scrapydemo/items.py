# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    section = scrapy.Field()
    section_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    published_time = scrapy.Field()
    updated_time = scrapy.Field()
    body = scrapy.Field()


class ScrapySectionCategoriesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    section_name = scrapy.Field()
    section_cats = scrapy.Field()
    section_cats_url = scrapy.Field()
