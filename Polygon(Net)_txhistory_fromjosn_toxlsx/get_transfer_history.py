import pandas as pd
import datetime

TARGET_ADDRESS = "0x81251d5047f57bb6158d39b72ae1bf92faf26261"

file_matic = "Peertec 메타마스크 Polygon 네트워크 입출금"
df_matic = pd.read_excel(file_matic+".xls")

# 1. Null 처리
df_matic = df_matic[df_matic['Status'].isnull()==True]
# 2. KST Time
df_matic['KST Time (GMT+9)'] = df_matic.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)

df_matic['Value'] = df_matic.apply(lambda r:r['Value_OUT(MATIC)'] if r['From'] == TARGET_ADDRESS else r["Value_IN(MATIC)"], axis=1)

# 토큰 티커도 만들어줘야 함
df_matic['TICKER'] = df_matic.apply(lambda r: 'MATIC', axis=1)
df_matic["ERC20 Token Contract Address"] = df_matic.apply(lambda r: None, axis=1)

# 3. 원하는 열만 추출
df_matic = df_matic.loc[:,['KST Time (GMT+9)','Txhash','Method',"TICKER",'From','To','Value']]


file_ERC20 = "Peertec 메타마스크 Polygon ERC20"
df_ERC20 = pd.read_excel(file_ERC20+".xls")

# 1. KST Time
df_ERC20['KST Time (GMT+9)'] = df_ERC20.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)

# 2. Dummy Method
df_ERC20['Method'] = df_ERC20.apply(lambda r: 'Transfer', axis=1)

# 2. 원하는 열만 추출
df_ERC20 = df_ERC20.loc[:,['KST Time (GMT+9)','Txhash','Method','TokenSymbol','From','To', "Value", "ContractAddress"]]

df_ERC20.rename(columns = {
    "TokenSymbol":"TICKER",
    "ContractAddress":"ERC20 Token Contract Address"
}, inplace=True)    


# 1. 합치기
df = pd.concat([df_matic, df_ERC20])
# 2 Datetime 내림차순 정렬
df.sort_values(by=["KST Time (GMT+9)"], ascending = False, inplace=True)


df.to_excel(file_matic + "+ERC20.xlsx", index=False)