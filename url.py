# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 00:56:43 2020

@author: gamma
"""
import requests
import datetime
import json
import time
def new_data(url):
    response = requests.get(url)
    output=response.json()
    file1=r'\Users\gamma\Documents\kja\mu-kgt\data_'+str(datetime.datetime.now())
    file=file1.replace('.','-').replace(':','-')
    with open('C:'+file+'.json', 'w', encoding='utf-8') as read_file:
        json.dump(output, read_file)
    
url='https://mu-kgt.ru/informing/wap/marsh/?action=getListCountTransport'
while 1!=0:
    print(datetime.datetime.now())
    new_data(url)
    time.sleep(3600)
    
