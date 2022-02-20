# Wordnet testing
#

from nltk.corpus import wordnet as wn
import nltk
import pprint


#
def size1(s):
    return 1 + sum(size1(child) for child in s.hyponyms())

#
def size2(s):

    layer = [s]

    total = 0

    while layer:

        total += len(layer)

        layer = [h for c in layer for h in c.hyponyms()]

    return total

#
def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        trie['value'] = value

#
#
dog = wn.synset('dog.n.01')

print(str(size1(dog)))

print(str(size2(dog)))

#
trie = nltk.defaultdict(dict)
insert(trie, 'chat', 'cat')
insert(trie, 'chien', 'dog')
insert(trie, 'chair', 'flesh')
insert(trie, 'chic', 'stylish')
trie = dict(trie) # for nicer printing
print(str(trie['c']['h']['a']['t']['value']))
pprint.pprint(trie)

