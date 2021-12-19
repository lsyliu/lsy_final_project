# -*- coding: utf-8 -*-
"""

@author: lsyliu
"""

import numpy as np
import pandas as pd
import re


df = pd.read_excel('info_all.xlsx')
df.head()
df = df.reset_index(drop=True)
df = df.drop(['horse_power','warranty'],axis = 1)#too many missing value
df.isnull().sum()

#set up search condition for a car
df = df[~df["price"].isnull()] #OK
df = df[~df['mileage'].isnull()] #OK
df = df[~df["year"].isnull()] #OK
df = df[~df['transmission'].isnull()] #OK
df = df[~df['body_type'].isnull()]
df = df[~df['model'].isnull()]
df = df[~df['location'].isnull()]

df = df.fillna('')
#download city cordinate data from Simple Map Website : https://simplemaps.com/data/us-cities
cord = pd.read_csv('uscities.csv')
cord = cord[['state_name','city','lat','lng','state_id']].drop_duplicates()

df['city'] =  df['location'].apply(lambda x: x.split(',')[0])
df['state'] =  df['location'].apply(lambda x: x.split(',')[1].strip())
df = df.merge(cord,how='left',left_on=('city','state'), right_on =('city','state_name'))
df = df[~df['lat'].isnull()]

#clea up variables
#1.price 
df['price'] =  df['price'].apply(lambda x: int(re.sub("\D", "", x))/100)
df['price'] = df['price'].astype(int)
round(df['price'].mean())#41634
price_low = round(np.percentile(df['price'], 25),0) # price <= 20000 low
price_medium =  round(np.percentile(df['price'], 50),0)# 20000 <price <40000 medium
price_high = round(np.percentile(df['price'], 75),0)# price > 40000 high

#2.mileage
round(df['mileage'].mean())#77597
mile_low = round(np.percentile(df['mileage'], 25),0) # mileage <= 16131 low
mile_medium =  round(np.percentile(df['mileage'], 50),0)# 16131< mileage <73106 medium
mile_high = round(np.percentile(df['mileage'], 75),0)# mileage > 73106 high
df = df[df['mileage'] <= 1000000]
#3.year
df['year'].unique()
df['year'].astype(int)
round(df['year'].mean())#2007
df = df[df['year'] != 0]

year_low = round(np.percentile(df['year'], 25),0) # year <= 2007 old
year_medium =  round(np.percentile(df['year'], 50),0)# 2007< year <2019 medium
year_high = round(np.percentile(df['year'], 75),0)# year > 2019 rather new

#4.transmission
df['transmission'].unique()
df['transmission'] =  df['transmission'].apply(lambda x: x.lower())
trans = df['transmission'].tolist()

for i in range(len(trans)):
    if 'auto' in trans[i]:
        trans[i] = 'automatic'
    else:
        trans[i] = 'manual'

df['transmission'] = trans        
df['transmission'].unique()    # 'manual', 'automatic'


#5.Body_type
df['body_type'] =  df['body_type'].apply(lambda x: x.lower())
df['body_type'].unique()


body_type = df['body_type'].tolist()

for i in range(len(body_type)):
    if 'convert' in body_type[i]:
        body_type[i] = 'convertible'
    elif 'coup' in body_type[i]:
        body_type[i] = 'coupe'
    elif '2dr car' in body_type[i]:
        body_type[i] = 'coupe' 
    elif '2 door' in body_type[i]:
        body_type[i] = 'coupe'         
    elif 'pickup' in body_type[i]:
        body_type[i] = 'pickup'
    elif 'truck' in body_type[i]:
        body_type[i] = 'pickup'    
    elif 'sedan' in body_type[i]:
        body_type[i] = 'sedan'          
    elif 'wagon' in body_type[i]:
        body_type[i] = 'wagon'        
    elif 'suv' in body_type[i]:
        body_type[i] = 'suv'         
    elif 'sport utility' in body_type[i]:
        body_type[i] = 'suv' 
    else:
        body_type[i] = 'other'     

df['body_type'] = body_type        
df['body_type'].unique() #'convertible', 'other', 'coupe', 'pickup', 'sedan', 'suv', 'wagon'


#6.brand
df['make'] =  df['make'].apply(lambda x: x.lower())
df_make = df.groupby('make')['year'].count().reset_index()
df_make.columns =['make','num']
df_make_top_list = df_make[df_make['num']>75]['make'].tolist()
df_make_other_list = df_make[df_make['num']<20]['make'].tolist()

#Top ten:  
#ford 1175 honda 605 chevroet 585 nissan 175 jeep 157 
#toyota 133 ram 108 gmc 85 bmw 81 subaru 78

make = df['make'].tolist()
for i in range(len(make)):
    if make[i] in df_make_other_list:
        make[i] = 'other'
    if 'other' in make[i]:
        make[i] = 'other'
    else: 
        continue
        
df['make'] = make        
len(df['make'].unique())# reduce to 26 cars, when make recommendation show df_make_top_list

df = df.reset_index(drop=True)

df['extra_info'] = ''
for i in range(len(df)):
    df['extra_info'][i] = 'Model: '+ str(df['model'][i]) +',  Engine: '+ str(df['engine'][i])  + ', Trim: '+ df['trim'][i] + ', Options: '+ df['options'][i] + ', Inner Color: '+ df['inter_color'][i] +', Outside color: '+ df['exter_color'][i]

df['extra_info'][1]



df.to_csv('data_cleaned.csv')