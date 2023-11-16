import pandas as pd
import jieba

stopwords = ['，', '。', '！', '？', '：', '、', '‘', '’', '“', '”', '（', '）', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def cutwords(x):
    cutwords = pd.Series(jieba.lcut(x))
    cutwords = list(cutwords[~cutwords.isin(stopwords)])
    cutwords = ",".join(cutwords)
    return cutwords
def data(df):
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna()
    return df

df1 = pd.read_excel('data(0-16600).xlsx')
df2 = pd.read_excel('data(16600-28000).xlsx')
df3 = pd.read_excel('data(28000-42000).xlsx')
df4 = pd.read_excel('data(42000-55868).xlsx')

df = pd.concat([df1, df2, df3, df4])

df=data(df)
df.to_excel('data.xlsx')

seg_q = df['question'].apply(cutwords)
df.insert(3, 'seg_q', value=seg_q)
seg_a = df['answer'].apply(cutwords)
df.insert(5, 'seg_a', value=seg_a)

df.to_excel('cutwords.xlsx')