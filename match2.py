#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 15:20:39 2019

@author: wenbo
"""

import pandas as pd 
import numpy as np 



age_dic = {'fifty':50, 'forty':40, 'seven':7, 'eleven':11,'eight':8,
              'eighty fivee':85,
              'seventy seven':77, 'six':6, 'sixteen':16,'sixx':6,
              'thirtythree':33, 'twenty':20
              }

smoke_dic = {'active_smoker':1, 'non-smoker':2, 'quit':3}
sex_dic = {'M':0, 'F':1}
job_dic = {'biz':'business owner','govt.':'government','private':'private sector'
,'privattte':'private sector'}
living_dic = {'r':'remote','remotee':'remote'}
living_num_dic = {'city':1,'remote':2,'City':1,'cIty':1,'ciTy':1,'CITY':1,'city ':1,'CIty':1}
job_num_dic = {'private sector':1,'government' :2, 'parental leave':3,'business owner':4,'unemployed':5}

File_PATH = "/Users/wenbo/Desktop/hackthon/train.csv" 

xl = pd.read_csv(File_PATH) 

new = xl["sex and age"].str.split(",", n = 1, expand = True)  

xl["sex"] = new[0] 
xl["age"] = new[1] 

old = xl["job_status and living_area"].str.split("?", n = 1, expand = True)  

xl["job_status"] = old[0] 
xl["living_area"] = old[1] 
#xl.to_csv('tmp.csv')
#byage = xl.groupby("age") 
#byage["sex"].describe() 

df = pd.DataFrame(xl) 
###删除有5个及以上空白数据的行
df=df.dropna(axis=0,thresh=4)
###将所有空白数据用0填充
df=df.fillna(0)
###删除这一列中的空格
df['sex and age'] = df['sex and age'].str.strip() 

for index, row in df.iterrows():
    temp = str(row['sex']) 
    temp.strip() 
    if temp[0] != 'M' and temp[0] != 'F':
        b, c = row['sex'], row['age'] 
        df.set_value(index, 'age', b) 
        df.set_value(index, 'sex', c) 
        #print(index, row['sex'],row['age']) 

df['sex'] = df['sex'].str.strip() 
df['age'] = df['age'].str.strip() 

###删除split后age列中这些奇葩的情况
df=df[(True^df['age'].isin(['Other','','M','Male','MM','MALE','Female','0','f','female','femalle','m','male','mmale','Female','Male','MM','MALE']))]
df=df[(True^df['sex'].isin(['Other',' ','f','female','femalle','m','male','mmale','Female','Male','MM','MALE']))]
df=df[(True^df['smoker_status'].isin([',',',,','.','11','>','>??','N?A','_','__','non>','quit?','���','?','??']))]



###根据前面的dic替换英文单词表示的数字
df.replace(age_dic, inplace=True)
df.replace(smoke_dic, inplace=True)
df.replace(sex_dic, inplace=True)

###删除'sex and age','job_status and living_area'这2列
df.drop('sex and age', axis=1, inplace=True)
df.drop('job_status and living_area', axis=1, inplace=True) 


#remove duplicate id
df.drop_duplicates('id',keep='last', inplace=True)
#smoke = df.groupby('smoker_status')
#print(smoke["smoker_status"].describe())





for index, row in df.iterrows():
    
    
    temp = str(row['living_area']) 
    temp.strip() 
    if temp:
        if temp[0] != 'C' and temp[0] != 'R':
            '''''
            print(index, row['sex and age'], row['job_status and living_area']) 
            '''''
            b, c = row['living_area'], row['job_status'] 
            df.set_value(index, 'job_status', b) 
            df.set_value(index, 'living_area', c) 
            #print(index, row['job_status'],row['living_area']) 


df['living_area'] = df['living_area'].str.strip() 
df=df[(True^df['living_area'].isin(['NULL','c','business_owner','private_sector','']))]
df['living_area'] = df['living_area'].map(object.__str__).map(str.lower).apply(str.replace,args=("'",''))



  

df.replace(living_dic,inplace=True)
df.replace(living_num_dic,inplace=True)
df=df[(True^df['job_status'].isin([0,'','NULL','null','c']))]
###把job_status所有的值转成小写
df['job_status'] = df['job_status'].map(str.lower).apply(str.replace,args=('_',' '))
# 把job status 按字典换
df.replace(job_dic, inplace=True)
df.replace(job_num_dic,inplace=True)

# 删除stroke_in_2018 的空格
df['stroke_in_2018'] = df['stroke_in_2018'].str.strip() 
df=df[(True^df['stroke_in_2018'].isin([',','.','','?','nuLL','N?A']))]


df=df[(True^df['BMI'].isin([',','?','nuLL','N?A']))]

df['heart_condition_detected_2017'] = df['heart_condition_detected_2017'].str.strip() 
df=df[(True^df['heart_condition_detected_2017'].isin(['.','?','n.a','N?A']))]
df['high_BP'] = df['high_BP'].str.strip() 
df=df[(True^df['high_BP'].isin([',','.,','','?','nuLL','N?A']))]

df['TreatmentD'] = df['TreatmentD'].str.strip() 
df=df[(True^df['TreatmentD'].isin(['0+E1860:E1868','.','','?','nuLL','N?A']))]




byage = df.groupby("living_area") 
print(byage["living_area"].describe())
df.to_csv('dataclean.csv')
#bysex = df.groupby("sex")
#print(bysex["sex"].describe())    
#byage = df.groupby("age") 
#print(byage["sex"].describe())
#print(df.head(6))
