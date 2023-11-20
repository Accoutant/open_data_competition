import pickle
import pandas as pd
from pandas import DataFrame
from predict import predict
from bert_net import LSTM
from get_vocab import cosine_similarity, Vocab
import torch


def predict_doctor(x: str, net, vocab, max_len):
    output = predict(net, x, vocab, max_len=max_len)
    data = pd.read_excel("./data/merged.xlsx")
    data = data[['患者编码', 'seg', '接诊医生ID', '就诊科室名称_encode']]
    data: DataFrame
    data_fitter = data[data["就诊科室名称_encode"] == output]
    patients = data_fitter['患者编码'].tolist()
    segs = data_fitter['seg'].tolist()
    doctors = data_fitter['接诊医生ID'].tolist()
    # x患者和每个患者都计算一遍余弦相似度
    x = encode_token(x, max_len, vocab)
    cos_dict = {}
    patients_list = []
    segs_list = []
    cos_list = []
    doctors_list = []
    for patient, seg, doctor in zip(patients, segs, doctors):
        segs_list.append(seg.replace(",", ""))
        seg = encode_token(seg, max_len, vocab)
        cos_similarity = cosine_similarity(x, seg)
        patients_list.append(patient)
        cos_list.append(cos_similarity)
        doctors_list.append(doctor)
    cos_dict["病人编号"] = patients_list
    cos_dict['口述'] = segs_list
    cos_dict["余弦相似度"] = cos_list
    cos_dict['医生编号'] = doctors_list
    return cos_dict


def encode_token(x, max_len, vocab):
    x = x.split(",")
    n = len(x)
    if n < max_len:
        x = x + ['[pad]'] * (max_len - n)
    else:
        x = x[:max_len]
    x = torch.tensor([vocab.get_vector(token) for token in x])
    x = torch.mean(x, dim=0)
    return x


if __name__ == '__main__':
    with open('./data/vocab.pkl', "rb") as f:
        vocab = pickle.load(f)

    net = LSTM(128, 128, 3, 0, 70)
    net.load_state_dict(torch.load("./data/param.pkl"))
    net.eval()
    x = "心房颤动,心功能,不全,心房颤动,心功能,不全"
    cos_dict = predict_doctor(x, net, vocab, max_len=5)
    cos_dict = pd.DataFrame(cos_dict)
    cos_dict.dropna(subset=['医生编号'], inplace=True)
    cos_dict.sort_values(by='余弦相似度', ascending=False, inplace=True)
    cos_dict.to_excel("./data/cos.xlsx")



"""
x = "糖尿病,肾病,复查"
"""