import pandas as pd
import json
from datetime import datetime


with open('binance_10028(1_sub)_deposit_history.json', 'r') as file:
   result = json.load(file)

data = result['data'][0]['res'] # 리스트여야 함
df = pd.DataFrame(data)

# DATETIME
def get_local_time(unix_time):
    return datetime.fromtimestamp(unix_time/1000)
df["insertTime"] = df["insertTime"].apply(get_local_time)
df.rename(columns = {'insertTime':'KST Time'}, inplace=True)

# TRANSFER TYPE
def get_transfer(number):
   return "internal (binance ↔ binance)" if number == 0 else "external (binance ↔ external)"
df["transferType"] = df["transferType"].apply(get_transfer) # axis=1

# STATUS
status_enum = {
   0: "Cancelled",
   1: "Success"
}
def get_status(number):
   return status_enum[number]
df["status"] = df["status"].apply(get_status) # axis=1

# WALLET TYPE
df["walletType"] = df["walletType"].apply(lambda x: "spot" if x == 0 else "fund") # axis=1

df.to_excel('binance_10028(1_sub)_deposit_history.xlsx', index=False)