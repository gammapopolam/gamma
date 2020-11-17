# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 00:19:15 2020

@author: gamma
"""
from os import listdir
import pandas as pd
from os.path import isfile, join
import json
import csv

def csv_proc(mypath): #processing csv
    file=mypath+r'\\density_groupby.csv'
    outputfile=mypath+r'\\density_out.csv'
    reader = csv.reader(open(file, newline='', encoding='utf-8'), delimiter=';')
    writer = csv.writer(open(outputfile, 'w'), delimiter=';')
    for row in reader:
        print(row)
        if '),  LINESTRING(' not in row[0]:
            name=row[1].split(',')
            count=len(name)
            row.insert(1, count)
            writer.writerow(row)
    
def process_2g(inputlist, ctr, ctr1, df): #regions
    for filename in inputlist:
        print(ctr1, filename)
        file = json.load(open(mypath+'\\'+filename, encoding='utf-8'))
        item = file['result']['items'][0]
        for d in item['directions']:
            if d['type'] == 'loop':
                d['type'] = 'circular'
        item['directions'] = list(map(lambda x: x[1], list(filter(lambda x: x[1]['type'] != "additional" and not (x[1]['type'] == 'circular' and x[0] > 0), enumerate(item['directions'])))))
        item['directions'].sort(key=lambda x: 0 if x['type'] == 'circular' else 1 if x['type'] == 'forward' else 2, reverse=False)
        geometry = list(map(lambda x: x['geometry']['selection'][11:-1],item['directions']))
        cords=str(geometry).split(',')
        for cord in range(len(cords)-1):
            cordss='LINESTRING('+str(cords[cord]).replace("['", '')+', '+str(cords[cord+1]).replace("']", "")+') '
            df.loc[ctr] = [cordss, filename[:-5]]
            ctr=ctr+1
        ctr1+=1
    return df

def process(inputlist, ctr, ctr1, df): #moscow
    for filename in inputlist:
        file=open(mypath+'\\renamed\\'+filename, 'r')
        print(ctr1, filename)
        data=file.read()
        str1=data[11:-1]
        cords=str1.split(',')
        for cord in range(len(cords)-1):
            cordss='LINESTRING('+str(cords[cord])+', '+str(cords[cord+1])+') '
            df.loc[ctr] = [cordss, filename[:-4]]
            ctr=ctr+1
        ctr1+=1
    return df


mypath=r'put/your/path'
inputlist = [f for f in listdir(mypath) if isfile(join(mypath, f)) and '.json' in f]
ctr=0
ctr1=1
df = pd.DataFrame(columns=['cords', 'name_of_transport'])
df2=process_2g(inputlist, ctr, ctr1, df)
df1=df2.groupby(by='cords', group_keys=False)['name_of_transport'].apply(lambda list: set(list))
print(df1)
path_or_buf=mypath+r'\\density_groupby.csv'
df1.to_csv(path_or_buf, sep=';')
csv_proc(mypath)
