
"""
1. ǰ�� ������ �ϱ� 

2. �鼼, ���� -> ���ֱ�

3. ()() [][] �� ���� ����, ��� (),[] �ڿ� ���� ��� �ؽ�Ʈ ���ֱ� ex) (��)�����޽�, (��)(��)�����޽�, [��]�����޽�, �����޽�(��)��Ǫ -> �����޽�
'[ ]|����|�鼼|[\(].+[\)]|[\[].+[\]]' 

4. ���� �� ���� ���ֱ� ex) �����޽��� -> �����޽�  ��������-ڸYOU -> �� ���� 
'[ ]|����|�鼼|[\(].+[\)]|[\[].+[\]]|��|'

5. �ؽ�Ʈ�� �ִ� Ư������ �� /, ���ֱ� ex) ����,�޽� -> �����޽�
'[ ]|����|�鼼|[\(].+[\)]|[\[].+[\]]|��|[\,]'
 
6. ���� �� ���� ���ֱ� (��Ʈ�� �� ���̱�) ex) �����޽� ��� -> �����޽���� 

7. \+ �ڿ� ���� ���� ���ֱ� ex) �����޽�+������ -> �����޽�
'[ ]|����|�鼼|[\(].+[\)]|[\[].+[\]]|��|[\,]|[\+].+'

8. \- �ھ� ���� ���� ���ֱ� ex) �����޽�-������ -> �����޽�
'[ ]|����|�鼼|[\(].+[\)]|[\[].+[\]]|��|[\,]|[\+\-\_\/].+'

9. \_ �ڿ� ���� ���ڵ� ���ֱ� ex) �����޽�_������ -> �����޽�

10. \/ �ڿ� ���� ���� ���ֱ� ex) �����޽�/������ -> �����޽�

"""


import os 
import sys 
import pandas as pd 
import re 

os.chdir('/Users/dk/Documents')


pumbun_df = pd.read_csv(
	'PUMBUN_CD ???????_1��_����.txt',
	usecols = ['bef_pumbun_cd','bef_pumbun_nm'],
	dtype=str
)

pumbun_nm = list(pumbun_df['bef_pumbun_nm'])
pumbun_cd = list(pumbun_df['bef_pumbun_cd'])



pattern = '����$|�鼼$|[\(].+[\)]|[\[].+[\]]|��|[\,]|[\+\-\_\/]|[\(].+|[\��].+[\��]'


# �̰��� �ؽ�Ʈ�� ������ ù ��° �ε����� ���� �غ��� 

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

# �׽�Ʈ �ڵ� 

temp = pd.DataFrame(
	{
		'ǰ���ڵ�': ['020631','027149','032142','042882'],
		'ǰ��': ['�����޽�','�����޽�(����)','�����޽�(�ð����)','�����޽���Ǿ']
	}
)

pumbun_nm = list(temp['ǰ��'])
pumbun_cd = list(temp['ǰ���ڵ�'])


aft_pumbun_nm = []
aft_pumbun_cd = []

result = []
for txt in pumbun_nm:
	txt_cum = ''

	for s in txt: 
		txt_cum += s # �ܾ ���� 
		if txt_cum in pumbun_nm: 
			# �����ϴٰ� ǰ�� ����Ʈ���� ������ �ش� ǰ���� ǰ���ڵ带 �����ͼ� ������ 
			idx = pumbun_nm.index(txt_cum) # �ش� ǰ���� index ��ġ 
			# txt_dict[pumbun_cd[idx]] = txt_cum
			aft_pumbun_nm.append(txt_cum)
			aft_pumbun_cd.append(pumbun_cd[idx])

			
			break 
		else: 
			pass 
