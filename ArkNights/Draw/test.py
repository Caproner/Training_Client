# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 23:02:04 2019

@author: Administrator
"""

from urllib import  request
from bs4 import BeautifulSoup
import os
import json
import requests

w_filename = 'Agent.json'
Agents = dict()
Agents['agent'] = list()

url = 'http://wiki.joyme.com/arknights/%E5%B9%B2%E5%91%98%E6%95%B0%E6%8D%AE%E8%A1%A8'

wbdata = requests.get(url).text
soup = BeautifulSoup(wbdata,'lxml')
agent_list = soup.find(attrs={"id":"CardSelectTr"})
cnt = 0
gcnt = 0
for agent in agent_list:
    if cnt % 2 == 1 and cnt != 1:
        acnt = 0
        flag = False
        for i in agent:
            if acnt == 15:
                if i.string.find(u'寻访') != -1:
                    flag = True
                break
            acnt += 1
        if flag:
            acnt = 0
            gcnt += 1
            AgentData = dict()
            for i in agent:
                if acnt == 1:
                    AgentData['img'] = i.img['src'].strip()
                elif acnt == 3:
                    AgentData['name'] = i.a.string.strip()
                elif acnt == 7:
                    AgentData['class'] = i.string.strip()
                elif acnt == 9:
                    AgentData['rank'] = i.string.strip()
                acnt += 1
            Agents['agent'].append(AgentData)
    cnt += 1
print(gcnt)

with open(w_filename, 'w', encoding='utf-8') as f:
    f.write(json.dumps(Agents, ensure_ascii=False))

if not os.path.exists('img'):
    os.mkdir('img')
os.chdir('img')

for i in Agents['agent']:
    print(i['name'] + ' start!')
    request.urlretrieve(i['img'], i['name'] + '.png', None)
    print(i['name'] + ' done.')


                             
                            