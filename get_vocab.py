import torch
import pandas as pd
import pickle


class Vocab:
    def __init__(self, token_dict: dict, vectors_dict: dict):
        self.vocab = token_dict
        self.vectors_dict = vectors_dict

    def __getitem__(self, token):
        if token in self.vocab.keys():
            output = self.vocab[token]
        else:
            output = self.vocab['unk']
        return output

    def __len__(self):
        return len(self.vocab)

    def get_vector(self, token):
        if token in self.vectors_dict.keys():
            output = self.vectors_dict[token]
        else:
            output = self.vectors_dict['unk']
        return output


def cosine_similarity(x, y):
    """计算相似度"""
    return (torch.dot(x, y) / (torch.norm(x) * torch.norm(y))).item()


if __name__ == "__main__":
    with open('./data/vocab.txt', 'r', encoding='utf-8') as f:
        vocabs = f.readlines()

    tokens_dict = {}
    for token in vocabs:
        word, idx = token.split(" ")
        tokens_dict[word] = idx.replace('\n', '')

    with open('./data/vectors.txt', 'r', encoding='utf-8') as f:
        vectors = f.readlines()

    vectors_dict = {}
    for item in vectors:
        temp = item.replace("\n", "").split(" ")
        word, vector = temp[0], temp[1:]
        vector = [float(num) for num in vector]
        vectors_dict[word] = vector
    vectors_dict['[pad]'] = [0] * 128

    # 保持vocab
    vocab = Vocab(tokens_dict, vectors_dict)
    with open('./data/vocab.pkl', "wb") as f:
        pickle.dump(vocab, f)



    print(vocab['[cls]'])
    # data = pd.read_excel('./data/cutwords.xlsx')
    a = "[cls],肾病,综合征,发现,右,颈部,肿物,数月"
    print(a)
    a = a.split(",")
    a = torch.tensor([vocab.get_vector(token) for token in a])
    a = torch.mean(a, dim=0)

    b = "[cls],肾病,综合征,13,年"
    print(b)
    b = b.split(",")
    b = torch.tensor([vocab.get_vector(token) for token in b])
    b = torch.mean(b, dim=0)
    print(cosine_similarity(a, b))
