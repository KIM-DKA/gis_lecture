
import os 
import sys 
import numpy as np 
import pandas as pd 
import geopandas as gpd
import importlib
import openpyxl
from time import time 


sys.path.append('/Applications/anaconda3/envs/myenv3/lib/python3.8/packages')

file_path = '/Users/dk/Documents/galleria/scheme/'

start = time() 
file_nm = list(filter(lambda s : 'xlsx' in s, os.listdir(file_path)))
end = time() 

file_nm 

file_path + file_nm[0]
# Excel sheet view 

pd.read_excel(os.listdir)

temp = pd.read_excel(file_path + file_nm[0],sheet_name=None)

help(pd.read_excel)

# count sheet number 

_ = pd.ExcelFile(file_path + file_nm[0])



