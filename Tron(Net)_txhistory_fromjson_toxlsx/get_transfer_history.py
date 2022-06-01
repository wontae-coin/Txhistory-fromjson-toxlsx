import requests
import pandas as pd
from datetime import datetime

target_account = "TKqUVHFV4ayYZR138m2BiVPktn9XZXLZ7W"

df = pd.DataFrame(columns=['time','tx_hash','tx_type',
'coin','token_type','amount','from_address','to_address'])

def get_json_data(target_account, start = 0):
    url = f"https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=20&start={start}&address={target_account}"
    res = requests.get(url)
    json_data = res.json()
    return json_data

json_data = get_json_data(target_account)
total_num = json_data['total']
number_of_iter = ( total_num // 20 ) + 1
txs = json_data['data']

def add_row_of_(txs):
    global df
    for tx in txs:
        tx_time_stamp = datetime.fromtimestamp(tx['timestamp']/1000)
        tx_hash = tx['hash']
        tx_result = tx['result']
        if tx_result != 'SUCCESS':
            continue
        tx_coin = tx['tokenInfo']['tokenName']
        tx_token_decimal = tx['tokenInfo']['tokenDecimal'] 
        # TRX이 아닌 TRC10은 decimal 값이 0으로 들어온다
        tx_amount = int(tx['amount']) if tx_token_decimal == 0 else int(tx['amount']) / (10 ** tx_token_decimal)
        tx_from_address = tx['ownerAddress']
        tx_to_address = tx['toAddress']
        tx_token_type = tx['tokenType']
        try:
            tx_type = tx['trigger_info']['methodName']
        except:
            tx_type = "Transfer TRX"
        df = pd.concat([df, pd.DataFrame([[tx_time_stamp, tx_hash,tx_type, 
        tx_coin, tx_token_type,tx_amount,tx_from_address,
        tx_to_address]], 
        columns=['time','tx_hash','tx_type',
        'coin','token_type','amount','from_address','to_address'])])

add_row_of_(txs)

for i in range(1, number_of_iter):
    start = 20 * i
    json_data = get_json_data(target_account, start)
    txs = json_data['data']
    add_row_of_(txs)

file_name =  F'트론 입출금 {target_account}.xlsx'
df.to_excel(file_name, index=False)

    




