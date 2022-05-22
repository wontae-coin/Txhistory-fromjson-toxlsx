import pandas as pd
import json
from datetime import datetime

address = "0x8f27fa136ff4da1796368380019029d81d12d06d"

with open(f'{address}_page_1.json', 'r') as file:
   page_1 = json.load(file)

with open(f'{address}_page_2.json', 'r') as file:
   page_2 = json.load(file)

data_1 = page_1['result']
data_2 = page_2['result']

df_1 = pd.DataFrame(data_1)
df_2 = pd.DataFrame(data_2)

dataframe = pd.concat([df_1, df_2])

# DECIMAL
DECIMAL = 1000000000000000000
dataframe["amount"] = dataframe["amount"].apply(lambda x: int(x)/DECIMAL)
dataframe.rename(columns = {'amount':'Amount'}, inplace=True)

# KST TIME
def get_local_time(unix_time):
    return datetime.fromtimestamp(unix_time)
dataframe["createdAt"] = dataframe["createdAt"].apply(get_local_time)
dataframe.rename(columns = {'createdAt':'KST Time'}, inplace=True)

dataframe.to_excel(f'KLAY_{address}_transfer_history.xlsx', index=False)