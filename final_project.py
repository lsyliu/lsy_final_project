# -*- coding: utf-8 -*-
"""

@author: lsyliu
"""

import json
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import plotly.graph_objects as go
import webbrowser


#caching
def load_cache(CACHE_FILENAME):
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict,CACHE_FILENAME):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()

def make_url_request_using_cache(url, cache):
    ''' Check the cache for a saved result for this url. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    url: string
        The URL for the website
        
    cache: a cache file    
    
    Returns
    -------
    cache[url]
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    if url in cache: # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text 
        save_cache(cache,CACHE_FILENAME)
        return cache[url] # in both cases, we return cache[url]

CACHE_FILENAME = "car_data.json"
cars_caching_file = load_cache(CACHE_FILENAME)

#Tree
class Tree():
    ''' create a generic tree '''
    def __init__(self, root):
        self.root = root
        self.children = []
        self.Nodes = []
        self.all_info = {}
        
    def addNode(self,obj):
        self.children.append(obj)
    
    def getAllNodes(self):
        self.Nodes.append(self.root)
        for child in self.children:
            self.Nodes.append(child.data)
        for child in self.children:
            if child.getChildNodes(self.Nodes) != None:
                child.getChildNodes(self.Nodes)
        print(*self.Nodes, sep = "\n")
        print('Tree Size:' + str(len(self.Nodes)))
        
class Node():
    
    def __init__(self, data):
        self.data = data
        self.children = []
       # self.key = key
       # self.val = val
       # self.all_info = {}
        
    def addNode(self,obj):
        self.children.append(obj)
        
    def getChildNodes(self,Tree):
        for child in self.children:
            if child.children:
                child.getChildNodes(Tree)
                Tree.append(child.data)
            else:
                Tree.append(child.data)
                
    #def loadCarInfo(self, data):
        

#### level 1 - root ####        
carInfo = Tree('Cars')  #Create a tree and add root data
#print(carInfo.root) #ask the Tree for it's root

#### level 2 - price ####

# Add children to root 
carInfo.addNode(Node('0-20000')) #top 25% by ascending prices
carInfo.addNode(Node('20000-40000')) #25%-75%
carInfo.addNode(Node('40000-more')) #bottom 25%

# Get children of root
#print(f'The three levels of prices are {", ".join(str(child.data) for child in carInfo.children)}')

#### level 3 - transmission ####

# Add Node to the first child of the Tree
carInfo.children[0].addNode(Node('Manual'))
carInfo.children[0].addNode(Node('Automatic'))
carInfo.children[1].addNode(Node('Manual'))
carInfo.children[1].addNode(Node('Automatic'))
carInfo.children[2].addNode(Node('Manual'))
carInfo.children[2].addNode(Node('Automatic'))

# Get the first child of the first child of the Tree
#print(f'The transmission options are: {carInfo.children[0].children[0].data} and {carInfo.children[0].children[1].data} for all three levels of prices')

#### level 4 - year #### 

#price lower than $20,000 and Manual 
carInfo.children[0].children[0].addNode(Node('before 1999'))
carInfo.children[0].children[0].addNode(Node('after 1999'))

#price lower than $20,000 and Auto
carInfo.children[0].children[1].addNode(Node('before 2013'))
carInfo.children[0].children[1].addNode(Node('after 2013'))

#Prices between $20,000-$40,000 and Manual
carInfo.children[1].children[0].addNode(Node('before 2011'))
carInfo.children[1].children[0].addNode(Node('after 2011'))

#Prices between $20,000-$40,000 and Auto
carInfo.children[1].children[1].addNode(Node('before 2017'))
carInfo.children[1].children[1].addNode(Node('after 2017'))

#Prices higher than $40,000 and Manual
carInfo.children[2].children[0].addNode(Node('before 2007'))
carInfo.children[2].children[0].addNode(Node('after 2007'))

#Prices higher than $40,000 and Auto
carInfo.children[2].children[1].addNode(Node('before 2019'))
carInfo.children[2].children[1].addNode(Node('after 2019'))

#print(carInfo.children[2].children[1].children[0].data)

#### level 5 - body type ####

#price lower than $20,000, Manual, Before Year 1999
carInfo.children[0].children[0].children[0].addNode(Node('convertible'))
carInfo.children[0].children[0].children[0].addNode(Node('coupe'))
carInfo.children[0].children[0].children[0].addNode(Node('pickup'))
carInfo.children[0].children[0].children[0].addNode(Node('sedan'))
carInfo.children[0].children[0].children[0].addNode(Node('suv'))
carInfo.children[0].children[0].children[0].addNode(Node('wagon'))
carInfo.children[0].children[0].children[0].addNode(Node('other'))

#price lower than $20,000, Manual, After Year 1999
carInfo.children[0].children[0].children[1].addNode(Node('convertible'))
carInfo.children[0].children[0].children[1].addNode(Node('coupe'))
carInfo.children[0].children[0].children[1].addNode(Node('pickup'))
carInfo.children[0].children[0].children[1].addNode(Node('sedan'))
carInfo.children[0].children[0].children[1].addNode(Node('suv'))
carInfo.children[0].children[0].children[1].addNode(Node('wagon'))
carInfo.children[0].children[0].children[1].addNode(Node('other'))

#price lower than $20,000, Auto, Before Year 2013
carInfo.children[0].children[1].children[0].addNode(Node('convertible'))
carInfo.children[0].children[1].children[0].addNode(Node('coupe'))
carInfo.children[0].children[1].children[0].addNode(Node('pickup'))
carInfo.children[0].children[1].children[0].addNode(Node('sedan'))
carInfo.children[0].children[1].children[0].addNode(Node('suv'))
carInfo.children[0].children[1].children[0].addNode(Node('wagon'))
carInfo.children[0].children[1].children[0].addNode(Node('other'))

#price lower than $20,000, Auto, After Year 2013
carInfo.children[0].children[1].children[1].addNode(Node('convertible'))
carInfo.children[0].children[1].children[1].addNode(Node('coupe'))
carInfo.children[0].children[1].children[1].addNode(Node('pickup'))
carInfo.children[0].children[1].children[1].addNode(Node('sedan'))
carInfo.children[0].children[1].children[1].addNode(Node('suv'))
carInfo.children[0].children[1].children[1].addNode(Node('wagon'))
carInfo.children[0].children[1].children[1].addNode(Node('other'))

#Prices between $20,000-$40,000, Manual, Before Year 2011
carInfo.children[1].children[0].children[0].addNode(Node('convertible'))
carInfo.children[1].children[0].children[0].addNode(Node('coupe'))
carInfo.children[1].children[0].children[0].addNode(Node('pickup'))
carInfo.children[1].children[0].children[0].addNode(Node('sedan'))
carInfo.children[1].children[0].children[0].addNode(Node('suv'))
carInfo.children[1].children[0].children[0].addNode(Node('wagon'))

#Prices between $20,000-$40,000, Manual, After Year 2011
carInfo.children[1].children[0].children[1].addNode(Node('convertible'))
carInfo.children[1].children[0].children[1].addNode(Node('coupe'))
carInfo.children[1].children[0].children[1].addNode(Node('pickup'))
carInfo.children[1].children[0].children[1].addNode(Node('sedan'))
carInfo.children[1].children[0].children[1].addNode(Node('suv'))
carInfo.children[1].children[0].children[1].addNode(Node('wagon'))
carInfo.children[1].children[0].children[1].addNode(Node('other'))

#Prices between $20,000-$40,000, Auto, Before Year 2017
carInfo.children[1].children[1].children[0].addNode(Node('convertible'))
carInfo.children[1].children[1].children[0].addNode(Node('coupe'))
carInfo.children[1].children[1].children[0].addNode(Node('pickup'))
carInfo.children[1].children[1].children[0].addNode(Node('sedan'))
carInfo.children[1].children[1].children[0].addNode(Node('suv'))
carInfo.children[1].children[1].children[0].addNode(Node('wagon'))
carInfo.children[1].children[1].children[0].addNode(Node('other'))

#Prices between $20,000-$40,000, Auto, After Year 2017
carInfo.children[1].children[1].children[1].addNode(Node('convertible'))
carInfo.children[1].children[1].children[1].addNode(Node('coupe'))
carInfo.children[1].children[1].children[1].addNode(Node('pickup'))
carInfo.children[1].children[1].children[1].addNode(Node('sedan'))
carInfo.children[1].children[1].children[1].addNode(Node('suv'))
carInfo.children[1].children[1].children[1].addNode(Node('wagon'))
carInfo.children[1].children[1].children[1].addNode(Node('other'))

#Prices higher than $40,000, Manual, Before Year 2007
carInfo.children[2].children[0].children[0].addNode(Node('convertible'))
carInfo.children[2].children[0].children[0].addNode(Node('coupe'))
carInfo.children[2].children[0].children[0].addNode(Node('pickup'))
carInfo.children[2].children[0].children[0].addNode(Node('sedan'))
carInfo.children[2].children[0].children[0].addNode(Node('suv'))
carInfo.children[2].children[0].children[0].addNode(Node('wagon'))
carInfo.children[2].children[0].children[0].addNode(Node('other'))

#Prices higher than $40,000, Manual, After Year 2007
carInfo.children[2].children[0].children[1].addNode(Node('convertible'))
carInfo.children[2].children[0].children[1].addNode(Node('coupe'))
carInfo.children[2].children[0].children[1].addNode(Node('pickup'))
carInfo.children[2].children[0].children[1].addNode(Node('sedan'))
carInfo.children[2].children[0].children[1].addNode(Node('suv'))
carInfo.children[2].children[0].children[1].addNode(Node('wagon'))
carInfo.children[2].children[0].children[1].addNode(Node('other'))

#Prices higher than $40,000, Auto, Before Year 2019
carInfo.children[2].children[1].children[0].addNode(Node('convertible'))
carInfo.children[2].children[1].children[0].addNode(Node('coupe'))
carInfo.children[2].children[1].children[0].addNode(Node('pickup'))
carInfo.children[2].children[1].children[0].addNode(Node('sedan'))
carInfo.children[2].children[1].children[0].addNode(Node('suv'))
carInfo.children[2].children[1].children[0].addNode(Node('wagon'))
carInfo.children[2].children[1].children[0].addNode(Node('other'))

#Prices higher than $40,000, Auto, After Year 2019
carInfo.children[2].children[1].children[1].addNode(Node('convertible'))
carInfo.children[2].children[1].children[1].addNode(Node('coupe'))
carInfo.children[2].children[1].children[1].addNode(Node('pickup'))
carInfo.children[2].children[1].children[1].addNode(Node('sedan'))
carInfo.children[2].children[1].children[1].addNode(Node('suv'))
carInfo.children[2].children[1].children[1].addNode(Node('wagon'))
carInfo.children[2].children[1].children[1].addNode(Node('other'))
#print(carInfo.children[2].children[1].children[0].children[0].data)
#carInfo.getAllNodes()


##### data structuring

df = pd.read_csv("data_cleaned.csv")
df = df.fillna('')

def create_us_graph(data):
    ''' create graph of the number of used cars on map

    Parameters
    ----------
    data: contains cars' locations and numbers 

    Returns
    -------
    map: shows the locations of cars and the numbers of cars
    '''
    data_graph = data.groupby('state_id')['title'].count().reset_index()
    fig = go.Figure(data=go.Choropleth(
        locations=data_graph['state_id'], # 
        z = data_graph['title'].astype(float), 
        locationmode = 'USA-states', 
        colorscale = 'Reds', 
        colorbar_title = "Number of car", 
        ))

    fig.update_layout(
        title_text = 'Used Car Number in US',
        geo_scope='usa', 
        )
    
    fig.write_html("Your_used_car_choices_in_US.html")


def car_info_detail1(data):
    ''' show information for one specific used car

    Parameters
    ----------
    data: contains all sorts of cars' infomation 

    Returns
    -------
    table: generates the chosen car's information
    
    '''
    print ('The best and only choice you have is ' + str(data['title'].tolist()[0]))
    time.sleep(1.5)
    print('The price is $'+ str(int(data['price'].tolist()[0])))
    print('The mileage is '+ str(int(data['mileage'].tolist()[0]))+ ' km.')
    print('It was produced in '+ str(int(data['year'].tolist()[0])))
    print('The body type is '+ str((data['body_type'].tolist()[0]))+ ' as you like.')
    print('The transmission is '+ str((data['transmission'].tolist()[0]))+ ' as you like.')
    print('The make is  '+ str((data['make'].tolist()[0]))+ '.')
    print('The model is  '+ str((data['model'].tolist()[0]))+ '.')
    print('The engine is  '+ str((data['engine'].tolist()[0]))+ '.')
    print('The outside color is  '+ str((data['exter_color'].tolist()[0])))
    print('The inner color is  '+ str((data['inter_color'].tolist()[0])))
    print('Here are extra infomation '+ str((data['options'].tolist()[0]))  + ' '+ str((data['power options'].tolist()[0]))) 
    time.sleep(1)
    print("You can check the comparasion of 'year', 'price' or 'mileage' between this car and all car,or simply a map of this car's location")

    while True:
        comparations = input("Please choose from 'year', 'price', 'mileage', 'map'  Input here: ")
        if not str(comparations).lower() in ['year', 'price', 'mileage','map']:
            print("Please choose from 'year', 'price','mileage'or 'map'! ")    
        else:
            break
    
    plt.style.use('ggplot')
    sns.set(style="whitegrid")

    if comparations == 'year':
        ax = sns.boxplot(y="year", data=df)
        plt.xlabel('All cars')
        plt.axhline(y=int(data['year'].tolist()[0]),ls=":",c="red")
        plt.title('Year Compared to All Cars')
        plt.show()

    elif comparations == 'price':
        ax = sns.boxplot(y="price", data=df)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        plt.ylim(0,700000)
        plt.xlabel('All cars')
        plt.axhline(y=int(data['price'].tolist()[0]),ls=":",c="red")
        plt.title('Price Compared to All Cars')
        plt.show()

    elif comparations == 'mileage':
        ax = sns.boxplot(y="mileage", data=df)
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        plt.ylim(0,400000)
        plt.xlabel('All cars')
        plt.axhline(y=int(data['mileage'].tolist()[0]),ls=":",c="red")
        plt.title('Mileage Compared to All Cars')
        plt.show()
    else:
        create_us_graph(data)
        print('Map has been saved! Check it in your local directory!')
        time.sleep(1.5)
    
   
    print('If you want to have more infomation, here is the link: '+ str((data['url'].tolist()[0])))
#    while True:
#        y_n = input("Do you want to open the link: 'y' or 'n'  Input here: ")
#        if not str(y_n) in ['y','n']:
#            print("Please choose from 'y','n'! ") 
#        else:
#            break
#        if y_n == 'y':
#            webbrowser.open(str(data['url'].tolist()[0]))
#        else:
#            continue


def car_info_detail20(data):
    ''' show information for more than one used cars

    Parameters
    ----------
    data: contains all sorts of cars' infomation 

    Returns
    -------
    table: generates a list of car's information
    
    '''

    data['car_num'] = range(1,len(data)+1)
    url_lists = data[['car_num','url']].reset_index(drop=True)
    title_lists = data[['car_num','title']].reset_index(drop=True)
    extra_lists = data[['car_num','extra_info']].reset_index(drop=True)

    print ('Your choices are shown below: ')
    time.sleep(1)
    print(title_lists)
    print ('Each car has a car number which you can rely on when you choose car in the future! ')
    print('The average price is $'+ str(int(data['price'].mean())))
    print('The average mileage is '+ str(int(data['mileage'].mean()))+ ' km.')
    print('Ihe average year is '+ str(int(data['year'].mean())))
    print('The body type is '+ str((data['body_type'].tolist()[0]))+ ' as you like.')
    print('The transmission is '+ str((data['transmission'].tolist()[0]))+ ' as you like.')
    time.sleep(1)
    print("You can check different features of all your chosen cars")
    time.sleep(1)

    while True:
        comparations = input("Please choose from 'price', 'year','mileage','map' Input here: ")
        if not str(comparations).lower() in ['price', 'year','mileage','map']:
            print("Please choose from 'price', 'year','mileage','map'! ")    
        else:
            break
        
    plt.style.use('ggplot')
    sns.set(style="whitegrid")

    #price mielage year
    if comparations == 'price':      
        ax = sns.barplot(x='car_num',y="price", data=data)
        plt.xlabel('Car number of your chosen cars')
        plt.ylabel('Price')
        plt.title('Price Of Your Choice')
        plt.show()
        
    elif comparations == 'year':          
        ax = sns.barplot(x='car_num',y="year", data=data)
        plt.xlabel('Car number of your chosen cars')
        plt.ylabel('Year')
        plt.ylim(data['year'].min()-2,data['year'].max()+2)
        plt.title('Year Of Your Choice')
        plt.show()
        
    elif comparations == 'mileage':            
        ax = sns.barplot(x='car_num',y="mileage", data=data)
        plt.xlabel('Car number of your chosen cars')
        plt.ylabel('Mileage')
        plt.title('Mileage Of Your Choice')
        plt.show()  
        
    else:
        create_us_graph(data)
        print('Map has been saved! Check it in your local directory!')
        time.sleep(1.5)

    print('Here are extra infomation!')
    time.sleep(1)
    print(extra_lists)

    while True:
        car_num_spec = input("If you interested in one specific car, please enter its car number:  Input here: ")
        time.sleep(1.5)
        if not int(car_num_spec) in data['car_num'].tolist():
            print("Please choose from existing car number! ")    
        else:
            break
    data_spec = data[data['car_num']== int(car_num_spec)]

    car_info_detail1(data_spec)
    time.sleep(2)
       
    print('If you want to have more infomation of all your chosen cars, here are the links: ')
    time.sleep(2)
    print(url_lists)    


def car_info_get(data):
    ''' create interactions with users

    Parameters
    ----------
    data: contains all sorts of cars' infomation 

    Returns
    -------
    interactive command lines: direct users to input commands
    
    '''
    df_copy = data.copy()
    print ('Welcome to Used Car Info System!') 
    time.sleep(1)

    print ('Please choose your price preference!')  
    time.sleep(1)   
    while True:
        price = input("Please choose from '0-20000', '20000-40000' or '40000-more'  Input here: ")
        if not str(price).lower() in ['0-20000','20000-40000','40000-more']:
            print("Please choose from '0-20000','20000-40000','40000-more'! ")    
        else:
            break
        
    if price == '0-20000':
        df_copy = df_copy[df_copy['price']<= 20000]
    elif price == 'medium price':
        df_copy = df_copy[(df_copy['price']<=40000)&(df_copy['price']>20000)]
    else:
        df_copy = df_copy[df_copy['price']>40000]

    print ('Good choice! You have ' + str(len(df_copy)) + ' choices left! ')  
    time.sleep(1)


    #transmission
    print ('Please choose your transmission preference!') 
    time.sleep(1) 
        
    while True:
        transmission = input("Please choose from 'manual', 'automatic' Input here: ")
        if not str(transmission).lower() in ['manual', 'automatic']:
            print("Please choose from 'manual', 'automatic' ! ")    
        else:
            break

    df_copy = df_copy[df_copy['transmission'] == transmission]    
    print ('Good choice! You have ' + str(len(df_copy)) + ' choices left! ')  
    time.sleep(1)


    #year
    print ('Please choose your year preference!') 
    time.sleep(1) 

    df_year = df_copy['year'].unique().tolist()

    if len(df_year)> 5:
        year_medium =  int(round(np.percentile(df_copy['year'], 50),0))# 2007< year <2019 medium
        while True:
            year_input = input("Please input your prefer year " + " 'before "+ str(year_medium) +"' or '" +  "after " + str(year_medium) + "'  Input your preference here: ")
            if not str(year_input).lower() in ["before "+ str(year_medium), "after "+ str(year_medium)] :
                print("Please choose from the given year range!")  
            else:
                break
        if 'before' in year_input:
            df_copy = df_copy[df_copy['year'] <= year_medium] 
        else:
            df_copy = df_copy[df_copy['year'] > year_medium] 


    else:
        year_lists = ''
        for i in df_year:
            year_lists = year_lists + i + ' '        
        while True:
            year_input = input("Please input your prefer year in " + year_lists + " Input your min year here: ")
            if not str(year_input).lower() in year_lists:
                print('Please choose from ' + year_lists) 
            else:
                break
        df_copy = df_copy[df_copy['year'] == year_input] 

    print ('Good choice! You still have ' + str(len(df_copy)) + ' choices left! ')  
    time.sleep(1)


    print ('Please choose your body type preference!') 
    #'convertible', 'other', 'coupe', 'pickup', 'sedan', 'suv', 'wagon'

    body_type_list = df_copy['body_type'].unique()
    body_type_lists = ''
    for i in body_type_list:
        body_type_lists = body_type_lists + i + ', '
        
    while True:
        body_type = input('Please choose from ' + body_type_lists + ' Input here: ')
        if not str(body_type).lower() in body_type_list:
            print('Please choose from ' + body_type_lists)    
        else:
            break

    df_copy = df_copy[df_copy['body_type']== body_type]
    #print ('You have ' + str(len(df_copy)) + ' choice left ')  

    if len(df_copy) == 1:
        car_info_detail1(df_copy)
    elif len(df_copy) <= 20:
        car_info_detail20(df_copy)
    else:
        df_copy = df_copy.sample(20)
        car_info_detail20(df_copy)

car_info_get(df)