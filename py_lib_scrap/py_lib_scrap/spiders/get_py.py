import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class GetPySpider(CrawlSpider):
    name = "get_py"
    allowed_domains = ["github.com"]
    start_urls = ["http://github.com/"]


    # rules : find links with termination ".py" from start_urls
    

    def parse(self, response):
        pass
