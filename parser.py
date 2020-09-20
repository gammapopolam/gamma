import json
from os import listdir
from os.path import isfile, join
mypath=r'D:\0_density\Cheboksary'

inputlist = [f for f in listdir(mypath+'\\routes') if isfile(join(mypath+'\\routes', f))]
# использовано из nktb40/mostransport_etl
parced_list=[]
def parcing(inputlist):
    for file_name in inputlist:
        file = json.load(open(mypath+'\\routes\\'+file_name, encoding='utf-8'))
    #    print(file['result']['items'][0]['directions'][0]['platforms'][0].keys())
    #    print(file['result']['items'][0]['directions'][0]['platforms'][1])
        item = file['result']['items'][0]
        #Загружаем данные по маршруту
        #Приводим кольцевые маршруты к одному формату
        for d in item['directions']:
            if d['type'] == 'loop':
                d['type'] = 'circular'
        #фильтруем направления, чтобы исключить дополнительные маршруты
        item['directions'] = list(map(lambda x: x[1], list(filter(lambda x: x[1]['type'] != "additional" and not (x[1]['type'] == 'circular' and x[0] > 0), enumerate(item['directions'])))))
        #Сортируем направления, чтобы сначала было прямое, затем обратное
        item['directions'].sort(key=lambda x: 0 if x['type'] == 'circular' else 1 if x['type'] == 'forward' else 2, reverse=False)
        #Выгружаем геометрию маршрута
        geometry = list(map(lambda x: x['geometry']['selection'],item['directions']))
        for i in geometry:
            str1=i.split(',')
            parced_list.append(str1[11:-1])
    output_wkt=[]
    file_name=''
    for a in parced_list:
        for ab in range(len(a)-1):
            counter=0
            name=''
            for c in parced_list:
                for cd in range(len(c)-1):
                    if a[ab]==c[cd] and a[ab+1]==c[cd+1]:
                        geomcheck='LineString ('+a[ab]+','+a[ab+1]+')'
                        if geomcheck not in output_wkt:
                            for file_name in inputlist:
#                            print(file_name)
                                file=json.load(open(mypath+'\\routes\\'+file_name, encoding='utf-8'))
                                item = file['result']['items'][0]
                                #Загружаем данные по маршруту
                                #Приводим кольцевые маршруты к одному формату
                                for d in item['directions']:
                                    if d['type'] == 'loop':
                                        d['type'] = 'circular'
                                        #фильтруем направления, чтобы исключить дополнительные маршруты
                                item['directions'] = list(map(lambda x: x[1], list(filter(lambda x: x[1]['type'] != "additional" and not (x[1]['type'] == 'circular' and x[0] > 0), enumerate(item['directions'])))))
                                        #Сортируем направления, чтобы сначала было прямое, затем обратное
                                item['directions'].sort(key=lambda x: 0 if x['type'] == 'circular' else 1 if x['type'] == 'forward' else 2, reverse=False)
                                #Выгружаем геометрию маршрута
                                geometry = list(map(lambda x: x['geometry']['selection'],item['directions']))
                                if a[ab] in str(geometry) and a[ab+1] in str(geometry):
                                    if file_name[:-5] not in name:
                                        name=name+' '+file_name[:-5]
                                        counter=counter+1
            string1='LineString ('+a[ab]+','+a[ab+1]+'); '+str(counter)+'; '+name
            output_wkt.append(string1)
            print(string1)
    return output_wkt
output_wkt=parcing(inputlist)
file=open(mypath+'.txt', 'w')
for row in output_wkt:
    file.write(str(row) + '\n')
file.close()
