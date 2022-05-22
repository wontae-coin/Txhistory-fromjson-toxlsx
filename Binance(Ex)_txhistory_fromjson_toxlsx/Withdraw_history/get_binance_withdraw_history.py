import pandas as pd
import json
from datetime import datetime, timedelta

with open('binance_10012(1_main)_withdraw_history.json', 'r') as file:
   result = json.load(file)

data = result['data'][0]['res'] # 리스트여야 함

df = pd.DataFrame(data)

# DATETIME
# "2022-05-11 09:11:52"(str type)을 datetime 객체로!
def get_date_time_from_str(date_time_str):
   return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S') + timedelta(hours=9)
df["applyTime"] = df["applyTime"].apply(get_date_time_from_str)
df.rename(columns = {'applyTime':'KST Time'}, inplace=True)

# TRANSFER TYPE
def get_transfer(number):
   return "internal (binance ↔ binance)" if number == 0 else "external (binance ↔ external)"
df["transferType"] = df["transferType"].apply(get_transfer) # axis=1

# STATUS
status_enum = {
   0: "Email Sent",
   1: "Cancelled",
   2: "Awaiting Approval",
   3: "Rejected",
   4: "Processing",
   5: "Failure",
   6: "Completed"
}
def get_status(number):
   return status_enum[number]
df["status"] = df["status"].apply(get_status) # axis=1

# WALLET TYPE
df["walletType"] = df["walletType"].apply(lambda x: "spot" if x == 0 else "fund") # axis=1
df.to_excel('binance_10012(1_main)_withdraw_history.xlsx', index=False)