# Tagging check test
# chkTags.py
#

from commonUtils import loadPickle, savePickle
from commonUtils import chkTagging

def chkTagging(taggedInput, taggedBoW):

    tagging = []

    for w in taggedInput:
        tmpTag = []
        word = w[0]
        tag = w[1]
        tmpTag.append(word)
        tmpTag.append(tag)
        for t in taggedBoW:    
            if w[0] == t[0]:
                tmpTag.append(t[1])
                print('t and i match: ')
                print('w; ', w)
                print('t: ', t)
        tagging.append(tmpTag)
        
    print('---')
    for t in tagging:
        print('t: ')
        print(t)


    return 'tags match BoW or do not match BoW'


if __name__ == "__main__":

    tBoW = loadPickle('taggedBoW')
#    tI = [('i', 'PRP'), ('can', 'MD'), ('not', 'RB'), ('load', 'VB'), ('pickles', 'NNS')]
#    tI = [('dogs', 'NNS'), ('run', 'VBP'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('at', 'IN'), ('night', 'NN')]
#    tI = [('the', 'DT'), ('dog', 'NN'), ('ran', 'VBD'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN')]
    tI = [('hello', 'UH'), ('boat', 'NNP'), ('run', 'NNP'), ('hill', 'NNP'), ('count', 'NN')]

    results = chkTagging(tI, tBoW)
