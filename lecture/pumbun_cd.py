
"""
1. 품번 오더링 하기 

2. 면세, 과세 -> 없애기

3. ()() [][] 와 같은 패턴, 멘뒤 (),[] 뒤에 오는 모든 텍스트 없애기 ex) (주)에르메스, (주)(주)에르메스, [주]에르메스, 에르메스(주)샴푸 -> 에르메스
'[ ]|과세|면세|[\(].+[\)]|[\[].+[\]]' 

4. 한자 外 외자 없애기 ex) 에르메스外 -> 에르메스  엔젤마켓-美YOU -> 미 뺴기 
'[ ]|과세|면세|[\(].+[\)]|[\[].+[\]]|外|'

5. 텍스트에 있는 특수문자 중 /, 없애기 ex) 에르,메스 -> 에르메스
'[ ]|과세|면세|[\(].+[\)]|[\[].+[\]]|外|[\,]'
 
6. 문자 내 띄어쓰기 없애기 (스트링 다 붙이기) ex) 에르메스 향수 -> 에르메스향수 

7. \+ 뒤에 나온 문자 없애기 ex) 에르메스+ㅁㅁㅁ -> 에르메스
'[ ]|과세|면세|[\(].+[\)]|[\[].+[\]]|外|[\,]|[\+].+'

8. \- 뒤애 나온 문자 없애기 ex) 에르메스-ㅁㅁㅁ -> 에르메스
'[ ]|과세|면세|[\(].+[\)]|[\[].+[\]]|外|[\,]|[\+\-\_\/].+'

9. \_ 뒤에 나온 문자도 없애기 ex) 에르메스_ㅁㅁㅁ -> 에르메스

10. \/ 뒤에 나온 문자 없애기 ex) 에르메스/ㅁㅁㅁ -> 에르메스

"""


import os 
import sys 
import pandas as pd 
import re 

os.chdir('/Users/dk/Documents')


pumbun_df = pd.read_csv(
	'PUMBUN_CD ???????_1차_정리.txt',
	usecols = ['bef_pumbun_cd','bef_pumbun_nm'],
	dtype=str
)

pumbun_nm = list(pumbun_df['bef_pumbun_nm'])
pumbun_cd = list(pumbun_df['bef_pumbun_cd'])



pattern = '과세$|면세$|[\(].+[\)]|[\[].+[\]]|外|[\,]|[\+\-\_\/]|[\(].+|[\（].+[\）]'


# 이거의 텍스트를 가지고 첫 번째 인덱스를 추출 해보면 

reg_pumbun_nm = [x.strip() for x in pumbun_nm]
reg_pumbun_nm = [re.sub(pattern,'',x) for x in reg_pumbun_nm]



aft_pumbun_cd = []
aft_pumbun_nm = [] 


for t in reg_pumbun_nm:

	idx = reg_pumbun_nm.index(t)
	aft_pumbun_cd.append(pumbun_cd[idx])
	aft_pumbun_nm.append(pumbun_nm[idx])



txt_df = pd.DataFrame(
	{
		'bef_pumbun_cd': pumbun_cd,
		'bef_pumbun_nm': pumbun_nm,
		'aft_pumbun_nm': reg_pumbun_nm,
		'aft_pumbun_cd': aft_pumbun_cd
	}
)



txt_df = txt_df.sort_values('aft_pumbun_cd')

txt_df.to_csv('PUMBUN_CD.txt',index=False,encoding ='euc-kr')

len(txt_df.aft_pumbun_cd.unique())






############################################################################################################

# 테스트 코드 

temp = pd.DataFrame(
	{
		'품번코드': ['020631','027149','032142','042882'],
		'품번': ['에르메스','에르메스(수선)','에르메스(시계수선)','에르메스퍼퓸']
	}
)

pumbun_nm = list(temp['품번'])
pumbun_cd = list(temp['품번코드'])


aft_pumbun_nm = []
aft_pumbun_cd = []

result = []
for txt in pumbun_nm:
	txt_cum = ''

	for s in txt: 
		txt_cum += s # 단어를 누적 
		if txt_cum in pumbun_nm: 
			# 누적하다가 품번 리스트에서 만나면 해당 품목의 품목코드를 가져와서 저장함 
			idx = pumbun_nm.index(txt_cum) # 해당 품목의 index 위치 
			# txt_dict[pumbun_cd[idx]] = txt_cum
			aft_pumbun_nm.append(txt_cum)
			aft_pumbun_cd.append(pumbun_cd[idx])

			
			break 
		else: 
			pass 
