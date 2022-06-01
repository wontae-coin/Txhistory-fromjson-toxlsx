import pandas as pd
import datetime

# NEAR BLOCKS에서 CSV 파일 다운로드 가능
file_name = "NEAR, FTX peertec에서 6140 NEAR 받은 의심 지갑 tx 내역"
df = pd.read_excel(file_name+".xls")
# thousand = "," 옵션은 csv를 읽어들일때만 가능하다


# 1. 2행을 Header로 설정
header = df.iloc[1]
df.columns = header
# 2. 잉여 1, 2행 삭제
df = df.iloc[2:]

# df['Method']에 batchTxns는 똑같은 행이 한 세개씩 겹쳐 나옵니다. 그거 다 어떻게 지우냐...
# 연속적인 행을 지우는 방법 연구 필요



# 3. KST Time
df['KST Time (GMT+9)'] = df.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)

# 4. Datetime 내림차순 정렬
df.sort_values(by=["KST Time (GMT+9)"], ascending = False, inplace=True)

df.rename(columns= {
    'DepositValue':'Deposit Value',
    'TransactionFee':'Transaction Fee'
}, inplace=True)

df = df.loc[:,['KST Time (GMT+9)','Txhash','Method','From','To','DepositValue','TransactionFee']]

# 5. PANDAS THOUSAND ',' 제거, float타입
df['Deposit Value'] = df.apply(lambda r:float(   r["Deposit Value"][:-2].replace(',',"")  ), axis=1)
df['Transaction Fee'] = df.apply(lambda r:float( r["Transaction Fee"][:-2].replace(',',"") ), axis=1)

# Ⓝ 이라고 되어있는거 NEAR 코드로

df.to_excel(file_name+'_v1.xlsx', index=False)

