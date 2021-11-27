# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter

class ReutersPipeline(object):

    def open_spider(self, spider):

        if spider.name != 'default':
            if spider.name == 'reuters_sections':
                self.f = open('scrapydemo/scrapydemo/data/reuters_categories.json', 'wb')
            elif spider.name == 'reuters':
                self.f = open('scrapydemo/scrapydemo/data/reuters.json', 'wb')
            elif spider.name == 'cna':
                self.f = open('scrapydemo/scrapydemo/data/cna.json', 'wb')
            elif spider.name == 'cnbc_articles_date':
                self.f = open('scrapydemo/scrapydemo/data/cnbc_articles_date.json', 'wb')
            self.exporter = JsonItemExporter(self.f)
            self.exporter.start_exporting()

    def close_spider(self, spider):
        if spider.name != 'default':
            self.exporter.finish_exporting()
            self.f.close()

    def process_item(self, item, spider):
        if spider.name != 'default':
            if spider.name in ['reuters','cna','cnbc_articles_date']:
                # post-processing body from list to string format
                item["body"] = '\n\n'.join(item["body"])

            self.exporter.export_item(item)
        return item

class CnbcPipeline(object):

    def open_spider(self, spider):
        self.f = open('scrapydemo/scrapydemo/data/cnbc_date.json', 'wb')
        self.exporter = JsonItemExporter(self.f)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.f.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item