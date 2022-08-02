# -*- coding: utf-8 -*-
"""
Created on Fri May 28 17:13:06 2021

@author: Filipe Vieira
"""

import os
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

query_body = {
  "query": {
    "function_score": {
      "query": { "match_all": {} },
      "boost": "5",
      "random_score": {}, 
      "boost_mode": "multiply"
    }
  }
}

result = es.search(index="alertas", body=query_body, size=200)
es.close()
documents = result['hits']['hits']

cur_path = os.getcwd()
#%%
count = 0

for doc in documents:
    source = doc['_source']
    t = source['maintext']
    print(t)
    if source['maintext'] is None or source['title'] is None:
        print('None found - continue')
        continue
    text = source['title'] + '\n' + source['maintext']
    name = str(count).zfill(4)+'.txt'
    new_path = cur_path + '\\neg\\' + name
    print(count)
    with open(new_path, 'w', encoding='utf8') as f:
        f.write(text)
    print('- ' + source['title'])
    count += 1
#%%    
    
for i in range(100):
    if i % 2 == 0:
        continue
    print(i)