import scrapy


class LinkedinSpiderSpider(scrapy.Spider):
    name = "linkedin_spider"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://linkedin.com"]

    def parse(self, response):
        pass
