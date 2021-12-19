# -*- coding: utf-8 -*-
"""
@author: lsyliu

"""


import numpy as np
import pandas as pd
import bs4
from bs4 import BeautifulSoup
import lxml.html as lx
import requests
import re
import time


##Data Collection 

def extract_single_links(url):
    '''The input for this function is ebay website, and the output of this function 
    is all the posts's links in the one page'''
    response = requests.get(url)
    response.raise_for_status()
    html = lx.fromstring(response.text)
    html.make_links_absolute(url)

    links = html.xpath("//a[contains(@class,'s-item__link')]/@href")
    return list(set(links))


def extract_all_links(url):
    '''The input for this function is ebay website without page numbers, 
    and the output of this function is all the posts's links in the next 10 pages''' 
    i = 0
    links_all = []
    # a while loop that scrape all links
    while i < 10 :
        i = str(i)
        url = url+i
        link = extract_all_links(url)
        links_all = links_all + link
        links_all = list(set(links_all))
        i+=1
 
 
#Since the ebay's website does not allow scrape more than 1000 at a time, I decide to scrape different type of used cars     
#convertible
convertible_link = ' https://www.ebay.com/sch/i.html?_from=R40&_nkw=used+cars&_sacat=6001&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_ipg=200&rt=nc&Body%2520Type=Convertible&_oaa=1&_dcat=6236&_pgn='
convertible_links = extract_all_links(convertible_link)
#coupe
coupe_link = ' https://www.ebay.com/sch/i.html?_from=R40&_nkw=used+cars&_sacat=6001&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_ipg=200&rt=nc&Body%2520Type=Coupe&_oaa=1&_dcat=6236&_pgn='
coupe_links= extract_all_links(coupe_link)
#sedan
sedan_link = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=used+cars&_sacat=6001&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_ipg=200&rt=nc&Body%2520Type=Sedan&_oaa=1&_dcat=6236&_pgn='
sedan_links= extract_all_links(sedan_link)
#suv
suv_link = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=used+cars&_sacat=6001&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_ipg=200&rt=nc&Body%2520Type=SUV&_oaa=1&_dcat=6236&_pgn='
suv_links= extract_all_links(suv_link)
#wagon
wagon_link = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=used+cars&_sacat=6001&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_ipg=200&rt=nc&Body%2520Type=Wagon&_oaa=1&_dcat=6236&_pgn='
wagon_links= extract_all_links(wagon_link)
#pick_up
pickup_link = 'https://www.ebay.com/sch/i.html?_oaa=1&_dcat=6236&_fsrp=1&rt=nc&_from=R40&LH_TitleDesc=0&_ipg=200&_nkw=used+cars&_sacat=6001&LH_BIN=1&Body%2520Type=Crew%2520Cab%2520Pickup&_pgn='
pickup_links= extract_all_links(pickup_link)


#find info in one post
def get_car_info(url):
    '''Request information of a article from a ebay used_card website, 
    the input should be a used car link, and the output
    will be a dictionary of car information'''
    year=''
    body_type= ''
    mileage=''
    model=''
    inter_color=''
    p_option =''
    engine=''
    sale_by=''
    exter_color=''
    clean_title=''
    trim=''
    transmission =''
    options =''
    fuel =''
    make=''
    warranty =''
    horsepower=''
    # set a empty string
    
    link = url
    try:
    # set link to the url put in
        response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        htmls = lx.fromstring(response.text)
        htmls.make_links_absolute(url)
    except:
        pass
    
#Find name
    try: 
        title = htmls.xpath("//h1[contains(@class, 'it-ttl')]/text()")
        title = title[0]
    except:
        title = np.nan 
        
#Find Price
    try: 
        price = htmls.xpath("//span[@class = 'notranslate' and @id = 'prcIsum']/text()")
        price = price[0]    
    except:
        price = np.nan
        
#Find Location
    try: 
        location = htmls.xpath("//span[contains(@itemprop, 'availableAtOrFrom')]/text()")
        location = location[0]    
    except:
        location = np.nan   

#Find content
    try: 
        content = htmls.xpath("//div[preceding::div[contains(@class,'ux-labels-values__values-content')]]/span/text()")
        for i in range(len(content)):
            if 'Year:' in content[i]:
                year = content[i+1]
            else:
                continue        

        for i in range(len(content)):
            if 'Mileage:' in content[i]:
                mileage = content[i+1]
            else:
                continue

        for i in range(len(content)):
            if 'Body Type:' in content[i]:
                body_type = content[i+1]
            else:
                continue
        
        for i in range(len(content)):
            if 'Model:' in content[i]:
                model = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Interior Color:' in content[i]:
                inter_color = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Engine:' in content[i]:
                engine = content[i+1]
            else:
                continue

        for i in range(len(content)):
            if 'For Sale By:' in content[i]:
                sale_by = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Exterior Color:' in content[i]:
                exter_color = content[i+1]
            else:
                continue 
                
        for i in range(len(content)):
            if 'Vehicle Title:' in content[i]:
                clean_title = content[i+1]
            else:
                continue 
                
        for i in range(len(content)):
            if 'Trim:' in content[i]:
                trim = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Transmission:' in content[i]:
                transmission = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Options:' in content[i]:
                options = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Power Options:' in content[i]:
                p_option = content[i+1]
            else:
                continue 
                
        for i in range(len(content)):
            if 'Fuel Type:' in content[i]:
                fuel = content[i+1]
            else:
                continue 
                
        for i in range(len(content)):
            if 'Make:' in content[i]:
                make = content[i+1]
            else:
                continue
                
        for i in range(len(content)):
            if 'Warranty:' in content[i]:
                warranty = content[i+1]
            else:
                continue  
                
        for i in range(len(content)):
            if 'Horsepower Value:' in content[i]:
                horsepower = content[i+1]
            else:
                continue                
    except:
        content = np.nan
        
    total = {"url":link,"title":title,'location':location,'make':make, 'model':model,'trim':trim,'engine':engine,'price': price ,'year':year, 'mileage':mileage,'transmission':transmission,'options':options,'power options':p_option,'body_type':body_type, 'inter_color':inter_color,'exter_color':exter_color ,'fuel_type':fuel,'vehicle_title':clean_title,'for_sale_by':sale_by ,'warranty':warranty,'horse_power':horsepower}
    # create a dictionary and put in all the information found of the article
    print('o')
    return total

#apply to all links 
info1 = pd.DataFrame([get_car_info(x) for x in convertible_links])
info2 = pd.DataFrame([get_car_info(x) for x in coupe_links])
info3 = pd.DataFrame([get_car_info(x) for x in sedan_links])
info4 = pd.DataFrame([get_car_info(x) for x in suv_links])
info5 = pd.DataFrame([get_car_info(x) for x in wagon_links])
info6= pd.DataFrame([get_car_info(x) for x in pickup_links])

#combine them
info = pd.concat([info1,info2])
info = pd.concat([info,info3])   
info = pd.concat([info,info4])  
info = pd.concat([info,info5])  
info = pd.concat([info,info6]) 

len(info.drop_duplicates())
                                         
#save a copy
info.to_excel('info_all.xlsx', index=False)

