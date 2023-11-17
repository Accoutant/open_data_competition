import scrapy
from jibingPro.items import JibingproItem
class JibingSpider(scrapy.Spider):
    name = "jibing"

    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://jbk.39.net/bw/t1"]
    dic = {}
    def parse(self, response):
        for i in range(1, 101):
            t_url = "https://jbk.39.net/bw/t1_p"+str(i)
            yield scrapy.Request(t_url, callback=self.parse_model)
            i=i+1

    def parse_model(self, response):
        print(response)
        list = response.xpath('//p[@class="result_item_top_l"]')
        name = list.xpath('./a/text()').extract()
        verbe_name = list.xpath('./i/text()').extract()
        item = JibingproItem()
        item["verbe_name"] = verbe_name
        print(name)
        print(verbe_name)
        s_list = response.xpath('//p[@class="result_item_content_label"]')

        j = 0
        for s in s_list:
            symptoms = []
            symptom = s.xpath('./a/text()').extract()
            symptoms.append(symptom)
            self.dic[name[j]] = symptoms
            j = j + 1
        item['dic'] = self.dic
        yield item




