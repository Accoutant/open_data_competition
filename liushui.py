import pandas as pd
import jieba

liushui=pd.read_excel('8月无空改.xlsx')
liushui['seg'] = None

for index, value in liushui.iterrows():
    try:
        value[1] = value[1].replace('，', ' ')
        value[1] = value[1].replace('。', ' ')
        value[1] = value[1].replace('‘', ' ')
        value[1] = value[1].replace('’', ' ')
        value[1] = value[1].replace('“', ' ')
        value[1] = value[1].replace('”', ' ')
        value[1] = value[1].replace('？', ' ')
        value[1] = value[1].replace('：', ' ')
        value[1] = value[1].replace('！', ' ')
        value[1] = value[1].replace('、', ' ')
        value[1] = value[1].replace('（', ' ')
        value[1] = value[1].replace('）', ' ')
        seg = jieba.lcut(value[1])
        if " " in seg:
            seg.remove(' ')
        
        #TODO 应该使用正规检索赋值
        liushui.loc[index, "seg"] = ','.join(seg)
    except (AttributeError):
        liushui.loc[index, "seg"] = 'no_str'

liushui = liushui.iloc[:, [0,1,12,2,3,4,5,6,7,8,9,10,11]]
liushui.to_excel('liushui.xlsx')