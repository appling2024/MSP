import os
import sys
import codecs
import gensim
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import numpy as np
import warnings
warnings.filterwarnings('ignore')


model = Word2Vec(LineSentence(r'combined1.txt'),
                 vector_size=150,
                 window=1,
                 min_count=5,
                 workers=2)
model.init_sims(replace=True)#clearmemory
model.save('combined1.model')

m = Word2Vec.load('combined1.model')

for t in m.wv.most_similar(positive=[u'солнце'],
    topn=10):
    print (t[0], t[1])
print()

#косинусное сходство
print(model.wv.similarity("солнце", "небо"))

#евклидово расстояние
euclid1 = np.linalg.norm(model.wv['солнце'] - model.wv['небо'])
euclid2 = np.linalg.norm(model.wv['солнце'] - model.wv['облако'])
print(euclid1, euclid2)
