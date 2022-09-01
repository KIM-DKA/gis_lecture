
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