import requests
import re

url = "https://ask.39.net/"
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "cache-control": "max-age=0",
    "Host": "ask.39.net",
    "Referer": "http://www.39.net/",
    "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

content = requests.get(url, headers=headers).content.decode()
boxes = re.findall('(<div class="page-subclassify-title">.*?)<div class="page-subclassify-box">', content, re.S)
print(len(boxes))
item = {}
for box in boxes:
    title_ = re.findall('<div class="page-subclassify-title">(.*?)<div', box, re.S)
    title = re.findall('>(.*?)</a>', title_[0], re.S)
    url__ = re.findall('<div class="page-subclassify-item(.*?)</div>', box, re.S)
    print(title, len(url__))
    url_list = []
    for url_ in url__:
        urls = re.findall('<a href="(.*?)>', url_, re.S)
        sub_titles = re.findall('html">(.*?)</a>', url_, re.S)
        for url, sub_title in zip(urls, sub_titles):
            url_dict = {'url': "https://ask.39.net/" + str(url), 'sub_title': sub_title}
            url_list.append(url_dict)
        print(url_list)
    item['url'] = url_list
    print("-"*50)

