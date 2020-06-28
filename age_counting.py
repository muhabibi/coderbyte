import requests
import numpy as np 
import pandas as pd
import json 
import re

r = requests.get('http://coderbyte.com/api/challenges/json/age-counting')
data_list = r.json()['data']
cast_ages = []
ages = re.findall(r'age=(\d+),', data_list)
i=0
for age in ages:
    if int(age) >= 50 : i+=1
    
print(i)
