#
# simpGA.py
#
#   Grammar analysis of current corpus
#

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from commonUtils import *

if __name__ == "__main__":

    taggedCorpus = []
    firstMatch = []
    noDups = []

    corpus = loadPickle('newCorpus')

#    smallCorpus = corpus[1:20] # For testing puposes 
#
#    for s in smallCorpus:
#        tags = pos_tag(s)
#        taggedCorpus.append(tags)

    for s in corpus:
        tags = pos_tag(s)
        taggedCorpus.append(tags)

    pos = 0
    copyTaggedCorpus = taggedCorpus.copy()

    print('len taggedCorpus: ', len(taggedCorpus))
    print('----------------------')

    for s in taggedCorpus:
#        print(s)
        taggedS = []
        for w in s:
            taggedS.append(w[1])
        if len(taggedS) > 0:
            firstMatch.append(taggedS)
    print('len firstMatch: ', len(firstMatch))
    print('----------------------')

    for m in firstMatch:
#        print(m)
        if m not in noDups:
            noDups.append(m)

    print('len noDups: ', len(noDups))
    print('----------------------')

#    for n in noDups:
#        print(n)

    testInput = 'i am very fine'
    testInputlist = testInput.split()

    taggedTestInput = pos_tag(testInputlist)

    print(taggedTestInput)

    tagTest = []
    for x in taggedTestInput:
        tagTest.append(x[1])
    print('-------')
    print(tagTest)
    print('-------')
    for n in noDups:
        if tagTest == n:
            print('exact match')
            print('tagTest: ', tagTest)
            print('      n: ', n)

        if n[0] == tagTest[0]:
            print(n)
