# gis_lecture2.py 
# python 3.8.13

"""
[folinum 사용법](https://cow97.tistory.com/34)
[geopandas 사용법](https://yganalyst.github.io/spatial_analysis/spatial_analysis_2/)
[Geo pandas 설치]() -> conda-forge channel add 하기 


	0) geopandas 설치 
	1) shp 파일 불러오기
	2) csv 파일 불러오기
	
	3) 데이터 편집하기 
		3-1) csv 파일 지리정보  데이터로 바꾸기 
		3-2) crs 부여하기 
		3-3) 좌표계 변경하기 

	4) Geopandas 오브젝트(객체) 속성 다루기 
		1. area : polygon 면적 
		2. length : 길이
		3. centroid : polygon 무게중심 
		4. boundary : 경계선 확인 
		5. is_valid : 도형 유효성 검사 . geom_type : 공간 객체 타입 
		6. 유효한 도형으로 만들기(buffer) 

	5) 시각화 
	6) 공간 데이터 심화 

	7)낙동강 데이터에 apply 하기 



"""
	
import os 
import sys 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import geopandas as gpd 
import folium
from shapely.geometry import Point, Polygon, LineString


# 1) shp 파일 불러오기

# load shp file and csv file 

file_path = '/Applications/anaconda3/envs/gis_env/git/shape/data'

os.listdir(file_path)


korea_adm_shp = gpd.read_file(
	file_path + '/korea_adm_shp/Z_SOP_BND_ADM_DONG_PG.shp',
	encoding='EUC-KR'
)

# 컬럼명 소문자로 변경 

korea_adm_shp.columns = map(str.lower, korea_adm_shp.columns)

korea_adm_shp.head()

# 2) csv 파일 불러오기

st_buck_data = pd.read_csv(
	file_path + '/starbucks.csv',
	encoding='EUC-KR'
)

st_buck_data.head()

# 3) 데이터 편집하기 

st_buck_data.rename(
	columns={
		'지점명': 'spot',
		'주소': 'address',
		'위도': 'lat',
		'경도': 'long'
	},
	inplace=True
)

st_buck_data.head()

# 3-1) csv 데이터 프레임 파일 Geo 데이터 프레임으로 바꾸기 

st_buck_data['geometry'] = st_buck_data.apply(
	lambda dt: Point([dt['long'],dt['lat']]),
	axis=1
)

st_buck_data = gpd.GeoDataFrame(
	st_buck_data,
	geometry = 'geometry'
)

## 좌표계 부여 (csv)

st_buck_data.crs = {'init': 'epsg:4326'}

# 좌표계 변경 change coordinate from 5181 to 4326(WGS84)
 
korea_adm_shp = korea_adm_shp.to_crs({'init': 'epsg:4326'})

st_buck_data.crs
korea_adm_shp.crs

# 4) Geopandas object 속성

"""
1. area : polygon 면적 
2. length : 길이
3. centroid : polygon 무게중심 
4. boundary : 경계선 확인 
5. is_valid : 도형 유효성 검사 . geom_type : 공간 객체 타입 

"""

# 4-1) 면적 (area)
# '도' 좌표계에서는 면적과 길이등이 제대로 계산이 안되므로 정확한 계산을 위해서는 '미터' 좌표계로 변경 
korea_adm_shp.geometry.area 

korea_adm_shp.to_crs({'init': 'epsg:5181'}).geometry.area

# 4-2) 길이 (테두리의 길이 반환)

korea_adm_shp.to_crs({'init': 'epsg:5181'}).geometry.length

# 4-3) 도형의 무게중싱 centroid 

korea_adm_shp.to_crs({'init': 'epsg:5181'}).geometry.centroid


# 4-4) boundary 확인 (서울)

## seoul 지역 추출 

adm_cond = korea_adm_shp.adm_dr_cd.str[0:2] == '11'

seoul_adm_shp = korea_adm_shp[adm_cond]

adr_cond = st_buck_data.address.str[0:2] == '서울'

seoul_st_buck_data = st_buck_data[adr_cond]

### boundary 확인 

ax = seoul_adm_shp.plot(color='black')
seoul_adm_shp.geometry.boundary.plot(ax=ax,color='white',linewidth=0.5)

seoul_adm_shp.plot(color='gray',alpha=1,edgecolor='black')
plt.show() 

seoul_adm_shp.geometry.boundary.coords


# 도형의 경계선임을 확인 

# 4-5) 도형 유효성 확인 
## 저번에도 얘기햇듯 도형의 마감처리가 잘 안되어있을 때 유효하지 않은 경우가 생김 

valid_cond = seoul_adm_shp.geometry.is_valid.map(lambda x: False if x else True)

## invalid 한 Polygon 추출
seoul_adm_shp[valid_cond]

# 4-6) 유효한 도형으로 만들기 

seoul_adm_shp_buff = seoul_adm_shp.buffer(0)

len(seoul_adm_shp_buff.geometry.is_valid)
sum(seoul_adm_shp_buff.geometry.is_valid)
seoul_adm_shp_buff.geometry.is_valid # 모든 폴리곤이 valid 한 폴리곤이 되었음 

# polygon 

with open('polygon.txt','w') as f: 
	f.write(
		str(korea_adm_shp.geometry[0:1])
	)


with open('line.txt','w') as f: 
	f.write(
		str(korea_adm_shp.geometry.boundary[0:1])
	)

# 일단 이건 스킵 
