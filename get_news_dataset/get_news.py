# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:39:02 2021

@author: Filipe Vieira
"""

from newsplease import NewsPlease
import os

file = open("pos-links.txt", "r", encoding="utf-8")   
contents = file.read()
links = contents.split('\n')
file.close()

# %%
import random

# cur_path = os.path.dirname(__file__)
cur_path = os.getcwd()
random.seed(42)
count_train = 0
count_test = 0

for link in links:
    try:
        article = NewsPlease.from_url(link)
        article_dict = article.get_dict()
            
        text = article_dict['title'] + '\n' + article_dict['maintext']
        
        if random.random() > .80:
            name = str(count_test).zfill(4)+'.txt'
            count_test += 1
            new_path = cur_path + '\\news\\test\\pos\\' + name
            folder = 'test: '
        else:
            name = str(count_train).zfill(4)+'.txt'
            count_train += 1
            new_path = cur_path + '\\news\\train\\pos\\' + name
            folder = 'train: '
            
        with open(new_path, 'w', encoding='utf8') as f:
             f.write(text)
             
        print('- ' + folder + article_dict['title'])
    except:
        pass
        

#%%

# Get news from Elasticsearch

import os
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

query_body = {
  "query": {
    "function_score": {
      "query": { "match_all": {} },
      "boost": "5",
      "random_score": {
          "seed": 42
          }, 
      "boost_mode": "multiply"
    }
  }
}

result = es.search(index="alertas", body=query_body, size=700)
es.close()
documents = result['hits']['hits']
#%%
import random
# Save news from Elasticsearch
cur_path = os.getcwd()

random.seed(42)
count_train = 0
count_test = 0

for doc in documents:
    source = doc['_source']
    # t = source['maintext']
    # print(t)
    if source['maintext'] is None or source['title'] is None:
        print('None found - continue')
        continue
    text = source['title'] + '\n' + source['maintext']
    
    if random.random() > .80:
        name = str(count_test).zfill(4)+'.txt'
        count_test += 1
        new_path = cur_path + '\\news\\test\\neg\\' + name
        folder = 'test: '
    else:
        name = str(count_train).zfill(4)+'.txt'
        count_train += 1
        new_path = cur_path + '\\news\\train\\neg\\' + name
        folder = 'train: '
    # name = str(count).zfill(4)+'.txt'
    # new_path = cur_path + '\\neg\\' + name
    # print(count)
    with open(new_path, 'w', encoding='utf8') as f:
        f.write(text)
    print('- ' + source['title'])
    # count += 1
    
file = open("neg-links.txt", "r", encoding="utf-8")   
contents = file.read()
links = contents.split('\n')
file.close()

cur_path = os.getcwd()
random.seed(42)

for link in links:
    try:
        article = NewsPlease.from_url(link)
        article_dict = article.get_dict()
            
        text = article_dict['title'] + '\n' + article_dict['maintext']
        
        if random.random() > .80:
            name = str(count_test).zfill(4)+'.txt'
            count_test += 1
            new_path = cur_path + '\\news\\test\\neg\\' + name
            folder = 'test: '
        else:
            name = str(count_train).zfill(4)+'.txt'
            count_train += 1
            new_path = cur_path + '\\news\\train\\neg\\' + name
            folder = 'train: '
            
        with open(new_path, 'w', encoding='utf8') as f:
             f.write(text)
             
        print('- ' + folder + article_dict['title'])
    except:
        pass

#%%

