import pandas as pd
import json
from datetime import datetime

# API 키를 받고 해야돼...

file_name = "Peertec 메타마스크 Klaytn 인터널"

with open(f'{file_name}.json', 'r') as file:
   page = json.load(file)

objects_bowl = []
# 반복문 돌아가면서 객체를

# # KST TIME
def get_local_time(unix_time):
    return datetime.fromtimestamp(unix_time)
# dataframe["createdAt"] = dataframe["createdAt"].apply(get_local_time)


num = 0
for each in page:
    num += 1
    # type valuetransfer, typesmartcontract은 제외하고 넣게끔 합시다. 
    # 반복문 돌릴때 하면 됨
    objects = each['result']
    # objects_bowl.extend(objects)

    for object in objects:
        object['Amount'] = int(object['amount']) / 1000000000000000000
        object["KST Time (GMT+9)"] = get_local_time(object["createdAt"])
    # # 다 돌릴거면 여기서 전처리해도 되는데
    #     if object['txType'] == "TxTypeLegacyTransaction":
    #         continue
        objects_bowl.append(object)
    # 한번 더 어떻게 하나...?

print(num)

dataframe = pd.DataFrame(objects_bowl)

# token Address의 token Info를 어떻게 가져올 것이냐.. 
#

# createdAt	parentHash	blockNumber	fromAddress	toAddress	toAddressName	tokenAddress	amount	decimals	ticker	fromAddressName



# dataframe = dataframe.loc[:,['createdAt','txHash','txType','fromAddress','toAddress','amount','methodName']]

dataframe = dataframe.loc[:,['KST Time (GMT+9)','parentHash','fromAddress','toAddress', 'Amount', 'fromAddressName', 'toAddressName', 'methodName']]
# # DECIMAL
# dataframe.rename(columns = {'amount':'Amount'}, inplace=True)


dataframe.rename(columns = {'parentHash':'txHash'}, inplace=True)

dataframe.to_excel(f'{file_name} transfer.xlsx', index=False)