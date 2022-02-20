#
# Fun with WordNet
#
from nltk.corpus import wordnet as wn

synonyms = []
antonyms = []

inWord1 = 'walked'
inWord2 = 'park'
inSentence = 'Mary walked Pookie in the park'

print('Input Word 1: ' + str(inWord1))
print('Input Word 2: ' + str(inWord2))

syns1 = wn.synsets(inWord1)
syns2 = wn.synsets(inWord2)

print(type(syns1))
print(len(syns1))
print(syns1)

print('---------------------------')

if len(syns1) > 0:
    print(syns1[0].name())
    print(syns1[0].lemmas()[0].name())
    print(wn.synset(str(syns1[0].name())).lemma_names())

    print('---------------------------')

    for syn in wn.synsets(inWord1):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(set(synonyms))
    print(set(antonyms))
else:
    print(str(inputWord) + ' -- Not In WordNet')

print('---------------------------')    

w1 = wn.synset(str(syns1[0].name()))
w2 = wn.synset(str(syns2[0].name()))
print('similarity between w1 (' + str(w1) + ') and w2 (' + str(w2) + ')')
print(w1.wup_similarity(w2))

print('---------------------------')

print('w1 hyponyms:')
print(wn.synset(str(syns1[0].name())).hyponyms())

print('w1 hypernyms:')
print(wn.synset(str(syns1[0].name())).hypernyms())

print('---------------------------')

print('w2 hyponyms:')
print(wn.synset(str(syns2[0].name())).hyponyms())

print('w2 hypernyms:')
print(wn.synset(str(syns2[0].name())).hypernyms())

print('---------------------------')

print('w1 holonyms:')
print(wn.synset(str(syns1[0].name())).part_holonyms())

print('w1 meronyms:')
print(wn.synset(str(syns1[0].name())).part_meronyms())

print('w2 holonyms:')
print(wn.synset(str(syns2[0].name())).part_holonyms())

print('w2 meronyms:')
print(wn.synset(str(syns2[0].name())).part_meronyms())

print('---------------------------')

print('w1 entailments:')
print(wn.synset(str(syns1[0].name())).entailments())

print('w2 entailments:')
print(wn.synset(str(syns2[0].name())).entailments())

