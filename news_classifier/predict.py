# -*- coding: utf-8 -*-
"""
Created on Mon May 31 17:42:32 2021

@author: Filipe Vieira
"""

from tensorflow import keras
import vectorize_data
import os
import pickle


path = 'C:\\Users\\Filipe Vieira\\Documents\\Projetos\\get_news_dataset\\validate'
validate = []
samples_processed = 0
for fname in sorted(os.listdir(path)):
    samples_processed += 1
    if fname.endswith('.txt'):
        with open(os.path.join(path, fname), encoding='utf8') as f:
            validate.append(f.read())

vectorizer = pickle.load(open('tfidf.pickle', 'rb'))
x_val = vectorizer.transform(validate).todense()
selector = pickle.load(open('selector.pickle', 'rb'))
x_val = selector.transform(x_val)
model = keras.models.load_model('news_classifier_mlp_model.h5')
pred = model.predict(x_val)
pred_label = []
pred_label = ['pos' if x > 0.5 else 'neg' for x in pred]
