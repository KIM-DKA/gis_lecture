# gis_lecture2.py 
# python 3.10.6

"""
[geopandas 사용법](https://yganalyst.github.io/spatial_analysis/spatial_analysis_2/)
[Geo pandas 설치]() -> conda-forge channel add 하기 추가 
[Shapely 사용법](https://programmerpsy.tistory.com/104)
[folinum 사용법](https://cow97.tistory.com/34)
[shp 파일 다운로드](http://www.gisdeveloper.co.kr/?p=2332)                                                                                                                                                                                                                                                                                                                                                                                                                                                         ㅡ

	0) geopandas 설치 

	1) shp 파일 불러오기
		* 저번 파일에 행정동 코드가 국가 통계코드로 행정동 코드(8자리 데이터 사용) 
	2) csv 파일 불러오기

	3) 데이터 편집하기 
		3-1) csv 파일 지리정보  데이터로 바꾸기 
		3-2) crs 부여하기 
		3-3) 좌표계 변경하기 

	4) Geopandas 오브젝트(객체) 속성 다루기 
		1.area : polygon 면적 
		2.length : 길이
		3.centroid : polygon 무게중심 
		4.boundary : 경계선 확인 
		5.is_valid : 도형 유효성 검사 . geom_type : 공간 객체 타입 
		6.유효한 도형으로 만들기(buffer) 

	5) shapely 사용법 

		1.Point(점)
		2.MulitPoint (여러 점)
		3.LineString(선)
		4.Polygon (면)
		5.Multipolygon (여러 도형)
	
	6) 공간데이터 활용하기 
		1. buffer 
		2. envelope
		3. unary_union 
		4. dissolve 
		5. overlay [Intersection, Union, Symetrical Difference, Difference]
		6. Spatial Join 

	7) folium 패키지로 시각화 하기 

	8) 결과물 shp 파일로 write 하기 

	9) 


"""
	
import os 
import sys 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import geopandas as gpd 
import folium
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon



# 1) shp 파일 불러오기

# load shp file and csv file 

file_path = '/Applications/anaconda3/envs/gis_env/git/shape/data'

os.listdir(file_path)


# 시도 
korea_sido_shp = gpd.read_file(
	file_path + '/korea_sido_shp/ctp_rvn.shp',
	encoding='EUC-KR'
)


# 시군구 
korea_sig_shp = gpd.read_file(
	file_path + '/korea_sig_shp/sig.shp',
	encoding='EUC-KR'
)

# 행정동 
korea_adm_shp = gpd.read_file(
	file_path + '/korea_adm_shp/emd.shp',
	encoding='EUC-KR'
)


# 2) csv 파일 불러오기

korea_st_buck_data = pd.read_csv(
	file_path + '/starbucks.csv',
	encoding='EUC-KR'
)

korea_st_buck_data.head()

# 3) 데이터 편집하기 


# 컬럼명 소문자로 변경 

korea_sido_shp.columns = map(str.lower, korea_sido_shp.columns)
korea_sig_shp.columns = map(str.lower, korea_sig_shp.columns)
korea_adm_shp.columns = map(str.lower, korea_adm_shp.columns)

korea_sido_shp.head()
korea_sig_shp.head()
korea_adm_shp.head()

# 시도 
korea_sido_shp.rename(
	columns = {
		'ctprvn_cd': 'sido_cd',
		'ctp_eng_nm': 'sido_eng_nm',
		'ctp_kor_nm': 'sido_kor_nm'
	},
	inplace=True
)


#행정동 

korea_adm_shp.rename(
	columns={
		'emd_cd': 'adm_cd',
		'emd_eng_nm': 'adm_eng_nm',
		'emd_kor_nm': 'adm_kor_nm'
	},
	inplace=True
)


#스타벅스 

korea_st_buck_data.rename(
	columns = {
		'지점명': 'spot',
		'주소': 'address',
		'위도': 'lat',
		'경도': 'long'
	},
	inplace=True
)

# 3-1) csv 데이터 프레임 파일 Geo 데이터 프레임으로 바꾸기 

korea_st_buck_data['geometry'] = korea_st_buck_data.apply(
	lambda dt: Point([dt['long'],dt['lat']]),
	axis=1
)

korea_st_buck_data = gpd.GeoDataFrame(
	korea_st_buck_data,
	geometry = 'geometry'
)

# 안쓰는 컬럼 버리기 

korea_st_buck_data = korea_st_buck_data[
	[
	'spot',
	'address',
	'geometry'
	]
]


## init 좌표계 부여 (csv)

korea_st_buck_data.crs = {'init': 'epsg:4326'}

# 좌표계 변경 change coordinate to 5179

korea_sido_shp = korea_sido_shp.to_crs({'init': 'epsg:5179'})
korea_sig_shp = korea_sig_shp.to_crs({'init': 'epsg:5179'})
korea_adm_shp = korea_adm_shp.to_crs({'init': 'epsg:5179'})

korea_st_buck_data = korea_st_buck_data.to_crs({'init': 'epsg:5179'})

# 4) Geopandas object 속성

# 4-1) 면적 (area)
# '도' 좌표계에서는 면적과 길이등이 제대로 계산이 안되므로 정확한 계산을 위해서는 '미터' 좌표계로 변경 
korea_adm_shp.geometry.area 

korea_adm_shp.geometry.area

# 4-2) 길이 (테두리의 길이 반환)

korea_adm_shp.geometry.length

# 4-3) 도형의 무게중싱 centroid 

korea_adm_shp.geometry.centroid


# 4-4) boundary 확인 (서울)

## seoul 지역 추출 (시도,군구,행정동)

sido_cond = (korea_sido_shp.sido_cd == '11')
sig_cond = (korea_sig_shp.sig_cd.str[0:2] == '11')
adm_cond = (korea_adm_shp.adm_cd.str[0:2] == '11')
adr_cond = (korea_st_buck_data.address.str[0:2] == '서울')

seoul_sido_shp = korea_sido_shp[sido_cond] 
seoul_sig_shp = korea_sig_shp[sig_cond]
seoul_adm_shp = korea_adm_shp[adm_cond]
seoul_st_buck_data = korea_st_buck_data[adr_cond]


seoul_sido_shp.plot(edgecolor='black')
seoul_sig_shp.plot(edgecolor='black')


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

seoul_adm_shp['geometry'] = seoul_adm_shp.buffer(1)

len(seoul_adm_shp.geometry.is_valid)
sum(seoul_adm_shp.geometry.is_valid)
seoul_adm_shp.geometry.is_valid # 모든 폴리곤이 valid 한 폴리곤이 되었음 


# 5. Shapely 사용법 



# 5-1) Point 

p1 = Point(
	[1,1],
)

p1 = gpd.GeoDataFrame(
	{'geometry': p1},
	index = [0]
)


p1.plot()
plt.show()

# 5-2) MultiPoint 

## 방법1 : MultiPoint 함수 이용 

p2 = MultiPoint(
	[
	(0,0),
	(1,1)	
	]
)


p2 = gpd.GeoDataFrame(
	{
	'geometry': p2
	},
	index = [0,1]
)

p2.plot()
plt.show()

## 방법2 : GeoSerires 사용 (개인적으론 Index 를 안줘도 되는 이 방법을 추천)

p3 = gpd.GeoSeries(
	[
	Point([0,0]),
	Point([1,1])
	]
)


p3 = gpd.GeoDataFrame(
	{
	'geometry': p2
	}
)


p2.plot()
plt.show()

# 5-2) LineString 

l1 = gpd.GeoSeries(
	[
	LineString([(0,0),(10,10)])	
	]
)

l1.plot()
plt.show()

# 5-3) MultiLine 
# MultiLine 함수는 안써도 되는데 

l2 = MultiLineString(
	[
	[(0,0),(10,10)],
	[(0,10),(10,0)]	
	]
)

l2 = gpd.GeoDataFrame(
	{
	'geometry': l2	
	}, 
	index = [0,1]
)

l2.plot()
plt.show()

## 추천하는 방법 

l3 = gpd.GeoSeries(
	[
	LineString([(0,0),(10,10)]),
	LineString([(0,10),(10,0)])		
	]
)

l3.plot()
plt.show()

# 5-4) Polygon
## Polygon 안 list 의 tuple(point) 순서에 따라 그림이 다르게 그려짐 

### 정사각형 
poly1 = gpd.GeoSeries(
	[
	Polygon([(0,0),(10,0),(10,10),(0,10)])
	] 
)


poly1 = gpd.GeoDataFrame(
	{
	'geometry': poly1	
	}
)


poly1.plot()
plt.show()


### 모래시계 모양 

poly2 = gpd.GeoSeries(
	[
	Polygon([(0,0),(10,0),(0,10),(10,10)])
	]
)

poly2.plot()
plt.show()



# 5-5) MultiPolygon 

# 추천 방법 

poly3 = gpd.GeoSeries(
	[
	Polygon([(0,0),(10,0),(5,5)]),
	Polygon([(5,5),(0,10),(10,10)])
	]
)

poly3 = gpd.GeoDataFrame(
	{
	'geometry': poly3
	}
)

poly3.plot()
plt.show()

# 6. 공간데이터 활용하기 

# 6-1) bufffer 

# 500m 정사각형과 지름이 500미터인 원 그리기 

sqaure_500m = gpd.GeoSeries(
	[
	Polygon([(0,0),(500,0),(500,500),(0,500)])
	]
)

circle_500m = gpd.GeoSeries(
	[
	Point([250,250])
	]
)

circle_500m.buffer(250)


ax = sqaure_500m.plot()
circle_500m.buffer(250).plot(color='gray',ax=ax)
circle_500m.plot(color='black',ax=ax)
plt.show()

# 6-2) envelope : 도형을 감싸는 사각형을 그려줌 
# 중심점이 100,100 인 점을 하나 추가해줌 

circle_100m = gpd.GeoSeries(
	[
	Point([100,100])
	]
)

circle = pd.concat(
	[
	circle_500m,
	circle_100m
	],
	axis=0
)

ax = circle.buffer(50).envelope.plot()
circle.buffer(50).plot(color='gray',ax=ax)
circle.plot(color='black',ax=ax)

plt.show()

# 6-3) dissolve 

# 시군구를 시도로 융해(디졸브) 하기 
# 시군구 5자리로 group by 


seoul_adm_shp['group'] = seoul_adm_shp.adm_cd.str[0:5] 

ax = seoul_sig_shp.plot(edgecolor='red')
seoul_adm_shp.dissolve(by='group').plot(edgecolor='black',ax=ax)

plt.show()

# 분명 시군구로 디졸브 했는데 왜이렇게 이상하게 합쳐졌을까? 
# 바로 유효하지 않은 도형이기 때문이다. 



# 다음주는 공간통계 기법, 분석을 낙동강 수질 예측에 적용 (업무 + 교육용)