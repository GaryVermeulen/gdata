#
# processInput.py
#

import pickle
## import pyinflect # For use as an extension of Spacy
### from pyinflect import getAllInflections, getInflection # Standalone
#from pyinflect import getAllInflections, getInflection
#import simpConfig as sC
from simpConfig import *
from processKB import *

def getCorpus():

    with open('pickles/newCorpus.pkl', 'rb') as fp:
        corpus = pickle.load(fp)
        print('Aunt Bee loaded newCorpus.pkl')
    fp.close()

    return corpus


def getNewTaggedList():

    with open('pickles/newTaggedList.pkl', 'rb') as fp:
        newTaggedList = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()

    return newTaggedList


def getInflectionsPickle():
    
    with open('pickles/inflections.pkl', 'rb') as fp:
        inflects = pickle.load(fp)
        print('Aunt Bee loaded inflections.pkl')
    fp.close()

    return inflects


def getKB():

    with open('pickles/newKB_Tree.pkl', 'rb') as fp:
        t = pickle.load(fp)
        print('Aunt Bee loaded newKB_Tree.pkl')
    fp.close()

    return t


def getWordTag(word):

    for t in newTaggedList:
        if word == t[0]:
            return t[1]

    return None


def isNNx(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] in ['NN', 'NNP', 'NNS']:
                return True

    return False


def isVBx(w):

    for t in newTaggedList:
        if w == t[0]:
#            if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
#            if t[1] in [sC.vb, sC.vbd, sC.vbg, sC.vbn, sC.vbp, sC.vbz]:
            if t[1] in [vb, vbd, vbg, vbn, vbp, vbz]:
                return True

    return False


def getVBxTag(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] == vb:
                return vb
            if t[1] == vbd:
                return vbd
            if t[1] == vbg:
                return vbg
            if t[1] == vbn:
                return vbn
            if t[1] == vbp:
                return vbp
            if t[1] == vbz:
                return vbz

    return unk


def getInflectionTag(vTag):

    if vTag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'

    return 'x'


def checkCorpus(uI):

    baseWordSearch = True

    print('Processing checkCorpus...')

    uI_List = uI.split()
    print('uI_List: ', uI_List)

    sentsFound = []
    allVerbs = []

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
                
    print('len (NNx) sentsFound: ', len(sentsFound))
    print('type (NNx) sentsFound: ', type(sentsFound))





    # Pull sentences from the corpus that match input senetence verbs
    for sent in corpus:
        for w in uI_List:
            t = []
            if w in sent:
                if isVBx(w):
                    t.append(w)
                    t.append(sent)
                    allVerbs.append(t)
                    #i = (getInflections(wTag[0][0], 'NN')) # Not yet
                
    print('len (VBx) allVerbs: ', len(allVerbs))
    print('type (VBx) allVerbs: ', type(allVerbs))
    
    
    # Of the above noun matching sentences what are the verbs?
    sentsFound_wVBs = []
    for s in sentsFound:
        tmp = []
        verb = []
        verbFound = False
        for s1 in s[1]:            
            if isVBx(s1):
                vTag = getVBxTag(s1)
                verb.append(s1)
                verb.append(vTag)
                iTag = getInflectionTag(vTag)
                i = []
                if iTag != 'x': # Trying to solve the see/saw/saw problem
                    if len(s[1]) > 2:
                        beforeWordTag = getWordTag(s[1][0])
                        afterWordTag = getWordTag(s[1][2])
                        if (beforeWordTag in [nn, nnp, nns, prp]) and (afterWordTag in [nn, nnp, nns, prp]):
                            baseWordSearch = False
                        else:
                            baseWordSearch = True
                    else:
                        print('else len(s[1]) > 2: ', len(s[1]))

                    i = getInflections(s1, iTag, baseWordSearch)
                else:
                    print('unknown inflection tag: ', iTag)
                verb.append(i)
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
        s2 = s[1] # Re-orders list entries
        s3 = s[2]
        newS.append(s0)
        newS.append(cnt)
        newS.append(s2)
        newS.append(s3)

        newSents.append(newS)
    
    print('len newSents (NNx, VBx, and cnt): ', len(newSents))
    print('type newSents (NNx, VBx, and cnt): ', type(newSents))

    for s in newSents:
        print(s)
    
    print('--' * 5)
    print('Do any of the verbs in the senetences found match the input sentence?')
    # Do any of the verbs in the senetences found match the input sentence?
    verbsMatch = []
    for w_uI in uI_List:
        if isVBx(w_uI):
#            print('w_uI: ', w_uI)
            for nS in newSents:
#                print('nS: ', nS)
                # direct match (non-inflection)
                tmp = []
                if w_uI in nS[2]:
#                    print('direct verb match w_uI {} found in nS[2] {}'.format(w_uI, nS[2]))
                    tmp.append(w_uI)
                    tmp.append(nS)
                    verbsMatch.append(tmp)
                else:
                    for v in nS[3]:
#                        print('v: ', v)                       
                        if isinstance(v, str):
#                            print('string found: ', v)
#                            print('w_uI: ', w_uI)
                            if w_uI == v:
#                                print('baseword match v {} and w_uI {}'.format(v, w_uI))
                                tmp.append(w_uI)
                                tmp.append(nS)
                                verbsMatch.append(tmp)
                        elif isinstance(v, list):
                            if w_uI in v:
#                                print('non-baseword match v {}'.format(v))
                                tmp.append(w_uI)
                                tmp.append(nS)
                                verbsMatch.append(tmp)
                        else:
                            print('unknown type found')
                
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))

    for v in verbsMatch:
        print(v)
            

    
    return newSents, verbsMatch, allVerbs


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


def getInflections(word, tag, baseWordSearch):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag)) 
    for line in allInflections:
        if word in line:
#            print('found {} at {} {}'.format(word, cnt, line))
            if line[1] == tag:
#                print('found v {} with tag {} at {} {}'.format(word, tag, cnt, line))
                if baseWordSearch:
#                    print('base word match {} at {} {}'.format(word, cnt, line))
                    return line
                else: # Search inflections only
                    idx = 0
                    for i in line:
                        if idx > 1:
                            if i == word:
#                                print('i: ', i)
#                                print('idx: ', idx)
#                                print('Non-base word match {} at {} {}'.format(word, cnt, line))
                                return line
                        idx += 1
#        cnt += 1

    return []


def checkKB(nounsMatch, tagged_uI):

    kb_Nouns = []
    kb_uI = []

    # sloppy...
    # List of matched corpus nouns
    for s in nounsMatch:
        tmp = []
        if t.isNode(s[0]):
#            print('found node s[0]: ', s[0])
            cDo = t.get_canDo(t.root, s[0])
            tmp.append(s[0])
            tmp.append(cDo)
            kb_Nouns.append(tmp)
        else:
            print('node s[0] not found: ', s[0])

    noDupFoundList = []
    for i in kb_Nouns:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    kb_Nouns = noDupFoundList

    # uI
    for s in tagged_uI:
        tmp = []
        if t.isNode(s[0]):
#            print('found node s[0]: ', s[0])
            cDo = t.get_canDo(t.root, s[0])
            tmp.append(s[0])
            tmp.append(cDo)
            kb_uI.append(tmp)
        else:
            print('node s[0] not found: ', s[0])

    noDupFoundList = []
    for i in kb_uI:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    kb_uI = noDupFoundList

    return kb_Nouns, kb_uI


def inferConclusion(tagged_uI, nounsMatch, verbsMatch, kb_Nouns, kb_uI):

    conclusion = []

    print('start inferConclusion...')
    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print('len nounsMatch: ', len(nounsMatch))
    print('type nounsMatch: ', type(nounsMatch))
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))
    print('len kb_Nouns: ', len(kb_Nouns))
    print('type kb_Nouns: ', type(kb_Nouns))
    print('len kb_uI: ', len(kb_uI))
    print('type kb_uI: ', type(kb_uI))
    
    

    return conclusion


def tagSentence(sentence):

    taggedSentence = []

    if isinstance(sentence, str):
        sentList = sentence.split()
    elif isinstance(sentence, list):
        sentList = sentence
    else:
        print('Unknown sentence type: ', type(sentence))
        return None

    for w in sentList:
        tmp = []
        tag = getWordTag(w)
        tmp.append(w)
        tmp.append(tag)
        taggedSentence.append(tmp)

    return taggedSentence


def getMatchedTags(corpus, tagged_uI):

    matchedTags = []
    allTags = []
    tagOnly_uI = []
    
    for t in tagged_uI:
        tagOnly_uI.append(t[1])

    for sent in corpus:
        tagSent = []
        for word in sent:
            tmp = []
            tag = getWordTag(word)
            tmp.append(word)
            tmp.append(tag)
            tagSent.append(tmp)
        allTags.append(tagSent)

    for taggedSent in allTags:
        tags = []
        for t in taggedSent:
            tags.append(t[1])

        if tagOnly_uI == tags: # Wow a direct match!
            matchedTags.append(taggedSent)

    return matchedTags


def previousGrammar(tagged_uI, nounsMatch, verbsMatch, matchedTags, allVerbs):

    taggedNounsMatched = []
    taggedVerbsMatched = []
    previousGrammar = []

    print('start inferGrammar...')
    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print('len nounsMatch: ', len(nounsMatch))
    print('type nounsMatch: ', type(nounsMatch))
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))
    print('len matchedTags: ', len(matchedTags))
    print('type matchedTags: ', type(matchedTags))

    print('len allVerbs: ', len(allVerbs))
    print('type allVerbs: ', type(allVerbs))


    for s in nounsMatch:
        sent = []
        for entry in s[2]:
            tmp = []
            tag = getWordTag(entry)
            tmp.append(entry)
            tmp.append(tag)
            sent.append(tmp)
        taggedNounsMatched.append(sent)


    noDupFoundList = []
    for i in taggedNounsMatched:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    taggedNounsMatched = noDupFoundList

    print('nouns')
    for i in taggedNounsMatched:
        print(i)


    for s in verbsMatch:
        sent = []
        for entry in s[1][2]:
            tmp = []
            tag = getWordTag(entry)
            tmp.append(entry)
            tmp.append(tag)
            sent.append(tmp)
        taggedVerbsMatched.append(sent)


    noDupFoundList = []
    for i in taggedVerbsMatched:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    taggedVerbsMatched = noDupFoundList

    print('verbs')
    for i in taggedVerbsMatched:
        print(i)

    print('\ntagged uI: ', tagged_uI)


    # Based on the assumption the corpus has correct grammar...
    # Does our input match and of the noun matched sentences?

    # low hanging furit
    print('matchedTags found:')
    print(matchedTags)
    d = listDepth(matchedTags)
    print('d: ', d)
    if len(matchedTags) > 0:
        return matchedTags
    
        """
        uI_matched_matchedTags = []
        for t in matchedTags:
            print('t1: ', t)
            for x in t:
                print('x: ', x)

            for x, u in zip(t, tagged_uI):
                print('x: ', x)
                print('u2: ', u)
                if x[0] == u[0]:
                    uI_matched_matchedTags.append(x)
                else:
                    tmp = []
                    tmp.append('x')
                    tmp.append(x[1])
                    uI_matched_matchedTags.append(tmp)
        
        for m in uI_matched_matchedTags:
            print('m: ', m)
        """ 
            

    print('---')

    for n in taggedNounsMatched:
        if len(tagged_uI) != len(n):
            if len(tagged_uI) < len(n):
                print('tagged_uI is shorter than n')
                print(tagged_uI)
                print(n)
                if tagged_uI[0] == n[0]:
                    print('tagged_uI[0] == n[0]')
                    print(tagged_uI[0])
                    print(n[0])
                else:
                    print('tagged_uI[0] != n[0]')
                    print(tagged_uI[0])
                    print(n[0])

                winSize = 3
                for i in range(len(n) - winSize + 1):
                    window = n[i:i+winSize]
                    print('window: ', window)
                    if tagged_uI[i:i+winSize] == window:
                        print(' Match Found: ', tagged_uI[i:i+winSize])
                    
            elif len(tagged_uI) > len(n):
                print('tagged_uI is longer than n')
                print(tagged_uI)
                print(n)
                if tagged_uI[0] == n[0]:
                    print('tagged_uI[0] == n[0]')
                    print(tagged_uI[0])
                    print(n[0])
                else:
                    print('tagged_uI[0] != n[0]')
                    print(tagged_uI[0])
                    print(n[0])

                winSize = 3
                for i in range(len(tagged_uI) - winSize + 1):
                    window = tagged_uI[i:i+winSize]
                    print('window: ', window)
                    print('n[i:i+winSize]: ', n[i:i+winSize])
                    if n[i:i+winSize] == window:
                        print(' Match Found: ', n[i:i+winSize])
            else:
                print('tagged_uI has unkown len compared to n')
                print(tagged_uI)
                print(n)
        else:
            # This should never be reached and should be caught
            # via matchedTags (above)
            print('tagged_uI is equal to n')
            print(tagged_uI)
            print(n)
            if tagged_uI == n:
                print('   Exact match: tagged_uI == n')
                return n
                
            else:
                print('window search...')
                
                winSize = 3
                for i in range(len(tagged_uI) - winSize + 1):
                    window = tagged_uI[i:i+winSize]
                    print('window: ', window)
                    if n[i:i+winSize] == window:
                        print(' Match Found: ', n[i:i+winSize])


    return previousGrammar


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

    allInflections = getInflectionsPickle()

    print('len allInflections: ', len(allInflections))
    print('type allInflections: ', type(allInflections))
    print('-' * 5)
    
    nounsMatch, verbsMatch, allVerbs = checkCorpus(uI)

    print('len nounsMatch: ', len(nounsMatch))
    print('type nounsMatch: ', type(nounsMatch))
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))

    print('len allVerbs: ', len(allVerbs))
    print('type allVerbs: ', type(allVerbs))

#    print(xyz)
    print('-' * 5)


    tagged_uI = tagSentence(uI)

    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print(tagged_uI)

    print('-' * 5)

    # Are there sentences in the corpus where the tags match?
    # But where the words may be different...

    matchedTags = getMatchedTags(corpus, tagged_uI)

    print('len matchedTags: ', len(matchedTags))
    print('type matchedTags: ', type(matchedTags))
    print(matchedTags)

    

    print('-' * 5)

    print('KB Tree check...')

    t = getKB()

    kb_Nouns, kb_uI = checkKB(nounsMatch, tagged_uI)

    print('len kb_Nouns: ', len(kb_Nouns))
    print('type kb_Nouns: ', type(kb_Nouns))    
    for n in kb_Nouns:
        print(n)

    print('len kb_uI: ', len(kb_uI))
    print('type kb_uI: ', type(kb_uI))    
    for n in kb_uI:
        print(n)

    print('-' * 5)
    print('Can we learn any grammar?')

    previousGrammarMatch = previousGrammar(tagged_uI, nounsMatch, verbsMatch, matchedTags, allVerbs)

    print('len previousGrammarMatch: ', len(previousGrammarMatch))
    print('type previousGrammarMatch: ', type(previousGrammarMatch))

    print('-' * 5)
    print('inferConclusion...')

    conclusion = inferConclusion(tagged_uI, nounsMatch, verbsMatch, kb_Nouns, kb_uI)
    