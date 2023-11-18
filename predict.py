import pickle
import pandas as pd
from pandas import DataFrame
import torch

from bert_net import Bert
from get_vocab import Vocab


def predict(net, x, vocab, max_len=10):
    x = ['[cls]'] + x.split(",")
    n = len(x)
    if n < max_len:
        x = x + ['[pad]'] * (max_len - n)
    else:
        x = x[:max_len]
    x = torch.tensor([vocab.get_vector(token) for token in x]).unsqueeze(0)
    vec, output = net(x)
    output = torch.argmax(output.squeeze(0), dim=0).item()
    print(output)
    with open("./data/department_dict.pkl", "rb") as f:
        department_dict = pickle.load(f)
    print("department: ", department_dict[output])


if __name__ == '__main__':
    net = Bert(128, 16, 0, 3, 188)
    with open("./data/vocab.pkl", "rb") as f:
        vocab = pickle.load(f)
    x = "甲亢,停药,复查"
    predict(net, x, vocab)