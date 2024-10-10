# тексты
with open ('/Users/juliak/PycharmProjects/MSP/Language Identification/Maugham langid.txt', 'r', encoding='utf-8') as f_eng:
    english_text = ''.join(f_eng.readlines())
with open ('/Users/juliak/PycharmProjects/MSP/parse/Чехов.txt', 'r', encoding='utf-8') as f_ru:
    russian_text = ''.join(f_ru.readlines())
with open ('/Users/juliak/PycharmProjects/MSP/Language Identification/Remarque langid.txt', 'r', encoding='utf-8') as f_ge:
    german_text = ''.join(f_ge.readlines())


# определения языка langid
import langid
print ('\n\033[1mLanguage Identification by langid:\033[0m')
print('English text:', langid.classify(english_text))
print('Russian text:', langid.classify(russian_text))
print('German text:', langid.classify(german_text))

# определения языка langdetect
from langdetect import detect
print('\n\033[1mLanguage Identification by langdetect:\033[0m')
print('English text:', detect(english_text))
print('Russian text:', detect(russian_text))
print('German text:', detect(german_text))






