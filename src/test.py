#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project:     Desktop
# @Filename:    test.py
# @Author:      staceyrivet
# @Time:        7/19/22 5:53 PM
# @IDE:         PyCharm

import os
import pandas as pd

path = 'data/'
dir_list = os.listdir(path)
print(dir_list)

for f in dir_list:
    if f == 'cb_2018_us_state_500k.shp':
        file = f

#state_data = pd.read_csv(path+dir_list[-1])
print("GDSGD", f'path + file')