#
# processInput.py
#

import pickle
## import pyinflect # For use as an extension of Spacy
### from pyinflect import getAllInflections, getInflection # Standalone
from pyinflect import getAllInflections, getInflection
import simpConfig as sC

def getCorpus():

    with open('newCorpus.pkl', 'rb') as fp:
        corpus = pickle.load(fp)
        print('Aunt Bee loaded newCorpus.pkl')
    fp.close()

    return corpus


def getNewTaggedList():

    with open('newTaggedList.pkl', 'rb') as fp:
        newTaggedList = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()

    return newTaggedList


def isNNx(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] in ['NN', 'NNP', 'NNS']:
                return True

    return False


def isVBx(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                return True

    return False


def getVBx(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] == sC.vb:
                return sC.vb
            if t[1] == sC.vbd:
                return sC.vbd
            if t[1] == sC.vbg:
                return sC.vbg
            if t[1] == sC.vbn:
                return sC.vbn
            if t[1] == sC.vbp:
                return sC.vbp
            if t[1] == sC.vbz:
                return sC.vbz

    return sC.unk


def checkCorpus(uI):

    print('Processing checkCorpus...')

    uI_List = uI.split()
    print('uI: ', uI_List)

    wordSents = []
    xMatch = []
    sentsFound = []

    # Pull sentences from the corpus that match input senetence nouns
    for sent in corpus:
        for w in uI_List:
            t = []
            if w in sent:
                if isNNx(w):
                    t.append(w)
                    t.append(sent)
                    sentsFound.append(t)
                    #i = (getInflections(wTag[0][0], 'NN')) # Not yet
                
    print('len sentsFound: ', len(sentsFound))
    print('type sentsFound: ', type(sentsFound))
    
    # Of the above what are the verbs?
    sentsFound_wVBs = []
    for s in sentsFound:
        tmp = []
        verb = []
        verbFound = False
        for s1 in s[1]:            
            if isVBx(s1):
                v = getVBx(s1)
                verb.append(s1)
                verb.append(v)
                verbFound = True
            
        tmp.append(s[0])
        tmp.append(s[1])
        tmp.append(verb)
        
        sentsFound_wVBs.append(tmp)
        
    print('len sentsFound_wVBs: ', len(sentsFound_wVBs))
    print('type sentsFound_wVBs: ', type(sentsFound_wVBs))

    # Number of words from corpus sentence that match input sentence
    newSents = []
    for s in sentsFound_wVBs:
        newS = []
        cnt = 0
        for w in s[1]:
            counted = []
            for i in uI_List:
                if i == w and i not in counted:
                    cnt += 1
                    counted.append(i)

        s0 = s[0]
        s2 = s[1]
        s3 = s[2]
        newS.append(s0)
        newS.append(cnt)
        newS.append(s2)
        newS.append(s3)

        newSents.append(newS)
    
    print('len newSents: ', len(newSents))
    print('type newSents: ', type(newSents))

    for s in newSents:
        print(s)
    
    print('--' * 5)

    # Matching verbs input and corpus? W/O inflections.
    sentsWithMatchVerbs = []
    for s in newSents:
        for uI in uI_List:
            if uI in s[3]:
                sentsWithMatchVerbs.append(s)
    
    print('--' * 5)

    print('len sentsWithMatchVerbs: ', len(sentsWithMatchVerbs))
    print('type sentsWithMatchVerbs: ', type(sentsWithMatchVerbs))

    for vs in sentsWithMatchVerbs:
        print(vs)

    print('--' * 5)

    sentsInflectionVerbs = []
    # Matching verbs input and corpus? With inflections.
    for s in newSents:
        tmp = []
        i = (getInflections(s[3], 'V'))

        #if len(i) > 0:
        tmp.append(s[0])
        tmp.append(s[1])
        tmp.append(s[2])
        tmp.append(s[3])
        tmp.append(i)
        sentsInflectionVerbs.append(tmp)
        
    
    print('--' * 5)

    print('len sentsInflectionVerbs: ', len(sentsInflectionVerbs))
    print('type sentsInflectionVerbs: ', type(sentsInflectionVerbs))

    for vs in sentsInflectionVerbs:
        print(vs)
        

    """
    # Group by s[0]
    groups = {}
    for s in newSents:
        groups.setdefault(s[0], []).append(s)

    sortList = list(groups.values())

    for s in sortList:
        for si in s:
            print(si)
        
        print('-' * 5)
     """   
     
     
    

    return wordSents


def validInput(uI):

    uI_List = uI.split()
    valid_uI = []
    unknown_uI = []

    for word in newTaggedList:
#        print('word: ', word)
#        print()
        if word[0] in uI_List:
            if word[0] not in valid_uI:
                valid_uI.append(word[0])

    uI_Set = set(uI_List)
    valid_uI_Set = set(valid_uI)

    diff = uI_Set.difference(valid_uI)
    intr = uI_Set.intersection(valid_uI)
    
    
    return valid_uI, diff, intr


def getInflections(verbList, pos):
    # verbList => [word, tag, verb, tag,...]

    iList = []

    if pos == "V":
        odd = True 
        for v in verbList:
            if odd:
#                print('odd T word: ', v)
                word = v
                odd = False
            else:
#                print('even: ', v)
                odd = True
#                print('odd: {} even: {}'.format(word, v))

                i = getAllInflections(word, pos)

                if len(i) > 0:
                    iList.append(i)
                     
    elif pos == "N":
        print(" No NNs yet")
    else:
        print("Unknown inflection pos tag: ", pos)
    
    return iList



if __name__ == "__main__":

    print('Processing processInput...')

    corpus = getCorpus()
    newTaggedList = getNewTaggedList()

    print('len corpus: ', len(corpus))
    print('type corpus: ', type(corpus))
#    for s in corpus:
#        print(s)
    print('-' * 5)
    print('len newTaggedList: ', len(newTaggedList))
    print('type newTaggedList: ', type(newTaggedList))
#    for t in newTaggedList:
#        print(t)
    print('-' * 5)
    
    uI = input('Please enter a sentence: ')
    print(uI)

    print('-' * 5)

    valid_uI, diff, intr = validInput(uI)  # Is the input in out list?

    print('len valid_uI: ', len(valid_uI))
    print('type valid_uI: ', type(valid_uI))
    for v in valid_uI:
        print(v)

    print('diff: ', diff)
    print('intr: ', intr)
    print('-' * 5)

    
    
    xyz = checkCorpus(uI)

    print('-' * 5)
    print('len xyz: ', len(xyz))
    print('type xyz: ', type(xyz))
    for x in xyz:
        print('len x: ', len(x))
        print('type x: ', type(x))
        print(x[0])

    print(xyz)
    print('-' * 5)
    print(uI)
