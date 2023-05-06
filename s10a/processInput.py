#
# processInput.py
#

import pickle
## import pyinflect # For use as an extension of Spacy
### from pyinflect import getAllInflections, getInflection # Standalone
#from pyinflect import getAllInflections, getInflection
import simpConfig as sC
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
            if t[1] in [sC.vb, sC.vbd, sC.vbg, sC.vbn, sC.vbp, sC.vbz]:
                return True

    return False


def getVBxTag(w):

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


def getInflectionTag(vTag):

    if vTag in [sC.vb, sC.vbd, sC.vbg, sC.vbn, sC.vbp, sC.vbz]:
        return 'v'

    return 'x'


def checkCorpus(uI):

    baseWordSearch = True

    print('Processing checkCorpus...')

    uI_List = uI.split()
    print('uI_List: ', uI_List)

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
                
    print('len (NNx) sentsFound: ', len(sentsFound))
    print('type (NNx) sentsFound: ', type(sentsFound))
    
    # Of the above what are the verbs?
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
                        if (beforeWordTag in [sC.nn, sC.nnp, sC.nns, sC.prp]) and (afterWordTag in [sC.nn, sC.nnp, sC.nns, sC.prp]):
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
            

    
    return newSents




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


def checkKB():

    foundList = []

    for s in xyz:
        tmp = []
        if t.isNode(s[0]):
#            print('found node s[0]: ', s[0])
            cDo = t.get_canDo(t.root, s[0])
            tmp.append(s[0])
            tmp.append(cDo)
            foundList.append(tmp)
        else:
            print('node s[0] not found: ', s[0])

    noDupFoundList = []
    for i in foundList:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    foundList = noDupFoundList

    print('len foundList: ', len(foundList))
    print('type foundList: ', type(foundList))    
    for f in foundList:
        print(f)

    return "KB Check Complete"



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
    
    xyz = checkCorpus(uI)

    print('len xyz: ', len(xyz))
    print('type xyz: ', type(xyz))
#    print(xyz)
    print('-' * 5)

    print('KB Tree check...')

    t = getKB()

    kbResults = checkKB()
    
#    print(uI)
