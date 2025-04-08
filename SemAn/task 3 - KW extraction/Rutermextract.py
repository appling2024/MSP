from rutermextract import TermExtractor

term_extractor = TermExtractor()

with open('ChizhikMelnikova_IMS_2022.txt', 'r', encoding='utf-8') as f:
    text = f.read()

for term in term_extractor(text):
    print(term.normalized, term.count)

with open('RuTermExtract_keywords.csv', 'w', encoding='windows-1251') as f2:
    for term in term_extractor(text):
        f2.write(str(term.normalized)+";"+str(term.count)+"\n")

with open('ChizhikMelnikova_IMS_2022_Abstract_rus.txt', 'r', encoding='utf-8') as f:
    text = f.read()

for term in term_extractor(text):
    print(term.normalized, term.count)

with open('RuTermExtract_keywords_abstract.csv', 'w', encoding='windows-1251') as f2:
    for term in term_extractor(text):
        f2.write(str(term.normalized)+";"+str(term.count)+"\n")
