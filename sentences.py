import pandas as pd

data = pd.read_excel('cutwords.xlsx', index_col=0)
seg_q = data['seg_q'].tolist()
seg_a = data['seg_a'].tolist()
sentences = seg_a + seg_q
print(len(sentences))
sentences = [token.replace(",", " ")+str('\n') for token in sentences]
with open("sentences.txt", "w", encoding='utf-8') as f:
    f.writelines(sentences)


