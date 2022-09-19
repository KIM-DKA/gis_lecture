# gis_lecture2.py 
# python 3.10.6

"""
[geopandas 사용법](https://yganalyst.github.io/spatial_analysis/spatial_analysis_2/)
[Geo pandas 설치]() -> conda-forge channel add 하기 추가 
[Shapely 사용법](https://programmerpsy.tistory.com/104)
[folinum 사용법](https://cow97.tistory.com/34)
[shp 파일 다운로드](http://www.gisdeveloper.co.kr/?p=2332)                                                                                                                                                                                                                                                                                                                                                                                                                                                         ㅡ

	0) geopandas 설치
		* conda forge 채널 설정 

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
		3. dissolve 
		4. overlay [Intersection, Union, Symetrical Difference, Difference]
	
	7) 공간 결합 

	8) 결과물 저장(write)하기

	9) reference

	10) 다음 주제  
		1. fiona 라이브러리를 통한 시각화 
		2. 공간통계 

		


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

korea_st_buck_gdf = gpd.GeoDataFrame(
	korea_st_buck_data,
	geometry = 'geometry'
)


temp = korea_st_buck_gdf.copy
# 변수 버리는거 drop 함수 사용하기 


# 안쓰는 컬럼 버리기 

korea_st_buck_gdf = korea_st_buck_gdf[
	[
		'spot',
		'address',
		'geometry'
	]
]

korea_st_buck_gdf 


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
plt.show()



### boundary 확인 

ax = seoul_adm_shp.plot(color='black')
seoul_adm_shp.geometry.boundary.plot(ax=ax,color='white',linewidth=0.5)
seoul_adm_shp.plot(color='gray',alpha=1,edgecolor='black')

seoul_adm_shp.geometry.boundary.coords


# 도형의 경계선임을 확인 

# 4-5) 도형 유효성 확인 
## 저번에도 얘기햇듯 도형의 마감처리가 잘 안되어있을 때 유효하지 않은 경우가 생김 

valid_cond = seoul_adm_shp.geometry.is_valid.map(lambda x: False if x else True)

## invalid 한 Polygon 추출
seoul_adm_shp[valid_cond]

# 4-6) 유효한 도형으로 만들기 

seoul_adm_shp['geometry'] = seoul_adm_shp.buffer(0)

len(seoul_adm_shp.geometry.is_valid)
sum(seoul_adm_shp.geometry.is_valid)
seoul_adm_shp.geometry.is_valid # 모든 폴리곤이 valid 한 폴리곤이 되었음 



# 5. Shapely 사용법 



# 5-1) Point 

p1_pt = Point(
	[1,1],
)

p1_gdf = gpd.GeoDataFrame(
	{'geometry': p1_pt},
	index = [0]
)


p1_gdf.plot()
plt.show()

# 5-2) MultiPoint 

## 방법1 : MultiPoint 함수 이용 

p2_mpt = MultiPoint(
	[
		(0,0),
		(1,1)	
	]
)


p2_gdf = gpd.GeoDataFrame(
	{
		'geometry': p2_mpt
	},
	index = [0,1]
)

p2_gdf.plot()
plt.show()

## 방법2 : GeoSerires 사용 (개인적으론 Index 를 안줘도 되는 이 방법을 추천)

p3_sr = gpd.GeoSeries(
	[
		Point([0,0]),
		Point([1,1])
	]
)


p3_gdf = gpd.GeoDataFrame(
	{
		'geometry': p3_sr
	}
)

p3_gdf.plot()
plt.show()

# 5-2) LineString 

l1_sr = gpd.GeoSeries(
	[
		LineString([(0,0),(10,10)])	
	]
)

l1_sr.plot()
plt.show()

# 5-3) MultiLine 
# MultiLine 함수는 안써도 되는데 

l2_sr = MultiLineString(
	[
		[(0,0),(10,10)],
		[(0,10),(10,0)]	
	]
)

l2_gdf = gpd.GeoDataFrame(
	{
		'geometry': l2_sr	
	}, 
	index = [0,1]
)

l2_gdf.plot()
plt.show()

## 추천하는 방법 

l3_sr = gpd.GeoSeries(
	[
		LineString([(0,0),(10,10)]),
		LineString([(0,10),(10,0)])		
	]
)

l3_gdf = gpd.GeoDataFrame(
	{
		'geometry': l3_sr
	}

)


l3_gdf.plot()
plt.show()

# 5-4) Polygon
## Polygon 안 list 의 tuple(point) 순서에 따라 그림이 다르게 그려짐 

### 정사각형 

poly1_sqr_sr = gpd.GeoSeries(
	[
		Polygon([(0,0),(10,0),(10,10),(0,10)])
	] 
)


poly1_sqr_gdf = gpd.GeoDataFrame(
	{
		'geometry': poly1_sqr_sr	
	}
)


poly1_sqr_gdf.plot()
plt.show()


### 모래시계 모양 

poly2_hglas_sr = gpd.GeoSeries(
	[
		Polygon([(0,0),(10,0),(0,10),(10,10)])
	]
)

poly2_hglas_sr.plot()
plt.show()

# 5-5) MultiPolygon 

# 추천 방법 

poly3_gsr = gpd.GeoSeries(
	[
		Polygon([(0,0),(10,0),(5,5)]),
		Polygon([(5,5),(0,10),(10,10)])
	]
)

poly3_gdf = gpd.GeoDataFrame(
	{
		'geometry': poly3_gsr
	}
)

poly3_gdf.plot()
plt.show()

# 6. 공간데이터 활용하기 

# 6-1) bufffer 

# 500m 정사각형과 지름이 500미터인 원 그리기 

poly_square_500m_gsr = gpd.GeoSeries(
	[
		Polygon([(0,0),(500,0),(500,500),(0,500)])
	]
)

poly_square_500m_gdf = gpd.GeoDataFrame(
	{
		'gemotry':poly_square_500m_gsr
	}
)


pt_circle_gsr = gpd.GeoSeries(
	[
		Point([250,250])
	]
)

pt_circle_gdf = gpd.GeoDataFrame(
	{
		'geometry': pt_circle_gsr
	}
)


ax = poly_square_500m_gsr.plot()
pt_circle_gsr.buffer(250).plot(color='gray',ax=ax)
pt_circle_gsr.plot(color='black',ax=ax)
plt.show()

# 6-2) envelope : 도형을 감싸는 사각형을 그려줌 
# 중심점이 100,100 인 점을 하나 추가해줌, 여기서 부터는 GeoSeries 를 따로 선언 안하고 바로 지오 데이터 프레임으로 만듬 


add_two_point = gpd.GeoDataFrame(
	{
		'geometry': [Point(100,100),Point(200,200)]
	}
)

pt_circle_add_pt_gdf = pd.concat(
	[
		pt_circle_gdf,
		add_two_point
	],
	ignore_index=True
)



ax = pt_circle_add_pt_gdf.buffer(10).plot(edgecolor='black')
pt_circle_add_pt_gdf.buffer(10).envelope.plot(ax=ax,color='gray',alpha=0.5,edgecolor='black')
plt.show()

# 6-3) dissolve 

# 시군구를 시도로 융해(디졸브) 하기 
# 시군구 5자리로 group by 


seoul_adm_shp['group'] = seoul_adm_shp.adm_cd.str[0:5] 

ax = seoul_sig_shp.plot(edgecolor='black')
seoul_adm_shp.dissolve(by='group').plot(ax=ax,color='red',alpha=0.5,edgecolor='black')

# 해결책 
# 아주 작은 숫자 버퍼 주기 (연결되지 않은 도형 연결해 주기)


seoul_adm_shp['geometry'] = seoul_adm_shp.buffer(0.1)

seoul_adm_shp.dissolve(by='group').plot(color='red',alpha=0.5,edgecolor='black')

plt.show()

# 분명 시군구로 디졸브 했는데 왜이렇게 이상하게 합쳐졌을까? 
# 바로 유효하지 않은 도형이기 때문이다. 저번 강의처럼 버퍼를 줘서유효한 도형으로 만들면 행정동의 디졸브가 시군구의 디졸브와 같아짐 

# 6-4) overlay : 도형끼리 겹치는 부분 처리하기 
# 사다리꼴은 한강으로 가정 
# 사각형은 땅으로 가정 

poly_land_gdf = gpd.GeoDataFrame(
	{
		'geometry': [
			Polygon([(0,0),(2,0),(2,2),(0,2)]),
			Polygon([(3,3),(4,3),(4,4),(3,4)])
			
		]
	}
)

poly_river_gdf = gpd.GeoDataFrame(
	{
		'geometry': [
			Polygon([(0,1),(1,0),(3,2),(2,3)])
		]
	}
)

ax = poly_land_gdf.plot(color='brown',edgecolor='black',alpha=0.5)

poly_river_gdf.plot(ax=ax,color='blue',edgecolor='blue',alpha=0.5)

plt.show()

# Union (합집합)

poly_union_gdf = gpd.overlay(
	poly_land_gdf,
	poly_river_gdf,
	how = 'union'
)


poly_union_gdf.plot(edgecolor='black')
plt.show()


# Intersect (교집합)

poly_intersect_gdf = gpd.overlay(
	poly_land_gdf,
	poly_river_gdf,
	how = 'intersection'
)

poly_intersect_gdf

ax = poly_union_gdf.plot(edgecolor='black')

poly_intersect_gdf.plot(ax=ax,color='red',edgecolor='black')
plt.show()

# Symmetric difference (여집합)

poly_sym_diff_gdf = gpd.overlay(
	poly_land_gdf,
	poly_river_gdf,
	how = 'symmetric_difference'
)

ax = poly_union_gdf.plot(edgecolor='black')

poly_sym_diff_gdf.plot(ax=ax,color='red',edgecolor='black')
plt.show()


# difference (차집합)

poly_diff_gdf = gpd.overlay(
	poly_land_gdf,
	poly_river_gdf,
	how = 'difference'
)

ax = poly_union_gdf.plot(edgecolor='black')

poly_diff_gdf.plot(ax=ax,color='red',edgecolor='black')
plt.show()

# 7. Spatial Join 

# op = [within,contain,intersects,crosses,distance]

# within : 안에 있는가? 
# contain : 포함하는가 
# 사실상 같은 의미이나 매개변수의 순서를 어떻게 하느냐에 따라 달라짐 



merge_contain_gdf = gpd.sjoin(
	seoul_adm_shp, 
	seoul_st_buck_data
)










seoul_adm_shp.head()
seoul_st_buck_data.head()

ax = seoul_adm_shp.plot(edgecolor='black')
seoul_st_buck_data.plot(ax=ax,color='black',markersize=5)
plt.show()



# 1) seoul 결과물 저장하기 