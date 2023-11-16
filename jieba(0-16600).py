import pandas as pd
import jieba

df = pd.read_excel('data(0-16600).xlsx')
df = df.drop('Unnamed: 0', axis=1)
df = df.dropna()
stopwords = ['，', '。', '！', '？', '：', '、', '‘', '’', '“', '”', '（', '）', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def cutwords(x):
    cutwords = pd.Series(jieba.lcut(x))
    cutwords = list(cutwords[~cutwords.isin(stopwords)])
    cutwords = ",".join(cutwords)
    return cutwords

seg_q = df['question'].apply(cutwords)
df.insert(3, 'seg_q', value=seg_q)

seg_a = df['answer'].apply(cutwords)
df.insert(5, 'seg_a', value=seg_a)

df.to_excel('jieba(0-16600).xlsx')