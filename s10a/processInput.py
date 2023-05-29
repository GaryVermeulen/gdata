#
# processInput.py
#

import pickle

from commonUtils import *
from simpConfig import *
from processKB import *
from simpSA import *

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

    tags = ''
    
    for t in newTaggedList:
        if word == t[0]:
            if tags == '':
                tags = t[1]
            else:
                tags = tags + ', ' + t[1]
    return tags


def isNNx(w):

    for t in newTaggedList:
        if w == t[0]:
            if t[1] in ['NN', 'NNP', 'NNS']:
                return True

    return False


def isVBx(w):

    for t in newTaggedList:
        if w == t[0]:
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


def getInflectionTag(tag):

    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'
    elif tag in [nns]:
        return 'n'

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
    
    print('--' * 5)
    print('Do any of the verbs in the senetences found match the input sentence?')
    # Do any of the verbs in the senetences found match the input sentence?
    verbsMatch = []
    for w_uI in uI_List:
        if isVBx(w_uI):
#            print('w_uI: ', w_uI)
##            for nS in newSents:
            for nS in sentsFound_wVBs:
#                print('nS: ', nS)
                # direct match (non-inflection)
                tmp = []
                if w_uI in nS[1]: # was 2
#                    print('direct verb match w_uI {} found in nS[2] {}'.format(w_uI, nS[2]))
                    tmp.append(w_uI)
                    tmp.append(nS)
                    verbsMatch.append(tmp)
                else:
                    for v in nS[2]: # was 3
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

#    for v in verbsMatch:
#        print(v)
               
    return sentsFound, sentsFound_wVBs, verbsMatch


def validInput(uI):

    uI_List = uI.split()
    valid_uI = []
    tmp = []

    for word in newTaggedList:
        if word[0] in uI_List:
            if word[0] not in valid_uI:
                valid_uI.append(word[0])

    uI_Set = set(uI_List)
    valid_uI_Set = set(valid_uI)

    diff = uI_Set.difference(valid_uI)
    intr = uI_Set.intersection(valid_uI)

    # Cheesy way to keep order but drop unknown words
    for i in uI_List:
        if i in valid_uI:
            tmp.append(i)
    
    return tmp, diff, intr


def getInflections(word, tag, baseWordSearch):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag)) 
    for line in allInflections:
        if word in line:
#            print('found {} at {} {}'.format(word, cnt, line))
#            print('tag: ', tag)
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


def checkKB(sents):

    kb_Nouns = []
    baseWordSearch = False
    inflect = []

#    print('checkKB::::::')
#    print('len sents: ', len(sents))
#    print('type sents: ', type(sents))
    
    for s in sents:
#        print('s: ', s)
        sWord = s[0]
        sTag  = s[1]
#        if is_uI:
#            sTag  = s[1]
#        else:
#            sTag = s[2][
        if sTag == nns:
#            print('sWord: {} sTag: {}'.format(sWord, sTag))
            tag = getInflectionTag(sTag)
#            print('tag: ', tag)
            inflect = getInflections(sWord, tag, baseWordSearch)        
#            print('inflect:')
#            print(inflect)

        if len(inflect) > 0:
            sWord = inflect[0]
            inflect = []
            
        tmp = []
        if t.isNode(sWord):
#            print('found node sWord: ', s[0])
            cDo = t.get_canDo(t.root, sWord)
            tmp.append(sWord)
            tmp.append(cDo)
            kb_Nouns.append(tmp)
        else:
#            print('node sWord not found: ', sWord)
#            print('sTag: ', sTag)
            if sTag in [nn, nns]:
                tmp.append(sWord)
                tmp.append('unknown')
                kb_Nouns.append(tmp)

    noDupFoundList = []
    for i in kb_Nouns:
        if i not in noDupFoundList:
            noDupFoundList.append(i)
    kb_Nouns = noDupFoundList

    return kb_Nouns


def inferConclusion(tagged_uI, nounsMatch, verbsMatch, kb_Nouns, kb_uI, fragmentMatches):

    """
        declarative sentence (statement)
        interrogative sentence (question)
        imperative sentence (command)
        exclamative sentence (exclamation)
    """

    firstWord = True
    sentSubject = ''
    sentObject = ''
    nMatch = []
    vMatch = []
    conclusion = ['i', 'do', 'not', 'have', 'a', 'clue']

    print('start inferConclusion...')
    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print(tagged_uI)
    
    print('len nounsMatch: ', len(nounsMatch))
    print('type nounsMatch: ', type(nounsMatch))
    for n in nounsMatch:
        print(n)
        
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))
    for v in verbsMatch:
        print(v)
        
    print('len kb_Nouns: ', len(kb_Nouns))
    print('type kb_Nouns: ', type(kb_Nouns))
    for kbN in kb_Nouns:
        print(kbN)
        
    print('len kb_uI: ', len(kb_uI))
    print('type kb_uI: ', type(kb_uI))
    for kbUI in kb_uI:
        print(kbUI)
        
    print('len fragmentMatches: ', len(fragmentMatches))
    print('type fragmentMatches: ', type(fragmentMatches))
    for f in fragmentMatches:
        print(f)



    simpCanDo = t.get_canDo(t.root, simp)
    simpCanDo = simpCanDo.split(',')

    print('simpCanDo: ', simpCanDo)
            

    # Sentence analysis...~? Do we really want to do this?
    # Or just catch commands and do a simp check?
    for word in tagged_uI:
        if word[1] in [vb, vbd, vbg, vbn, vbp, vbz]: # Assuming imperative
            if firstWord:
                if word[0] in simpCanDo:
                    print('YES, simp can: ', word[0])
                else:
                    print('NO, simp cannot: ', word[0])
            #else:
#        elif word[1] in [nn, nnp, nns]:
#            if sentSubj == '':
#                sentSubj = word[0]        
        firstWord = False



    sA_Obj = sentAnalysis(tagged_uI)
    sA_Obj.printAll()
    print('-' * 8)

    saList = []
    for nMatch in nounsMatch:
        tagged = tagSentence(nMatch[1], [])
        sa = sentAnalysis(tagged)
        sa.printAll()
        saList.append(sa)
                      

#    return conclusion
    return sA_Obj


def tagSentence(sentence, newWords):

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
        if tag == '':
            tag = newWordTag(w, newWords)
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


def fragmentMatcher(tagged_uI, nounsMatch, verbsMatch, matchedTags):

    taggedNounsMatched = []
    taggedVerbsMatched = []
    fragmentMatches = []

    print('start fragmentMatcher...')
    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print('len nounsMatch: ', len(nounsMatch))
    print('type nounsMatch: ', type(nounsMatch))
    print('len verbsMatch: ', len(verbsMatch))
    print('type verbsMatch: ', type(verbsMatch))
    print('len matchedTags: ', len(matchedTags))
    print('type matchedTags: ', type(matchedTags))

    for s in nounsMatch:
        sent = []
        for entry in s[1]:
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

    print('nouns taggedNounsMatched:')
    for i in taggedNounsMatched:
        print(i)


    for s in verbsMatch:
        sent = []
        for entry in s[1][1]:
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

    print('verbs taggedVerbsMatched')
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
    

    print('---')

    for n in taggedNounsMatched:
        if len(tagged_uI) != len(n):
            if len(tagged_uI) < len(n):
#                print('tagged_uI is shorter than n')
#                print(tagged_uI)
#                print(n)

                winSize_i = 3
                winSize_j = 3
                for i in range(len(n) - winSize_i + 1):
                    window_i = n[i:i+winSize_i]
#                    print('window_i: ', window_i)
                    for j in range(len(tagged_uI) - winSize_j + 1):
                        window_j = tagged_uI[j:j+winSize_j]
#                        print('window_j: ', window_j)
                        if window_i == window_j:
#                            print(' < Match Found: ', window_i)
                            fragmentMatches.append(n)
                            break
                    
            elif len(tagged_uI) > len(n):
#                print('tagged_uI is longer than n')
#                print(tagged_uI)
#                print(n)

                winSize_i = 3
                winSize_j = 3
                for i in range(len(tagged_uI) - winSize_i + 1):
                    window_i = tagged_uI[i:i+winSize_i]
#                    print('window_i: ', window_i)
                    for j in range(len(n) - winSize_j + 1):
                        window_j = n[j:j+winSize_j]
#                        print('window_j: ', window_j)
                        if window_i == window_j:
#                            print(' > Match Found: ', window_i)
                            fragmentMatches.append(n)
                            break
            else:
                print('tagged_uI has unkown len compared to n')
                print(tagged_uI)
                print(n)
        else:
#            print('tagged_uI is equal to n')
#            print(tagged_uI)
#            print(n)
            if tagged_uI == n:
                print('   Exact match: tagged_uI == n')
                return n
                
            else:
                print('window search...')
                
                for i in range(len(tagged_uI) - winSize_i + 1):
                    window_i = tagged_uI[i:i+winSize_i]
#                    print('window_i: ', window_i)
                    for j in range(len(n) - winSize_j + 1):
                        window_j = n[j:j+winSize_j]
#                        print('window_j: ', window_j)
                        if window_i == window_j:
#                            print(' = Match Found: ', window_i)
                            fragmentMatches.append(n)
                            break

    return fragmentMatches


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
#    for v in valid_uI:
#        print(v)
    print('valid_uI: ', valid_uI)
    print('diff: ', diff)
    print('intr: ', intr)
    print('-' * 5)

    if len(diff) > 0:
        newWords, notFound = chkUnkownWords(diff)

        print('newWords: ', newWords)
        print('notFound: ', notFound)
    else:
        print('All input words known...')
        newWords = []
        
    print('-' * 5)

    tagged_uI = tagSentence(uI, newWords)

    print('len tagged_uI: ', len(tagged_uI))
    print('type tagged_uI: ', type(tagged_uI))
    print(tagged_uI)

    print('-' * 5)


    allInflections = getInflectionsPickle()

    print('len allInflections: ', len(allInflections))
    print('type allInflections: ', type(allInflections))
    print('-' * 5)
    
    taggedNounsMatch, nounsMatch, verbsMatch = checkCorpus(uI)

    print('---len taggedNounsMatch: ', len(taggedNounsMatch))
    print('---type taggedNounsMatch: ', type(taggedNounsMatch))
    print('--len nounsMatch: ', len(nounsMatch))
    print('--type nounsMatch: ', type(nounsMatch))
    print('-len verbsMatch: ', len(verbsMatch))
    print('-type verbsMatch: ', type(verbsMatch))

#    print('len allVerbs: ', len(allVerbs))
#    print('type allVerbs: ', type(allVerbs))

#    print(xyz)
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

    # Do we care about nouns in the corpus which are not in the kb?
    # Yes...~?
    kb_Nouns = checkKB(matchedTags) 
    kb_uI = checkKB(tagged_uI)

    print('len kb_Nouns: ', len(kb_Nouns))
    print('type kb_Nouns: ', type(kb_Nouns))    
    for n in kb_Nouns:
        print(n)

    print('len kb_uI: ', len(kb_uI))
    print('type kb_uI: ', type(kb_uI))    
    for n in kb_uI:
        print(n)

    print('-' * 5)
    print('Any fragement matches?')

    fragmentMatches = fragmentMatcher(tagged_uI, nounsMatch, verbsMatch, matchedTags)

    print('len fragmentMatches: ', len(fragmentMatches))
    print('type fragmentMatches: ', type(fragmentMatches))
    for f in fragmentMatches:
        print('f: ', f)

    print('-' * 5)
    print('inferConclusion (main)...')

#    conclusion = inferConclusion(tagged_uI, nounsMatch, verbsMatch, kb_Nouns, kb_uI, fragmentMatches)
    sA_Obj = inferConclusion(tagged_uI, nounsMatch, verbsMatch, kb_Nouns, kb_uI, fragmentMatches)    
    sA_Obj.printAll()


    
