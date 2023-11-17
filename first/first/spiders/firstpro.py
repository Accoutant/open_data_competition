import scrapy


class FirstproSpider(scrapy.Spider):
    name = "firstpro"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["http://www.baidu.com/"]

    def parse(self, response):
        print(response)
