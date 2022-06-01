import requests
import pandas as pd
from datetime import datetime, timedelta
# 이전것: terra174evzq0tnd0uvzkkrvg08n9geqpcsvdrychcm8
# terra1s7gxam60m650w29s64ckqrw902c9nshgeu3zm8
target_account = "terra1s7gxam60m650w29s64ckqrw902c9nshgeu3zm8"
# offset 돌아가면서 할 수 있게...?
url = f"https://fcd.terra.dev/v1/txs?offset=0&limit=100&account={target_account}"
res = requests.get(url)
json_data = res.json()
# 188254623

# next_offset = json_data["next"] # 188254623, 240362378
# limit = json_data["limit"]
txs = json_data['txs'] # 전체 TRANSACTION 데이터

df = pd.DataFrame(columns=['type','time','tx_hash','memo','coin','tx_amount_in','tx_amount_out','from_address','to_address','terra_finder'])

num = 0
for tx in txs:
    tx_data = tx['tx']
    tx_timestamp = tx['timestamp']
    tx_hash = tx['txhash']
    tx_memo = tx_data['value']['memo']

    tx_msgs = tx_data['value']['msg']
    for tx_msg in tx_msgs:
        # 하나의 tx_hash에 tx가 여러개 있는 경우
        tx_type = tx_msg['type']
        if tx_type == "bank/MsgSend":
            num += 1
            # TYPE
            tx_type = "msgsend"

            # COIN (TICKER)
            tx_coin = tx_msg['value']['amount'][0]['denom']
            tx_coin = "UST" if tx_coin == "uusd" else "Luna"
            # AMOUNT
            tx_amount = int(tx_msg['value']['amount'][0]['amount'])/1000000
            tx_amount_in = 0
            tx_amount_out = 0

            # FROM_ADDRESS
            tx_from_address = tx_msg['value']['from_address']
            if tx_from_address == target_account:
                tx_amount_out = -1 * tx_amount
            # IF-ELSE가 틀렸나?
            else:
                tx_amount_in = tx_amount
            # TO_ADDRESS
            tx_to_address = tx_msg['value']['to_address']
            # TIMESTAMP
            # "2022-05-11 09:11:52"(str type)을 datetime 객체로!
            tx_timestamp = tx_timestamp[0:10] + " " + tx_timestamp[11:-1]
            tx_UTC_TIME = datetime.strptime(tx_timestamp, '%Y-%m-%d %H:%M:%S') + timedelta(hours=9)
            # TERRA FINDER ADDRESS
            terra_finder = "https://finder.terra.money/mainnet/tx/"+tx_hash
            df = pd.concat([df, pd.DataFrame([[tx_type, tx_UTC_TIME,tx_hash, tx_memo, tx_coin, tx_amount_in, tx_amount_out, tx_from_address , tx_to_address, terra_finder]], columns=['type', 'time', 'tx_hash', 'memo','coin', 'tx_amount_in', 'tx_amount_out', 'from_address', 'to_address','terra_finder'])])

file_name =  F'{target_account}_TERRA_TRANSFER.xlsx'
df.to_excel(file_name, index=False)


