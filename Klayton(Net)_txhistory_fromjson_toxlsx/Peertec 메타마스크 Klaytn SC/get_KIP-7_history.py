import pandas as pd
import json
from datetime import datetime

# API 키를 받고 해야돼...

file_name = "Peertec 메타마스크 Klaytn KIP-7"

with open(f'{file_name}.json', 'r') as file:
   page = json.load(file)

objects_bowl = []
# 반복문 돌아가면서 객체를

TICKERS = {
    "0x74ba03198fed2b15a51af242b9c63faf3c8f4d34" : "AKLAY",
    "0x5fff3a6c16c2208103f318f4713d4d90601a7313" : "KLEVA",
    "0xf6f6b8bd0ac500639148f8ca5a590341a97de0de" : "WKLAY",
    "0xa691c5891d8a98109663d07bcf3ed8d3edef820a" : "IBKLAY",
    "0xb15183d0d4d5e86ba702ce9bb7b633376e7db29f" : "KOKOA",
    "0x666e58391280a06a7cb380c1741376e0b3dd7531" : "sKOKOA",
    "0x4fa62f1f404188ce860c8f0041d6ac3765a72e67" : "KSD",
    "0x5e6215dfb33b1fb71e48000a47ed2ebb86d5bf3d" : "dKSD"
}

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
        object['Amount'] = int(object['amount'], 16) / (10 ** object['decimals'])
        object['Ticker'] = TICKERS[object['tokenAddress']]
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

dataframe = dataframe.loc[:,['KST Time (GMT+9)','parentHash','fromAddress','toAddress', 'Amount','Ticker', 'fromAddressName', 'toAddressName']]
# # DECIMAL
# dataframe.rename(columns = {'amount':'Amount'}, inplace=True)


dataframe.rename(columns = {'parentHash':'txHash'}, inplace=True)

dataframe.to_excel(f'{file_name} transfer.xlsx', index=False)