
# python 3.8.2 

import os 
import sys 
import numpy as np 
import pandas as pd 
import importlib
import openpyxl
import matplotlib.pyplot as plt 
from time import time 

import descartes
import geopandas as gpd
import shapely


'''

- QGIS란?
- 좌표계 정의 
- 공간 데이터란? (Point, Area) 
- 좌표계 변경하기 
- 공간 데이터 결합하기 
- 데이터 write 


'''


file_path = './shape/ulsan/'
file_nm = os.listdir('./shape/ulsan')
file_nm 
file_path + file_nm[0] 
file_nm

file_path + file_nm[0]
temp = gpd.read_file(file_path+file_nm[0],encoding='euc-kr')

temp.head()

temp.plot()

plt.show()

# 좌표계 정리 : https://www.osgeo.kr/17 


temp[['CTPRVN_CD']]

temp.iloc[0,[0,1]]

temp.crs
