import pandas as pd
import datetime


# UST 는 너무 많아서 5일치밖에 안나옴
# UST 토큰 컨트랙트는 이더리움 지갑에서 들어와서 자기자신(UST 토큰 컨트랙트)로 들어온것만 나오지, 어느 테라 토큰으로 갔는지는 나오지 않는다


file_ETH = "Peertec 메타마스크 Ethereum 네트워크 2022년"
df_ETH = pd.read_excel(file_ETH+".xls")

TARGET_ADDRESS = "0x81251d5047f57bb6158d39b72ae1bf92faf26261"

# 1. Null 처리
df_ETH = df_ETH[df_ETH['Status'].isnull()==True]
# 2. KST Time
df_ETH['KST Time (GMT+9)'] = df_ETH.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)

df_ETH['Value'] = df_ETH.apply(lambda r:r['Value_OUT(ETH)'] if r['From'] == TARGET_ADDRESS else r["Value_IN(ETH)"], axis=1)

# 토큰 티커도 만들어줘야 함
df_ETH['TICKER'] = df_ETH.apply(lambda r: 'ETH', axis=1)
df_ETH["ERC20 Token Contract Address"] = df_ETH.apply(lambda r: None, axis=1)

# 3. 원하는 열만 추출
df_ETH = df_ETH.loc[:,['KST Time (GMT+9)','Txhash','Method',"TICKER",'From','To','Value']]


file_ERC20 = "Peertec 메타마스크 이더리움 ERC20"
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
df = pd.concat([df_ETH, df_ERC20])
# 2 Datetime 내림차순 정렬
df.sort_values(by=["KST Time (GMT+9)"], ascending = False, inplace=True)


df.to_excel(file_ETH + "+ ERC20.xlsx", index=False)
