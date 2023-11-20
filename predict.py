import pickle
import pandas as pd
from pandas import DataFrame
import torch
from bert_net import Bert, LSTM
from get_vocab import Vocab


def predict(net, x, vocab, max_len=10):
    x = x.split(",")
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
    return output


if __name__ == '__main__':
    # net = Bert(128, 200, 16, 0, 4, 188)
    net = LSTM(128, 128, 3, 0, 70)
    net.load_state_dict(torch.load("./data/param.pkl"))
    net.eval()
    with open("./data/vocab.pkl", "rb") as f:
        vocab = pickle.load(f)
    x = "心闷，多梦"
    predict(net, x, vocab)
