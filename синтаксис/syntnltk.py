# Программа использует морфологические данные разбора PyMorphy2 и синтаксические правила для автоматического синтаксического разобра текста на русском языки в NLTK.
# Python 3, NLTK, pymorphy2
# -*- coding: utf-8 -*- 
import nltk
from nltk import *
import pymorphy2 as pm
import codecs

## загружаем PyMorphy2
m = pm.MorphAnalyzer()
## открываем (создаем)файл с грамматикой, куда будут записываться правила
f = codecs.open(r"C:\Users\Андрей\AppData\Roaming\nltk_data\grammars\book_grammars\test.fcfg", mode= "w", encoding = "utf-8")
rules = codecs.open("rules.txt", mode= "r", encoding = "utf-8")
## записываем правила, которые вручную делаем (некоторые на основе правил из АОТ)
for rule in rules:
	f.writelines(rules)


rules.close()
f.close()

## функция, которая переводит нужную нам информацию из пайморфи в вид, читаемый парсером NLTK
## принимает (токенизированное) словосочетание на входе, записывает правила (lexical productions) в тот же файл с грамматикой

def pm2fcfg (phrase): ## phrase - это словосочетание, которое мы разбираем
    f = codecs.open(r"C:\Users\Андрей\AppData\Roaming\nltk_data\grammars\book_grammars\test.fcfg", mode= "a", encoding = "utf-8")
    for x in phrase:
        a = m.parse(x) ## a - список возможных вариантов морфологического разбора слова, предлагаемых пайморфи
		## от части речи зависит, какие признаки отправляются в грамматику, осюда условия
        for y in a:
            if (y.tag.POS == "NOUN") or (y.tag.POS == "ADJF") or (y.tag.POS == "PRTF"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=3" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADJS") or (y.tag.POS == "PRTS"):
                strk = str(y.tag.POS) + "[G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "NUMR"):
                strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "ADVB") or (y.tag.POS == "GRND") or (y.tag.POS == "COMP") or (y.tag.POS == "PRED") or (y.tag.POS == "PRCL") or (y.tag.POS == "INTJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "PREP") or (y.tag.POS == "CONJ"):
                strk = str(y.tag.POS) + "[NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
                break
            elif (y.tag.POS == "NPRO") & (y.normal_form != "это")& (y.normal_form != "нечего"):
                if ((y.tag.person[0] == "3") & (y.tag.number == "sing")):                    
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[C=" + str(y.tag.case) + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
            elif (y.tag.POS == "VERB")  or (y.tag.POS == "INFN"):
                if (y.tag.tense == "past"):                    
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + str(y.tag.gender) + ", NUM=" + str(y.tag.number) + ", PER=" + "0" + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                elif (y.tag.POS == "INFN"):
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=0, G=0, NUM=0, PER=0, NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                else:
                    strk = str(y.tag.POS) + "[TR=" + str(y.tag.transitivity) + ", TENSE=" + str(y.tag.tense) + ", G=" + "0" + ", NUM=" + str(y.tag.number) + ", PER=" + str(y.tag.person)[0] + ", NF=u'" + str(y.normal_form) + "'] -> '" + str(y.word) + "'\n"
                f.writelines(strk)
    f.close()
                
    
text = input("введите предложение для разбора: ") ## сюда пишется словосочетание для разбора
words = word_tokenize(text.lower()) ## разбиваем словосочетание на токены

pm2fcfg(words) ## запускаем функцию, описанную выше
cp = load_parser('grammars/book_grammars/test.fcfg') ## открываем нашу грамматику, смотрим на разбор в консоли или ещё где
for tree in cp.parse(words):
		print (tree)




