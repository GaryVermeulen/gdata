#
# simpGA.py
#
#   Grammar analysis of current corpus
#

#from nltk.tag import pos_tag
#from nltk.tokenize import word_tokenize

#from commonUtils import loadPickle
from commonConfig import verbose
from commonConfig import Sentence


def saidBefore(sA_Obj, taggedCorpus):

    wordsMatch = False
    tagsMatch = False

    inputWords = []
    inputTags = []
    wordsMatchCopy = []
    tagsMatchCopy = []
    
    for w in sA_Obj.inSent:
        inputWords.append(w[0])
        inputTags.append(w[1])

    # Has this been said before?
    for s in taggedCorpus:
        sWords = []
        sTags = []
        for w in s:
            sWords.append(w[0])
            sTags.append(w[1])
        
        if sWords == inputWords:
            wordsMatch = True
            wordsMatchCopy = sWords.copy()

        if sTags == inputTags:
            tagsMatch = True
            tagsMatchCopy = sTags.copy()

    return wordsMatch, wordsMatchCopy, tagsMatch, tagsMatchCopy


def getMacthedTagSent(sA_Obj, taggedCorpus):

    inputWords = []
    inputTags = []
    
    for w in sA_Obj.inSent:
        inputWords.append(w[0])
        inputTags.append(w[1])

    for s in taggedCorpus:
        sWords = []
        sTags = []
        for w in s:
            sWords.append(w[0])
            sTags.append(w[1])
        
        if sTags == inputTags:
            tagsMatch = True
            sCopy = s.copy()

    return sCopy


def chkGrammar(sA_Obj, taggedCorpus):

    
    print('------ start chkGrammar ------')


    if sA_Obj == None:
        return None

    if len(taggedCorpus) < 1:
        return None

    #print('sA_Obj.inSent:', sA_Obj.inSent)


    #print('inputWords: ', inputWords)
    #print('inputTags: ', inputTags)


    # Has this been said before?
    wordsMatchB, wordsMatchLst, tagsMatchB, tagsMatchLst = saidBefore(sA_Obj, taggedCorpus)

    if wordsMatchB and tagsMatchB:
        return 'This has been said before (word for word)' 

    if tagsMatchB:
        print('tagsMatch: ', tagsMatchLst)
        print('sA_Obj.inSent: ', sA_Obj.inSent)
        sCopy = getMacthedTagSent(sA_Obj, taggedCorpus)
        print('sCopy: ', sCopy)

        return sCopy
        

    print('------ end chkGrammar ------')
    return 'nope'


if __name__ == "__main__":
#    verbose = False

    # setup test input
    # taggedInput = [('i', 'NN'), ('am', 'VBP'), ('very', 'RB'), ('fine', 'JJ')] # Dummy test input
    taggedInput = [('see', 'VB'), ('hammy', 'NNP'), ('run', 'VB')]

    sType = 'declarative'
    sSubj = ('hammy', 'NNP')
    sVerb = [('see', 'VBP'),('run', 'VB')]
    sObj = ''
    sInObj = ''
    sAdj = ''
    sDet = ''
    sIN = ''
    sPP = ''
    sMD = ''
    sWDT = ''
    sCC = ''

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

    taggedCorpus = loadPickle('taggedCorpusSents')
    
    print(chkGrammar(sent, taggedCorpus))

        
