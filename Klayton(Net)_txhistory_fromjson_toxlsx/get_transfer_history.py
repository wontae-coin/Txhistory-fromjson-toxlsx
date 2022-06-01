import pandas as pd
import json
from datetime import datetime


file_name = "Peertec 메타마스크 Klayton FeeDel"
# address

with open(f'{file_name}.json', 'r') as file:
   page_1 = json.load(file)
# with open(f'{file_name} 2.json', 'r') as file:
#    page_2 = json.load(file)
# with open(f'{file_name} 3.json', 'r') as file:
#    page_3 = json.load(file)
# with open(f'{file_name} 4.json', 'r') as file:
#    page_4 = json.load(file)
# with open(f'{file_name} 5.json', 'r') as file:
#    page_5 = json.load(file)
# with open(f'{file_name} 6.json', 'r') as file:
#    page_6 = json.load(file)
# with open(f'{file_name} 7.json', 'r') as file:
#    page_7 = json.load(file)
# with open(f'{file_name} 8.json', 'r') as file:
#    page_8 = json.load(file)

data_1 = page_1['result']
# data_2 = page_2['result']
# data_3 = page_3['result']
# data_4 = page_4['result']
# data_5 = page_5['result']
# data_6 = page_6['result']
# data_7 = page_7['result']
# data_8 = page_8['result']

df_1 = pd.DataFrame(data_1)
# df_2 = pd.DataFrame(data_2)
# df_3 = pd.DataFrame(data_3)
# df_4 = pd.DataFrame(data_4)
# df_5 = pd.DataFrame(data_5)
# df_6 = pd.DataFrame(data_6)
# df_7 = pd.DataFrame(data_7)
# df_8 = pd.DataFrame(data_8)
dataframe = df_1
# dataframe = pd.concat([df_1, df_2])
# dataframe = pd.concat([df_1, df_2, df_3,df_4, df_5, df_6, df_7, df_8])

dataframe = dataframe.loc[:,['createdAt','txHash','txType','methodName','fromAddress','toAddress','amount']]


# DECIMAL
DECIMAL = 1000000000000000000
dataframe["amount"] = dataframe["amount"].apply(lambda x: int(x)/DECIMAL)
dataframe.rename(columns = {'amount':'Amount'}, inplace=True)

# KST TIME
def get_local_time(unix_time):
    return datetime.fromtimestamp(unix_time)
dataframe["createdAt"] = dataframe["createdAt"].apply(get_local_time)
dataframe.rename(columns = {'createdAt':'KST Time (GMT+9)'}, inplace=True)

dataframe.to_excel(f'{file_name}.xlsx', index=False)