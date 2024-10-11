import warnings
warnings.filterwarnings('ignore')
import logging
logging.getLogger('stanza').setLevel(logging.WARNING)
from itertools import zip_longest
import pandas as pd

#считывание текста из файла
with open ('parse/Чехов.txt', 'r', encoding='utf-8-sig') as f:
    text_one=f.read()

#nltk
# и т.п. [т.], [п.] (но точки в конце предложения - отдельны
# й токен), слова через дефис - один токен
from nltk import word_tokenize
array_nltk=word_tokenize(text_one)
#print('nltk:', 'количество токенов:', len(array_nltk),array_nltk)
with open ('Output/nltk.txt', 'w') as f_nltk:
    for item in array_nltk:
        f_nltk.write(item)
        f_nltk.write('\n')

#razdel
# знаки препинания - отдельный токен, слова через дефис - один токен
from razdel import tokenize
tokens=list(tokenize(text_one))
array_razdel = [token.text for token in tokens]
#print('razdel:', 'количество токенов:', len(array_razdel),array_razdel)
with open ('Output/razdel.txt', 'w') as f_razdel:
    for item in array_razdel:
        f_razdel.write(item)
        f_razdel.write('\n')

#segtok
# слово с точкой в конце предложения, слово с дефисом, знак препинания + » - один токен
from segtok.tokenizer import word_tokenizer
array_segtok=word_tokenizer(text_one)
#print('segtok:', 'количество токенов:', len(array_segtok),array_segtok)
with open ('Output/segtok.txt', 'w') as f_segtok:
    for item in array_segtok:
        f_segtok.write(item)
        f_segtok.write('\n')

#pymorphy3
# знаки препинания - отдельный токен, слова через дефис - один токен
from pymorphy3 import tokenizers
array_pymorphy = tokenizers.simple_word_tokenize(text_one)
#print('pymorphy:', 'количество токенов:', len(array_pymorphy),array_pymorphy)
with open ('Output/pymorphy.txt', 'w') as f_pymorphy:
    for item in array_pymorphy:
        f_pymorphy.write(item)
        f_pymorphy.write('\n')

#spacy
# \n, знаки препинания - один токен, слова через дефис - отдельные токены
from spacy.lang.ru import Russian
nlp_spacy=Russian()
doc_spacy=nlp_spacy(text_one)
array_spacy = [token.text for token in doc_spacy]
#print('spacy:', 'количество токенов:', len(array_spacy),array_spacy)
with open ('Output/spacy.txt', 'w') as f_spacy:
    for item in array_spacy:
        f_spacy.write(item)
        f_spacy.write('\n')

#stanza
# -помалу ? - остальные слова через дефис, знаки препинания - один токен
import stanza
nlp_stanza = stanza.Pipeline(lang='ru', processors='tokenize')
doc_stanza = nlp_stanza(text_one)
array_stanza = [word.text for sentence in doc_stanza.sentences for word in sentence.words]
#print('stanza:', 'количество токенов:', len(array_stanza),array_stanza)
with open ('Output/stanza.txt', 'w') as f_stanza:
    for item in array_stanza:
        f_stanza.write(item)
        f_stanza.write('\n')

#mosestokenizer
# @-@ - токен дефис, « - отдельный токен, слова через дефис - отдельные токены
from mosestokenizer import MosesTokenizer
tokenize=MosesTokenizer('ru')
array_mosestokenizer = []
try:
    with open('parse/Чехов.txt', 'r', encoding='utf-8-sig') as f:
        for line in f:
            tokens = list(tokenize(line))
            array_mosestokenizer.extend(tokens)
except Exception as e:
    print(f"Произошла ошибка при токенизации: {e}")

#print('mosestokenizer:', 'количество токенов:', len(array_mosestokenizer),array_mosestokenizer)
with open ('Output/mosestokenizer.txt', 'w') as f_mosestokenizer:
    for item in array_mosestokenizer:
        f_mosestokenizer.write(item)
        f_mosestokenizer.write('\n')

#ufal.udpipe
# слово/знак препинания + » - один токен, слова через дефис и знаки препинания - один токен
import ufal
from ufal import udpipe
model_path = 'parse/russian-syntagrus-ud-2.0-170801.udpipe'
models = ufal.udpipe.Model.load(model_path)
pipeline = ufal.udpipe.Pipeline(
    models,
    'tokenize',
    ufal.udpipe.Pipeline.DEFAULT,
    ufal.udpipe.Pipeline.DEFAULT,
    ufal.udpipe.Pipeline.DEFAULT
)
processed_text = pipeline.process(text_one)
array_ufal = []
try:
    for line in processed_text.split('\n'):
        parts = line.split('\t')
        if len(parts) > 1:  # Проверка наличия хотя бы двух частей
            array_ufal.append(parts[1])
finally:
    #print('ufal.udpipe:', 'количество токенов:', len(array_ufal),array_ufal)
    with open ('Output/ufal.txt', 'w') as f_ufal:
        for item in array_ufal:
            f_ufal.write(item)
            f_ufal.write('\n')

def diff_func(array_one,array_two,name_one,name_two):
    set1 = set(array_one)
    set2 = set(array_two)

# Найти элементы, которые есть в array1, но нет в array2
    diff1 = set1 - set2
    print("\n\033[1mСравниваем",name_one,' c ',name_two,':\033[0m')
    print(f'Элементы в ',name_one,', но не в ',name_two,':',diff1)
    diff2 = set2 - set1
    print(f'Элементы в ',name_two,', но не в ',name_one,':',diff2)
    # diff3 ={item for item in diff2 if not (any(char.isalpha() for char in item) and '.' in item)}
    # print('\nДоп контент в котором мы убираем слова которые идут с точкой как один токен:')
    # print(f'Сравнение в котором убираем слова  в которых точка не отдельная из',name_two,': ',diff3)
    # diff4 ={item for item in diff1 if not (any(char.isalpha() for char in item) and '.' in item)}
    # print(f'Сравнение в котором убираем слова  в которых точка не отдельная из',name_one,':',diff4)

#Запуск функций проверки
diff_func(array_nltk,array_razdel,'nltk','razdel')
diff_func(array_segtok,array_pymorphy,'segtok','pymorphy')
diff_func(array_stanza,array_spacy,'stanza','spacy')
diff_func(array_mosestokenizer,array_ufal,'mosestokenizer','ufal.udpipe')

data = {
    'nltk': [f'{len(array_nltk)} токенов'],
    'razdel': [f'{len(array_razdel)} токенов'],
    'segtok': [f'{len(array_segtok)} токенов'],
    'pymorphy': [f'{len(array_pymorphy)} токенов'],
    'spacy': [f'{len(array_spacy)} токенов'],
    'stanza': [f'{len(array_stanza)} токенов'],
    'mosestokenizer': [f'{len(array_mosestokenizer)} токенов'],
    'ufal.udpipe': [f'{len(array_ufal)} токенов']
}


df_count_token = pd.DataFrame(data)
print("\n\033[1mТаблица количества токенов:\033[0m")
print(df_count_token.to_string())

data = list(zip_longest(array_nltk, array_razdel, array_segtok, array_pymorphy, array_spacy, array_stanza, array_mosestokenizer, array_ufal, fillvalue='-'))
df_token = pd.DataFrame(data, columns=['nltk', 'razdel', 'segtok', 'pymorphy', 'spacy', 'stanza', 'mosestokenizer', 'ufal.udpipe'])
print("\n\033[1mТаблица Токенизации:\033[0m")
print(df_token.to_string())


#print("\n\033[1mТаблица Токенизации:\033[0m")
#print('{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}'.format(
#    'nltk', 'razdel', 'segtok', 'pymorphy', 'spacy', 'stanza', 'mosestokenizer', 'ufal.udpipe'))
#print('{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}'.format(*values))
#for tk in zip_longest(array_nltk, array_razdel, array_segtok, array_pymorphy, array_spacy, array_stanza, array_mosestokenizer, array_ufal, fillvalue='-'):
#   print ('{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}\t{:20}'.format (*tk))