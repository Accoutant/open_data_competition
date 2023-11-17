import pandas as pd
import re


def formate_department(x):
    x = x.replace("(", "<")
    x = x.replace(")", ">")
    try:
        y = re.findall("(<.{2}?院区>)", x)[0]
        x = x.replace(y, "")
    except:
        pass
    return x


liushui = pd.read_excel('./data/liushui.xlsx', index_col=0)
liushui.drop(columns=['年龄', '性别', '挂号类型编码', '挂号类型', '挂号时间', '报到时间', '病历书写时间', '就诊时间'], inplace=True)
jiezheng = pd.read_excel('./data/接诊信息.xlsx')
jiezheng.drop(columns=['患者ID', '就诊类型编码', '年龄', '住址', '接诊时间', '诊毕时间'], inplace=True)

data_merged = pd.merge(liushui, jiezheng, how='left', left_on='患者编码', right_on='就诊ID')
data_merged['就诊科室名称'] = data_merged['就诊科室名称'].apply(formate_department)
data_merged['就诊科室名称_encode'] = pd.Categorical(data_merged['就诊科室名称']).codes
data_merged.to_excel('./data/merged.xlsx')