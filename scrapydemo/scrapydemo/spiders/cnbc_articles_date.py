import scrapy

class CnbcArticlesDateSpider(scrapy.Spider):
    name = 'cnbc_articles_date'
    allowed_domains = ['cnbc.com']
    start_urls = ['']

    def __init__(self,
                 year=2021,
                 month='January',
                 day=1):

        self.year  = year
        self.month = month
        self.day   = day

        self.start_urls = ['https://www.cnbc.com/site-map/articles/' \
                          + str(year) + '/' + month + '/' + str(day) + '/']

    def parse(self, response):
        articles = response.xpath('//div[@class="SiteMapArticleList-articleData"]/ul/li/a/@href').getall()
        
        for article in articles[:2]:

            # scrape url, title and store them in item dictionary
            item = {}
            item['url'] = article

            yield scrapy.Request(article,
                                 callback=self.parse_article,
                                 meta={'item':item})

    def parse_article(self, response):

        # item with url and title information is brought over from previous Response
        item = response.meta['item']

        item['section']        = response.xpath('//meta[@property="article:section"]/@content').get()
        item['section_url']    = "" #TODO
        item['title']          = response.xpath('//meta[@property="og:title"]/@content').get()
        item['author']         = response.xpath('//meta[@property="article:author"]/@content').get()
        item['published_time'] = response.xpath('//meta[@property="article:published_time"]/@content').get()
        item['updated_time']   = response.xpath('//meta[@property="article:modified_time"]/@content').get()
        item['image']          = response.xpath('//meta[@itemprop="primaryImageOfPage"]/@content').get()

        item['body'] = response.xpath('//div[@data-module="ArticleBody"]/div/p/text()').getall()

        # pass item to item pipeline
        yield item

