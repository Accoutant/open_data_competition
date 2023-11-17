import scrapy


class DoctorSpider(scrapy.Spider):
    name = "doctor"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.120ask.com/zhishi/"]
    model_urls = []
    def parse(self, response):
        li_list = response.xpath('//div[@class="sick_Lihide"]/ul/li')
        for li in li_list:
            keshi = li.xpath("./b/a/text()").extract()
            print(keshi)
            model_url = li.xpath("./b/a/@href").extract()
    # def parse_model(self, response):
    #     for i in range(1, 101):
    #         li_list = response.xpath('/html/body/div[5]/div[2]/div[1]/div[3]/ul/li')
    #         for li in li_list:
    #             title = li.xpath('./div[1]/p/a/text()').extract()
    #             model_url = li.xpath('./div[1]/p/a/@href').extract()
    #             print(title)
    #             print(model_url)
    #             self.model_urls.append(model_url)
    #         for url in self.model_urls: