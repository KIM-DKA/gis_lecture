import os 
import sys 
import pandas as pd 
import re 




# read data 
pumbun_df = pd.read_excel(
	io='PUMBUN_CD 코드명.xlsx',
)

pumbun_nm = list(pumbun_df['품번'])
pumbun_cd = list(pumbun_df['품번코드'])



txt_dict = {}

for txt in pumbun_nm:
	txt_cum = ''

	for s in txt: 
		txt_cum += s # 단어를 누적 
		
		if txt_cum in pumbun_nm: 
			# 누적하다가 품번 리스트에서 만나면 해당 품목의 품목코드를 가져와서 저장함 
			idx = pumbun_nm.index(txt_cum) # 해당 품목의 index 위치 
			txt_dict[pumbun_cd[idx]] = txt_cum

			print(txt_cum)
			break 
			
		else: 
			pass 



txt_df = pd.DataFrame(
	list(txt_dict.items()),
	columns = ['품번코드','품번']
).to_csv('PUMBUN_CD 코드명_1차_정리.csv',index=False,encoding ='euc-kr')


############################################################################################################

# 테스트 코드 

temp = pd.DataFrame(
	{
		'품번코드': ['020631','027149','032142','042882'],
		'품번': ['에르메스','에르메스(수선)','에르메스(시계수선)','에르메스퍼퓸']
	}
)

txt_dict = {}

pumbun_nm = list(temp['품번'])
pumbun_cd = list(temp['품번코드'])

for txt in pumbun_nm:
	txt_cum = ''

	for s in txt: 
		txt_cum += s # 단어를 누적 
		print(txt_cum)
		if txt_cum in pumbun_nm: 
			# 누적하다가 품번 리스트에서 만나면 해당 품목의 품목코드를 가져와서 저장함 
			idx = pumbun_nm.index(txt_cum) # 해당 품목의 index 위치 
			txt_dict[pumbun_cd[idx]] = txt_cum
			
			break 
		else: 
			pass 

txt_dict


# 특수문자, 과세, 면세등 특정 패턴으로 인하여 그룹핑이 안되는 애들은 합의만 하고 목요일 까지 전달 할 것 
# 디비 들어가서 조인하고 살아 남는 애들 확인 


# 과세, 면세, (듀퐁) 이런거 다 날리기 

# bef_cd / aft_ct / bef_nm / aft_nm 
