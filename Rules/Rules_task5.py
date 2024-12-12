from nltk import *
import pymorphy3 as pm
import codecs
from nltk.parse import ViterbiParser
from nltk.grammar import ProbabilisticProduction, PCFG
from nltk import word_tokenize
from nltk.corpus import treebank
from nltk.parse import pchart

m = pm.MorphAnalyzer()
with codecs.open(r'/Users/juliak/PycharmProjects/MSP/Rules/test.fcfg', mode="w", encoding="utf-8") as f:
    with codecs.open(r'/Users/juliak/PycharmProjects/MSP/Rules/rules.txt', mode="r", encoding="utf-8") as rules:
        for rule in rules:
            f.write(rule)


def pm3fcfg (phrase):
    with codecs.open("/Users/juliak/PycharmProjects/MSP/Rules/test.fcfg", mode="a", encoding="utf-8") as f:
        for x in phrase:
            a = m.parse(x)
            if not a:
              print(f"Error: No parse found for {x}")
              continue
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

def test_ambiguity(text, max_trees=2):
    words = word_tokenize(text.lower())
    print(f"Токены: {words}")
    pm3fcfg(words)
    cp = load_parser('/Users/juliak/PycharmProjects/MSP/Rules/test.fcfg')
    trees = list(cp.parse(words))
    if len(trees) > 1:
        print(f"Обнаружены неоднозначности: {len(trees)} разборов")
        limited_trees = trees[:max_trees]
        for i, tree in enumerate(limited_trees):
            print(f"Разбор {i + 1} из {max_trees} (максимум):")
            print(tree)
    elif len(trees) == 1:
        print("Неоднозначности не обнаружены. Один разбор:")
        print(trees)
    else:
        print("Неоднозначности не обнаружены")
        for tree in trees:
            print(tree)

text = "Джон пошёл на стадион с собакой"
test_ambiguity(text)

grammar_with_penalty  = PCFG.fromstring("""
    S    -> NP VP                     [1.0]    
    VP   -> V                         [0.01]
    VP   -> V NP                      [0.01]
    VP   -> V PP                      [0.01]
    VP   -> V NP PP                   [0.01]
    VP   -> V PP PP                   [0.96]  
    NP   -> Name                      [0.49]
    NP   -> N                         [0.49]
    NP   -> Det N                     [0.01]
    NP   -> NP PP                     [0.01]
    PP   -> P NP                      [1.0] 
    V    -> 'пошёл'                   [1.0]
    N    -> 'стадион'                 [0.5]
    N    -> 'собакой'                 [0.5]
    Name -> 'Джон'                    [1.0]
    P    -> 'на'                      [0.5]
    P    -> 'с'                       [0.5]
""")

tokens = 'Джон пошёл на стадион с собакой'.split()

parser_with_penalty = pchart.InsideChartParser(grammar_with_penalty)
parser_with_penalty_2 = ViterbiParser(grammar_with_penalty)

print("Деревья с применением штрафов:")
for t in parser_with_penalty.parse(tokens):
    print(f"Дерево разбора с InsideChartParser. Вероятность: {t.prob():.4f}:")
    print(t)

for t in parser_with_penalty_2.parse(tokens):
    print(f"Дерево разбора с ViterbiParser. Вероятность: {t.prob():.4f}:")
    print(t)
