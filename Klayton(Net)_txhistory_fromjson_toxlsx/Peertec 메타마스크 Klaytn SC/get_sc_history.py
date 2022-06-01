import pandas as pd
import json
from datetime import datetime

# API 키를 받고 해야돼...

file_name = "Peertec 메타마스크 Klaytn Legacy"

with open(f'{file_name}.json', 'r') as file:
   page = json.load(file)

objects_bowl = []
# 반복문 돌아가면서 객체를

num = 0
for each in page:
    num += 1
    # type valuetransfer, typesmartcontract은 제외하고 넣게끔 합시다. 
    # 반복문 돌릴때 하면 됨
    objects = each['result']
    for object in objects:
    # 다 돌릴거면 여기서 전처리해도 되는데
        if object['txType'] == "TxTypeLegacyTransaction":
            continue
        objects_bowl.append(object)
    # 한번 더 어떻게 하나...?

print(num)

dataframe = pd.DataFrame(objects_bowl)


dataframe = dataframe.loc[:,['createdAt','txHash','txType','fromAddress','toAddress','amount','methodName']]
# DECIMAL
DECIMAL = 1000000000000000000
dataframe["amount"] = dataframe["amount"].apply(lambda x: int(x)/DECIMAL)
dataframe.rename(columns = {'amount':'Amount'}, inplace=True)

# KST TIME
def get_local_time(unix_time):
    return datetime.fromtimestamp(unix_time)
dataframe["createdAt"] = dataframe["createdAt"].apply(get_local_time)
dataframe.rename(columns = {'createdAt':'KST Time (GMT+9)'}, inplace=True)

dataframe.to_excel(f'{file_name} transfer.xlsx', index=False)