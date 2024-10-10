import pandas as pd
from pymorphy3 import MorphAnalyzer
from pymorphy3.tokenizers import simple_word_tokenize
import spacy
morph = MorphAnalyzer()
nlp = spacy.load('ru_core_news_sm')

# Функция для анализа текста с помощью pymorphy3
def analyze_with_pymorphy(text, filename):
    tokens = simple_word_tokenize(text)
    analyzed_tokens = [(morph.parse(token)[0].word, morph.parse(token)[0].tag._str) for token in tokens]
    df = pd.DataFrame(analyzed_tokens, columns=['token', 'tag'])
    df.to_excel(filename, index=False)

# Функция для анализа текста с помощью spaCy
def analyze_with_spacy(text, filename):
    doc = nlp(text)
    analyzed_tokens = [(token.text, token.pos_, token.morph) for token in doc]
    df = pd.DataFrame(analyzed_tokens, columns=['token', 'pos', 'tag'])
    df.to_excel(filename, index=False)

# Чтение файлов
file_paths = {
    "brusov": "/Users/juliak/PycharmProjects/MSP/HW3 taggers/brusov.txt",
    "goldstandard": "/Users/juliak/PycharmProjects/MSP/HW3 taggers/rueval_2010_goldstandard_text.txt",
    "rare75": "/Users/juliak/PycharmProjects/MSP/HW3 taggers/rueval_2010_rare75_text.txt"
}

texts = {}
for key, path in file_paths.items():
    with open(path, 'r', encoding='cp1251') as f:
        texts[key] = f.read()

# Анализ pymorphy3
for key, text in texts.items():
    analyze_with_pymorphy(text, f'/Users/juliak/PycharmProjects/MSP/HW3 taggers/{key}_pymorphy.xlsx')

# Анализ spaCy
for key, text in texts.items():
    analyze_with_spacy(text, f'/Users/juliak/PycharmProjects/MSP/HW3 taggers/{key}_spacy.xlsx')