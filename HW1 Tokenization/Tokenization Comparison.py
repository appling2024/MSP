# %%
import nltk
nltk.download('punkt')

# %%
with open('Task1_tokens_nltk.txt', 'r', encoding='utf-8') as f:
  my_file = f.read()

#sentence = """Об орясину осёл топорище точит. А факир выгнав гостей выть акулой хочет."""
tokens = nltk.word_tokenize(my_file)
print(tokens)

with open('tokens_nltk.txt', 'w') as f2:
  print(len(tokens))
  for item in tokens:
    f2.write(item)
    f2.write('\n')

# %%
%pip install stanza

# %%
import stanza
stanza.download('ru')

# %%
with open('Task1_tokens_nltk.txt', 'r', encoding='utf-8') as f:
  my_file = f.read()

nlp = stanza.Pipeline(lang='ru', processors='tokenize', verbose = False) #verbose = False отмена отчета о работе программы
tokenised_text = nlp.process(my_file)



# %%
tokenised_text

# %%
tokenised_stanza = []
for token in nlp(my_file).iter_tokens():
    tokenised_stanza.append(token.text)

# %%
print(tokenised_stanza)
print(len(tokenised_stanza))

# %%
%pip install razdel
from razdel import tokenize

# %%
with open('Task1_tokens_nltk.txt', 'r') as f:
  my_file = f.read()

tokens = list(tokenize(my_file))
print(tokens)
print(len(tokens))

with open('tokens_razdel.txt','w') as f2:
  for item in tokens:
          f2.write(item.text)
          f2.write('\n')

# %%
%pip install spacy


# %%
import spacy

# %%
!python -m spacy download ru_core_news_sm

# %%

nlp = spacy.load('ru_core_news_sm')


# %%
doc = nlp(my_file)
with open('tokenized_spacy.txt', 'w', encoding='utf-8') as f:
    for token in doc:
      f.write(token.text)
      f.write('\n')


# %%
! pip install ufal.udpipe

# %%
! pip install pymorphy3

# %%
with open('Task1_tokens_nltk.txt', 'r', encoding='utf-8') as f:
  my_file = f.read()


# %%
from pymorphy3.tokenizers import simple_word_tokenize
tokenized_pymorphy3 = simple_word_tokenize(my_file)

# %%
with open('tokens_pymorphy.txt', 'w') as f2:
  for item in tokenized_pymorphy3:
    f2.write(item)
    f2.write('\n')

# %%
print(len(tokenized_pymorphy3))

# %%
! pip install segtok

# %%
from segtok.tokenizer import web_tokenizer
tokenized_segtok = web_tokenizer(my_file)
#print(tokenized_segtok)
#print(len(tokenized_segtok))


# %%
with open('tokens_segtok.txt', 'w') as f2:
  f2.write(str(len(tokenized_segtok)))
  for item in tokenized_segtok:
    f2.write(item)
    f2.write('\n')

# %%
! pip install segtok

# %%
with open('Task1_tokens_nltk.txt', 'r', encoding='utf-8') as f:
  my_file = f.read()

# %%
from segtok.tokenizer import web_tokenizer
tokenized_segtok = web_tokenizer(my_file)

# %%
with open('tokens_segtok.txt', 'w') as f2:
  f2.write(str(len(tokenized_segtok)))
  for item in tokenized_segtok:
    f2.write(item)
    f2.write('\n')

# %% [markdown]
# Comparison

# %%
lens = [len(tokenized_nltk), len(tokenized_razdel), len(tokenized_segtok), len(tokenized_spacy), len(tokenized_pymorphy3), len(tokenized_moses), len(tokenized_ud)]
lens


