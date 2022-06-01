import pandas as pd
import datetime

file_name = "비브릭 운용 메타마스크 BSC 네트워크 입출금내역"
df = pd.read_excel(file_name+".xls")

# 1. Null 처리
df = df[df['Status'].isnull()==True]
# 2. KST Time
df['KST Time (GMT+9)'] = df.apply(lambda r: r['DateTime'] + datetime.timedelta(hours=9), axis = 1)
# 3. 원하는 열만 추출
df = df.loc[:,['KST Time (GMT+9)','Txhash','Method','From','To','Value_IN(BNB)','Value_OUT(BNB)']]
# 4. Datetime 내림차순 정렬
df.sort_values(by=["KST Time (GMT+9)"], ascending = False, inplace=True)
df.to_excel(file_name+'_v1.xlsx', index=False)
