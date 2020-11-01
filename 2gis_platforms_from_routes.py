# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 11:59:05 2020

@author: gamma
"""
from geojson import Point, Feature, FeatureCollection, dump
import json
from os import listdir
# import pandas as pd
from os.path import isfile, join

def platforms_parcing(inputlist, mypath, outputpath, city):
    platforms_list=[]
    features = []
    for file_name in inputlist:
        file = json.load(open(mypath+'\\'+file_name, encoding='utf-8'))
        item = file['result']['items'][0]
        for d in item['directions']:
            if d['type'] == 'loop':
                d['type'] = 'circular'
        item['directions'] = list(map(lambda x: x[1], list(filter(lambda x: x[1]['type'] != "additional" and not (x[1]['type'] == 'circular' and x[0] > 0), enumerate(item['directions'])))))
        item['directions'].sort(key=lambda x: 0 if x['type'] == 'circular' else 1 if x['type'] == 'forward' else 2, reverse=False)
        for i in range(len(item['directions'][0]['platforms'])):
            point=item['directions'][0]['platforms'][i]['geometry']['centroid']
            name=item['directions'][0]['platforms'][i]['name']
            if point not in platforms_list:
                platforms_list.append(point)
                str1=point[6:-1].split(' ')
                pointg=Point((float(str1[0]), float(str1[1])))
                features.append(Feature(geometry=pointg, properties={'platform_name':name}))
    feature_collection = FeatureCollection(features)
    with open(outputpath+'\\'+city+'_platforms.geojson', 'w') as f:
        dump(feature_collection, f)
    print(city+': success')



mypath=r'E:\0_density\Cheboksary\routes'
inputlist = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
outputpath=r'C:\Users\gamma\Documents\platforms_for_voronoi'
city='Cheboksary'
result=platforms_parcing(inputlist, mypath, outputpath, city)

mypath=r'E:\0_density\Chelyabinsk\routes'
inputlist = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
outputpath=r'C:\Users\gamma\Documents\platforms_for_voronoi'
city='Chelyabinsk'
result=platforms_parcing(inputlist, mypath, outputpath, city)

mypath=r'E:\0_density\Yu-S\routes'
inputlist = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
outputpath=r'C:\Users\gamma\Documents\platforms_for_voronoi'
city='Yuzhno-Sakhalinsk'
result=platforms_parcing(inputlist, mypath, outputpath, city)

mypath=r'C:\Users\gamma\Documents\yakutsk\routes'
inputlist = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
outputpath=r'C:\Users\gamma\Documents\platforms_for_voronoi'
city='Yakutsk'
result=platforms_parcing(inputlist, mypath, outputpath, city)