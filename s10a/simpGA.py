#
# simpGA.py
#
#   Grammar analysis of current corpus
#

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from commonUtils import *
from simpConfig import verbose


def getCorpusTags():
    taggedCorpus = []
    extractedTags = []
    corpusTags = []
    cnt = 0

    corpus = loadPickle('newCorpus')

#    smallCorpus = corpus[1:20] # For testing puposes 
#
#    for s in smallCorpus:
#        tags = pos_tag(s)
#        taggedCorpus.append(tags)

    for s in corpus:
        tags = pos_tag(s)
        taggedCorpus.append(tags)
    
    copyTaggedCorpus = taggedCorpus.copy()

    if verbose:
        print('len taggedCorpus: ', len(taggedCorpus))
        print('----------------------')

    # Extract just the tags
    for s in taggedCorpus:
        taggedS = []
        for w in s:
            taggedS.append(w[1])
        if len(taggedS) > 0:
            extractedTags.append(taggedS)
    if verbose:
        print('len extractedTags: ', len(extractedTags))
        print('----------------------')

    # Remove dups
    for m in extractedTags: 
        if m not in corpusTags:
            corpusTags.append(m)

    if verbose:
        print('len corpusTags: ', len(corpusTags))
        print('----------------------')
        for n in corpusTags:
            cnt += 1        
            print('{} : {}'.format(cnt, n))

    return corpusTags

def chk4Grammar(inputSentence):


    print('------ start chk4Grammar ------')


    if len(inputSentence) < 1:
        inputSentence = [('i', 'NN'), ('am', 'VBP'), ('very', 'RB'), ('fine', 'JJ')] # Dummy test input
        
    corpusTags = getCorpusTags()

    print('-------')
    print('tagged?')
    print(inputSentence)
    
    # Extract just the tags
    tagTest = []
    for x in inputSentence:
        tagTest.append(x[1])
    print('-------')
    print(tagTest)
    print('-------')

    # Is the tag pattern of the test input within the corpus tags?
    for n in corpusTags:
        if tagTest == n:
            print('exact match')
            print('tagTest: ', tagTest)
            print('      n: ', n)
            return (True, tagTest)
        elif n[0] == 'PRP':
            print('PRP: ', n)

    print('------ end chk4Grammar ------')
    return (False, tagTest)


if __name__ == "__main__":

#    verbose = False


    print(chk4Grammar(''))

        
