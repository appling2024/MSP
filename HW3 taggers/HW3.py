import pandas as pd
import spacy
from pymorphy3 import MorphAnalyzer
from pymorphy3.tokenizers import simple_word_tokenize
morph = MorphAnalyzer()
nlp = spacy.load('ru_core_news_sm')

with open('/Users/juliak/PycharmProjects/MSP/HW3 taggers/brusov.txt', 'r', encoding='cp1251') as f_brusov:
    brusov_text = f_brusov.read()
with open ('/Users/juliak/PycharmProjects/MSP/HW3 taggers/rueval_2010_goldstandard_text.txt', 'r', encoding='cp1251') as f_goldstandard:
    goldstandard_text = f_goldstandard.read()
with open ('/Users/juliak/PycharmProjects/MSP/HW3 taggers/rueval_2010_rare75_text.txt', 'r', encoding='cp1251') as f_rare75:
    rare75_text = f_rare75.read()

# pymorphy3
brusov_pymorphy_text = simple_word_tokenize(brusov_text)
goldstandard_pymorphy_text = simple_word_tokenize(goldstandard_text)
rare75_pymorphy_text = simple_word_tokenize(rare75_text)
brusov_pymorphy = []
goldstandard_pymorphy = []
rare75_pymorphy = []

for token in brusov_pymorphy_text:
    parsed_token = morph.parse(token)[0]
    brusov_pymorphy.append((parsed_token.word, parsed_token.tag._str))
df = pd.DataFrame(brusov_pymorphy, columns=['token', 'tag'])
df.to_excel('/Users/juliak/PycharmProjects/MSP/HW3 taggers/brusov_pymorphy.xlsx', index=False)

for token in goldstandard_pymorphy_text:
    parsed_token = morph.parse(token)[0]
    goldstandard_pymorphy.append((parsed_token.word, parsed_token.tag._str))
df = pd.DataFrame(goldstandard_pymorphy, columns=['token', 'tag'])
df.to_excel('/Users/juliak/PycharmProjects/MSP/HW3 taggers/goldstandard_pymorphy.xlsx', index=False)

for token in rare75_pymorphy_text:
    parsed_token = morph.parse(token)[0]
    rare75_pymorphy.append((parsed_token.word, parsed_token.tag._str))
df = pd.DataFrame(rare75_pymorphy, columns=['token', 'tag'])
df.to_excel('/Users/juliak/PycharmProjects/MSP/HW3 taggers/rare75_pymorphy.xlsx', index=False)

# spacy
brusov_spacy_text = nlp(brusov_text)
goldstandard_spacy_text = nlp(goldstandard_text)
rare75_spacy_text = nlp(rare75_text)
brusov_spacy = []
goldstandard_spacy = []
rare75_spacy = []

for token in brusov_spacy_text:
    brusov_spacy.append((token.text, token.pos_, token.morph))
df = pd.DataFrame(brusov_spacy, columns=['token', 'pos', 'tag'])
df.to_excel('/Users/juliak/PycharmProjects/MSP/HW3 taggers/brusov_spacy.xlsx', index=False)

for token in goldstandard_spacy_text:
    goldstandard_spacy.append((token.text, token.pos_, token.morph))
df = pd.DataFrame(goldstandard_spacy, columns=['token', 'pos', 'tag'])
df.to_excel ('/Users/juliak/PycharmProjects/MSP/HW3 taggers/goldstandard_spacy.xlsx', index=False)

for token in rare75_spacy_text:
    rare75_spacy.append((token.text, token.pos_, token.morph))
df = pd.DataFrame(rare75_spacy, columns=['token', 'pos', 'tag'])
df.to_excel ('/Users/juliak/PycharmProjects/MSP/HW3 taggers/rare75_spacy.xlsx', index=False)

#  pymystem есть вункция снятия неоднозначности

# pymorphy3
# анализирует по слову, а не контекст, например синели - noun

# spacy
# точка не отдельный токен, Брюсов - имя собственное, прописаны категории (одушевленное)
