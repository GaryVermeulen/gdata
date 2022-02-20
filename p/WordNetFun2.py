#
# More fun with WordNet
#
from nltk.corpus import wordnet as wn

synonyms = []
antonyms = []

inSentence = 'Mary walked Pookie in the park'

s = inSentence.split()

print(s)

for w in s:
    print('===========================')
    syns = wn.synsets(w)
    print(w)
    print(type(syns))
    print(len(syns))
    print(syns)

    print('---------------------------')

    if len(syns) > 0:
        print(syns[0].name())
        print(syns[0].lemmas()[0].name())
        print(wn.synset(str(syns[0].name())).lemma_names())

        print('---------------------------')

        for syn in wn.synsets(w):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        print(set(synonyms))
        print(set(antonyms))

        synonyms.clear()
        antonyms.clear()

        print('---------------------------')

        print('hyponyms:')
        print(wn.synset(str(syns[0].name())).hyponyms())

        print('hypernyms:')
        print(wn.synset(str(syns[0].name())).hypernyms())

        print('---------------------------')

        print('holonyms:')
        print(wn.synset(str(syns[0].name())).part_holonyms())

        print('meronyms:')
        print(wn.synset(str(syns[0].name())).part_meronyms())

        print('---------------------------')

        print('entailments:')
        print(wn.synset(str(syns[0].name())).entailments())

    else:
        print(str(w) + ' -- Not In WordNet')

    
