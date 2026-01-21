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

# Сравнение результатов разметки
# 1. Имена собственные
# Pymorphy3: Относит "Брюсов" к существительному, даже если это имя собственное.
# Spacy: Корректно маркирует имена собственные как PROPN (например, "Брюсов" и "В").
# 2. Предлоги и союзы
# Pymorphy3: Обозначает предлоги как PREP.
# Spacy: Обозначает предлоги как ADP.

# 3. Ошибки

# Spacy:
# 26. кормила - VERB, должно быть существительное (pymorphy3 и spaCy)
# 29. закатный  - VERB, должно быть прилагательное
# 32-34. странно-кос -  разбито на части: "странно" помечено как прилагательное, "-", как существительное, "кос" — как имя собственное, хотя это одно прилагательное
# 40. синели - NOUN, должен быть глагол (pymorphy3 и spaCy)
# 45. кроя - NOUN, должен быть глагол(pymorphy3 и spaCy)
# 64. строго-четки - разбито на части: - "строго" и "-" помечены как наречие, "четки" как существительное, хотя это одно прилагательное
# 67./167. миг - имя собственное, должно быть существительное
# 71. жал - VERB, должно быть существительное (pymorphy3 и spaCy)
# 84. весло - VERB, должно быть существительное
# 103. закат - имя собственное, должно быть существительное
# 110. Алея - имя собственное, должен быть герундий
# 127. уста - имя собственное, должно быть существительное
# 179. ничтожная - VERB, должно быть прилагательное
# 184. 12 - ADV, должно быть числительное
# 186. 1914 - ADV, должно быть числительное

# pymorphy3
# в.я. - предлоги и пунктуация, должны бфть имена собственные
# 24. кормила - VERB, должно быть существительное (pymorphy3 и spaCy)
# 34. синели - NOUN, должен быть глагол (pymorphy3 и spaCy)
# 36. вечеровой - NOUN, должно быть прилагательное
# 38. кроя - NOUN, должен быть глагол (pymorphy3 и spaCy)
# 52. строго-четки - NOUN, должно быть прилагательное
# 71. жал - VERB, должно быть существительное (pymorphy3 и spaCy)
# 99. правда - PRCL, должно быть существительное

# SpaCy лучше справляется с выделением имен собственных (но иногда отмечает существительные как имена собственные), в инициалах не выделяет точки как отдельные токены, но хуже справляется с разметкой
# Pymorphy3 лучше справляется с разметкой, не выделяет слова с дефисом как отдельные, но прохо справляется с выделением имен собственных