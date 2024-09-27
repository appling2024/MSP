from nltk.stem import RegexpStemmer
regexp = RegexpStemmer('e$|n$|er$|s$|st$|t$|en$|et$|est$|in$|erin$|', min=3)
words = ['Fische','Blumen','Kinder', 'Parks', 'höre', 'badest','arbeitet', 'reisen', 'gefahren', 'Lehrerin', 'Schüler']
for word in words:
    print(word,"--->",regexp.stem(word))



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




