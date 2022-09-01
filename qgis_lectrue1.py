
# python 3.8.2 

import os 
import sys 
import numpy as np 
import pandas as pd 
import geopandas as gpd
import importlib
import openpyxl
from time import time 

file_path = './shape/ulsan/'
file_nm = os.listdir('./shape/ulsan')[1]

file_path + file_nm 

temp = gpd.read_file(file_path+file_nm)


