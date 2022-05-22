import pandas as pd
import requests_html
from bs4 import BeautifulSoup
import datetime

df = pd.read_excel("비브릭 운용 메타마스크 지갑 Ethereum(Net) transfer history 2022년.xls")

# 1. Null 처리
df = df[df['Status'].isnull()==True]
# 2. KST Time
df['KST Time (GMT+9)'] = df.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)
# 3. 원하는 열만 추출
df = df.loc[:,['KST Time (GMT+9)','Txhash','Method','From','To']]
# 4. Datetime 내림차순 정렬
df.sort_values(by=["KST Time (GMT+9)"], ascending = False, inplace=True)


# 5. 타겟 지갑 주소를 from, to와 비교한다
main_wallet_address = "0x8f27fa136ff4da1796368380019029d81d12d06d"
df['TargetAddress'] = df.apply(lambda r: r['To'] if r['From'] == main_wallet_address else r['From'], axis = 1)

# 6. 크롤링
etherscan_url = "https://etherscan.io/address/"
target_address = "0x8dbe9c44a42050da44f075149c1ff49b18bcaf3f"

# vscode 파이썬 디버깅
session = requests_html.HTMLSession()
res = session.get(etherscan_url + target_address)
res.html.render()
soup = BeautifulSoup(res.html.html, "html.parser")
print(soup)
address_or_contract = soup.select("#content > div.container.py-3 > div > div.mb-3.mb-lg-0 > h1")
print(address_or_contract)
