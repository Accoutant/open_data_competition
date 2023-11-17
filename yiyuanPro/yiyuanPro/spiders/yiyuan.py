import scrapy
import time
from yiyuanPro.items import YiyuanproItem
class YiyuanSpider(scrapy.Spider):
    name = "yiyuan"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://ask.39.net/"]
    model_urls = []
    model_urls_1 = []
    keshi_models=[]
    def parse(self, response):
        div_list = response.xpath('/html/body/div[3]/div[2]/div[2]/div')
        alist = [0, 1, 2, 3, 4]
        keshis = []
        for index in alist:
            time.sleep(2)
            model_url_List = div_list[index].xpath('./div')
            i = 0
            for index1 in model_url_List:
                time.sleep(2)
                model_url = model_url_List[i].xpath('./div[1]/a/@href').extract_first()
                keshi = model_url_List[i].xpath('./div[1]/a/text()').extract_first()
                keshis.append(keshi)
                i=i+1
                self.model_urls.append(model_url)
                self.keshi_models.append(keshi)
                j=0
        for url in self.model_urls:
            time.sleep(2)
            item = YiyuanproItem()
            item['title'] = keshis[j]
            j=j+1
            for i in range(1,101):
                t_url = "https://ask.39.net/news"+url[7:-9]+"-"+str(i)+".html"
                yield scrapy.Request(t_url, callback=self.parse_model, meta={'item':item} )
                # item = YiyuanproItem()
                # item
    def parse_model(self, response):
        time.sleep(2)
        t_urls = []
        q_urls = []
        li_list = response.xpath('//*[@id="list_tag"]/ul/li')
        for li in li_list:
            title = li.xpath('./span/p/a/text()').extract_first()
            q_url = li.xpath('./span/p/a/@href').extract_first()
            q_urls.append(q_url)
        for url in q_urls:
            t_url = "https://ask.39.net"+url
            t_urls.append(t_url)
        item = response.meta['item']
        item['urls'] = t_urls
        yield item
    # yield scrapy.Request(t_url, callback=self.parse1_model)
    # def parse1_model(self, response):
    #     time.sleep(2)
    #     question = response.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/p[1]/text()').extract_first()
    #     print("问题为：{}".format(question))
