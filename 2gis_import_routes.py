import json
from os import listdir
from os.path import isfile, join
'''

Created on Fri Sep 25 23:51:32 2020

@author: gamma


Использование:
1. все то, что выгружено с 2гис - добавляем в папку, где кроме json ничего нет
2. изменяем path и output в конце кода
3. запускаем
4. в папке output появится результат. Что с ним можно сделать: 
    закинуть в qgis с помощью менеджера источника данных, выбрав там Delimited Text
    потом перевести в json
    
в txt в строку указано три столбца:
    1. WKT Geometry
    2. название файла (можно исправить, чтобы сразу менял на автобус/трам/троллейбус на кириллице)
    3. символ для отображения в ГИС по уникальным значениям (А - автобус, Ш - маршрутка, Тм - трамвай, Тб - троллейбус)
    
Код не идеален, т.к. делался на скорую руку =)

Буду рад, если подпишетесь на мою группу: vk.com/kaaaarta


'''

def lines_parcing(filelist, path, output):
    print('Start executing')
    parced_list=[]
    for file_name in filelist:
        file = json.load(open(path+file_name, encoding='utf-8'))
        item=file['result']['items'][0]
        #кольцевые приводим к одному виду
        for d in item['directions']:
            if d['type'] == 'loop':
                d['type'] = 'circular'
        #сортировка
        item['directions'] = list(map(lambda x: x[1], list(filter(lambda x: x[1]['type'] != "additional" and not (x[1]['type'] == 'circular' and x[0] > 0), enumerate(item['directions'])))))
        item['directions'].sort(key=lambda x: 0 if x['type'] == 'circular' else 1 if x['type'] == 'forward' else 2, reverse=False)
        #собственно, сама геометрия
        geometry = list(map(lambda x: x['geometry']['selection'],item['directions']))
        for i in geometry:
            #можно поменять либо вообще убрать эту проверку, кому как надо
            if 'trolley' in file_name:
                str1=i+'; '+file_name[:-5]+'; '+'Тб'
            elif 'tram' in file_name:
                str1=i+'; '+file_name[:-5]+'; '+'Тм'
            elif 'shuttle' in file_name:
                str1=i+'; '+file_name[:-5]+'; '+'Ш'
            else:
                str1=i+'; '+file_name[:-5]+'; '+'А'
            parced_list.append(str1)
    file=open(output, 'w')
    for row in parced_list:
        file.write(str(row) + '\n')
    file.close()
    print('Done')
    

path=r'/type/your/path'
output=r'type/your/path/andfile.txt'

inputlist = [f for f in listdir(path) if isfile(join(path, f))]

lines_parcing(inputlist, path, output)
