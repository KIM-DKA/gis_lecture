# gis_lecture2.py 
# python 3.8.13

'''
[folinum 사용법](https://cow97.tistory.com/34)
[geopandas 사용법](https://yganalyst.github.io/spatial_analysis/spatial_analysis_2/)

[Geo pandas 설치]() 
	0) geopandas 사용법 
	1) shp 파일 불러오기 
	2) 엑셀파일 불러오기 
	3) 속성테이블 확인 
	4) 속성값 편집하기 (좌표계 변경) 
	5) sqlite DB 만들기 
	6) 좌표 데이터 변환, 속성 결합 하기 
	7) matplotlib 사용하기 
	8)낙동강 데이터 뿌려보기 

'''
	

import os 
import sys 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import geopandas as gpd 
import folium

