#
# simpGA.py
#
#   Grammar analysis of current corpus
#

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from commonUtils import *
from simpConfig import verbose


def getCorpusTags(taggedCorpus):

    extractedTags = []
    corpusTags = []
    cnt = 0

    # Extract just the tags
    for s in taggedCorpus:
        taggedS = []
        for w in s:
            taggedS.append(w[1])
        if len(taggedS) > 0:
            extractedTags.append(taggedS)
#    if verbose:
#        print('len extractedTags: ', len(extractedTags))
#        print('----------------------')

    # Remove dups
    for m in extractedTags: 
        if m not in corpusTags:
            corpusTags.append(m)

#    if verbose:
#        print('len corpusTags: ', len(corpusTags))
#        print('----------------------')
#        for n in corpusTags:
#            cnt += 1        
#            print('{} : {}'.format(cnt, n))

    return corpusTags

def chk4Grammar(inputSentence, taggedCorpus):


    print('------ start chk4Grammar ------')


    if len(inputSentence) < 1:
        inputSentence = [('i', 'NN'), ('am', 'VBP'), ('very', 'RB'), ('fine', 'JJ')] # Dummy test input
        
    corpusTags = getCorpusTags(taggedCorpus)

    print('-------')
    print('tagged?')
    print(inputSentence)
    
    # Extract just the tags
    inputTags = []
    for x in inputSentence:
        inputTags.append(x[1])
    print('-------')
    print(inputTags)
    print('-------')

    # Is the tag pattern of the test input within the corpus tags?
    for taggedCorpusSent in corpusTags:
        if inputTags == taggedCorpusSent:
            print('exact match')
            print('inputTags       : ', inputTags)
            print('taggedCorpusSent: ', taggedCorpusSent)
            return (True, inputTags)            
            
#        elif taggedCorpusSent[0] == 'PRP':
#            print('PRP: ', taggedCorpusSent)

    print('------ end chk4Grammar ------')
    return (False, inputTags)


if __name__ == "__main__":

#    verbose = False


    print(chk4Grammar(''))

        
