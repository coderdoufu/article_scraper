from scrapydemo.scrapydemo.spiders.reuters import ReutersSpider
from scrapydemo.scrapydemo.spiders.cna import CnaSpider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os, sys
from scrapy import signals
from crochet import setup
setup()

class Scraper:
    def __init__(self):
        settings_file_path = 'scrapydemo.scrapydemo.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerRunner(get_project_settings())
        self.CnaSpider = CnaSpider
        self.ReutersSpider = ReutersSpider

    def run_cna_spiders(self,section,number_articles):
        self.process.crawl(
            self.CnaSpider,                 
            section=section,
            number_articles=number_articles
        )

    def run_reuters_spiders(self,section,section_category_url,number_articles):
        self.process.crawl(
            self.ReutersSpider,                 
            section=section,
            section_category_url=section_category_url,
            number_articles=number_articles
        )

