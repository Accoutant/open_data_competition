import pandas as pd
from torch.utils.data import DataLoader, Dataset
import numpy as np
import pickle
from pandas import DataFrame


def split_train_test(x_data, t_data, z_data, seed, rate):
    """
    按照seed和rate来区分训练集和测试集
    :param x_data: 未打乱的特征数据，np.array数组
    :param t_data: 未打乱的标签数据, np.array数组
    :param seed: 种子
    :param rate: 划分比例，eg:0.9代表训练集占0.9
    :return: 返回打乱后的(x_train, t_train), (x_test, t_test)， 均为np.array数组
    """
    shuffled_indices = np.arange(x_data.shape[0])
    np.random.seed(seed)
    np.random.shuffle(shuffled_indices)
    x_data, t_data, z_data = x_data[shuffled_indices], t_data[shuffled_indices], z_data[shuffled_indices]
    idx = int(rate*x_data.shape[0])
    x_train = x_data[:idx]
    x_test = x_data[idx:]
    t_train = t_data[:idx]
    t_test = t_data[idx:]
    z_train = z_data[:idx]
    z_test = z_data[idx:]
    return (x_train, t_train, z_train), (x_test, t_test, z_test)


class Patient(Dataset):
    def __init__(self, patient_ids, complaints, departments):
        super().__init__()
        self.patient_ids = patient_ids.tolist()
        self.complaints = complaints.tolist()
        self.departments = departments

    def __getitem__(self, idx):
        return (self.patient_ids[idx], self.complaints[idx], self.departments[idx])

    def __len__(self):
        return len(self.patient_ids)


if __name__ == '__main__':
    data = pd.read_excel("./data/merged.xlsx")
    # data['就诊科室名称_encode'] = pd.Categorical(data['就诊科室名称']).codes
    # data.to_excel("./data/merged.xlsx")
    print(len(data['就诊科室名称'].unique()))
    patient_IDs = np.array(data['患者编码'])
    complaint = np.array(data['seg'])
    department = np.array(data['就诊科室名称_encode'])

    # 获取unique科室字典
    data = data[['就诊科室名称', '就诊科室名称_encode']]
    data.drop_duplicates(subset=['就诊科室名称', '就诊科室名称_encode'], inplace=True)
    data: DataFrame
    department_dict = {}
    for index, item in data.iterrows():
        department_name = item[0]
        encode = item[1]
        department_dict[encode] = department_name
    print(department_dict)
    with open("data/department_dict.pkl", "wb") as f:
        pickle.dump(department_dict, f)

    # 划分测试集和训练集
    (patient_IDs_train, complaint_train, department_train), (patient_IDs_test, complaint_test, department_test) = split_train_test(patient_IDs, complaint, department, seed=2023, rate=0.8)

    patient_train = Patient(patient_IDs_train, complaint_train, department_train)
    patient_test = Patient(patient_IDs_test, complaint_test, department_test)

    train_iter = DataLoader(patient_train, batch_size=64)
    test_iter = DataLoader(patient_test, batch_size=64)

    x = next(iter(train_iter))
    print(x)
    with open("./data/train_iter.pkl", "wb") as f:
        pickle.dump(train_iter, f)
    with open("./data/test_iter.pkl", "wb") as f:
        pickle.dump(test_iter, f)

