#
# processInput.py
#

import pickle
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
#        print('t:::: ', t)
#        print(t[0], t[1])
        if w == t[0]:
            if t[1] in ['NN', 'NNP', 'NNS']:
#                print('found {} at {}'.format(w, t))
                return True

    return False


def isVBx(w):

    for t in newTaggedList:
#        print('t:::: ', t)
#        print(t[0], t[1])
        if w == t[0]:
            if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
#                print('found {} at {}'.format(w, t))
                return True

    return False


def getVBx(w):


    for t in newTaggedList:
#        print('---t: ', t)
#        print('---t: {} {}'.format(t[0], t[1]))
#        print('w: ', w)
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
            
#            print(w)
#            print(type(w))
#            print(sent)
            t = []
            if w in sent:
                if isNNx(w):
                    t.append(w)
                    t.append(sent)
                    sentsFound.append(t)

                
    print('len sentsFound: ', len(sentsFound))
    print('type sentsFound: ', type(sentsFound))

    sentsFound_wVBs = []
    # Of the above what are the verbs?
    for s in sentsFound:
#        print('s: ', s)
#        print('len s: ', len(s))
#        print('type s: ', type(s))
#        print('s[0]: ', s[0])
        tmp = []
        verb = []
        verbFound = False
        for s1 in s[1]:
#            print('s1: ', s1)
#            print('len s1: ', len(s1))
#            print('type s1: ', type(s1))
            
            if isVBx(s1):
#                print('found verb: {} in: {} '.format(s1, s[1]))
                v = getVBx(s1)
#                print(v)
                verb.append(s1)
                verb.append(v)
#                print(verb)
                verbFound = True
            
        
        tmp.append(s[0])
        tmp.append(s[1])
        tmp.append(verb)
        
            
        sentsFound_wVBs.append(tmp)
        

    print('len sentsFound_wVBs: ', len(sentsFound_wVBs))
    print('type sentsFound_wVBs: ', type(sentsFound_wVBs))


    # Words from corpus sentence that match input sentence
    newSents = []
    for s in sentsFound_wVBs:
        newS = []
#        print(s)
#        print(uI_List)
        cnt = 0
        for w in s[1]:
#            print(w)
            counted = []
            for i in uI_List:
                if i == w and i not in counted:
#                    print('match i: {} w: {}'.format(i, w))
                    cnt += 1
                    counted.append(i)
#                    print('cnt: ', cnt)
            #cnt = 0
#        print('w cnt: ', cnt)
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

    sentsWithMatchVerbs = []
    # Matching verbs?
    for s in newSents:
#        print('s: ', s)
        for uI in uI_List:
#            print('s[3]: ', s[3])
#            print('uI: ', uI)
            if uI in s[3]:
#                print('verb match {} in {}'.format(uI, v))
                sentsWithMatchVerbs.append(s)
        
    
    print('--' * 5)

    print('len sentsWithMatchVerbs: ', len(sentsWithMatchVerbs))
    print('type sentsWithMatchVerbs: ', type(sentsWithMatchVerbs))

    for vs in sentsWithMatchVerbs:
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
     
     
    

    """
    for w in uI_List:
        print('w: ', w)
        tmp_wordSent = []
#        tmp_wordSent.append(w)
        for sent in corpus:
            if w in sent and isNNx(w): # Only capture nouns
                tSent = []
                print('found w: {} at: {} and isNNx {}'.format(w, sent, isNNx(w)))
                tSent.append(w)
                tSent.append(sent)
                tmp_wordSent.append(tSent)
                wordSents.append(tmp_wordSent)
        
#    print('len corpus: ', len(corpus))
    print('len wordSents: ', len(wordSents))

    for s in wordSents:
        print(s)

    """

    """

    for s in wordSents: # works when uI is shorter then s
        s_str = ' '.join(s)
        print(s_str)
        res = s_str.find(uI)
        if res > -1:
            xMatch.append(s_str)
    print('xMatch: ', xMatch)

    if len(xMatch) == 0:
        for s in wordSents:
            sSet = set(s)
            uISet = set(uI_List)
            print('sSet: ', sSet)
            print('uISet: ', uISet)
            intersection = sSet.intersection(uISet)
            if len(intersection) > 0:
                xMatch.append(' '.join(s))
            
            
    print('intersection: ', intersection)
        

    if len(xMatch) > 0:

        windowStart = 0
        windowStop = len(uI_List)
        windowStep = 1
        windowCount = 0
        windowSize = len(uI_List)

        print('len uI_List: ', len(uI_List))
        print(uI_List)
        print('len xMatch: ', len(xMatch))
        print(xMatch)
        print('-' * 5)
                                        # Input sentence is longer than matched sentence
        if len(uI_List) <= len(xMatch): # All words in uI_List are in xMatch
            tmpList = xMatch[0].split()
        
            window = tmpList[windowStart:windowStop:windowStep]

            print('tmpList: ', tmpList)
            print('window: ', window)

        
            if len(uI_List) == len(window) and len(uI_List) == sum([1 for i, j in zip(uI_List, window) if i == j]):
                print("The lists are identical")
                print(uI_List)
                print('=')
                print(window)
            else:
                # Move window and try again
                print('moving on...')
                windowStart += 1
                windowStop += 1
                windowCount += 1
                searchedLen = windowCount + windowSize
            
                while searchedLen <= len(tmpList):
                    window = tmpList[windowStart:windowStop:windowStep]
                    if len(uI_List) == len(window) and len(uI_List) == sum([1 for i, j in zip(uI_List, window) if i == j]):
                        print("The lists are identical")
                        print(uI_List)
                        print('=')
                        print(window)
                        break
                    else:
                        print("The lists are not identical")
                        print(uI_List)
                        print('!=')
                        print(window)
                        print('moving on again...')
                        windowStart += 1
                        windowStop += 1
                        windowCount += 1
                        searchedLen = windowCount + windowSize
                        
        elif len(uI_List) >= len(xMatch):   # Input sentence is longer than matched sentence
            print('input sentence longer then xMatch[0]')
            print(uI_list)
            print(xMatch[0])

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
