from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer, RegexpStemmer
porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = SnowballStemmer(language='german')
regexp = RegexpStemmer('e$|n$|er$|s$|st$|t$|en$|et$|est$|in$|erin$|', min=3)

words = ['Fische','Blumen','Kinder', 'Parks', 'höre', 'badest','arbeitet', 'reisen', 'gefahren', 'Lehrerin', 'Schüler']
print("{0:20}{1:20}{2:20}{3:30}{4:40}".format("Word","Porter Stemmer","Snowball Stemmer","Lancaster Stemmer",'Regexp Stemmer'))
for word in words:
    print("{0:20}{1:20}{2:20}{3:30}{4:40}".format(word,porter.stem(word),snowball.stem(word),lancaster.stem(word),regexp.stem(word)))




# e$|n$|er$|s$|- множественное число
# der Fisch -  die Fische
# die Blume - die Blumen
# das Kind - die Kinder
# der Park – die Parks

# спряжение глаголов в настоящем времени
# e$|st$|t$|en$|et$|est$|
# höre,  badest, arbeitet, reisen

#словообразование жр и мр
# in$|erin$|er$|
# Lehrerin, Schüler




