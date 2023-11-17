import json
import pandas as pd

with open('yiyuanPro/data1.json', encoding='utf-8') as f:
    dicts = json.load(f)

new_urls = []
for dict in dicts:
    for url in dict['urls']:
        new_dict = {'title': dict['title'], 'url': url}
        new_urls.append(new_dict)

data = pd.DataFrame(new_urls)
data.drop_duplicates(subset=['title', 'url'], inplace=True)
data.reset_index(drop=True, inplace=True)
# data.to_excel('urls.xlsx')


