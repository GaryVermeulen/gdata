#
# responseGenerator.py
#

import pickle


class Sentence: # Simple container class for input sentence data

    def __init__(self, inSent, sType, sSubj, sSubjAttr, sVerb, sObj, sObjAttr, sDT, sIN, sPP, sMD, sWDT):
        self.inSent    = inSent
        self.sType     = sType
        self.sSubj     = sSubj
        self.sSubjAttr = sSubjAttr
        self.sVerb     = sVerb
        self.sObj      = sObj
        self.sObjAttr  = sObjAttr
        self.sDT       = sDT
        self.sIN       = sIN
        self.sPP       = sPP
        self.sMD       = sMD
        self.sWDT      = sWDT


def getPickles():

    with open('data/tokenDocs.pkl', 'rb') as fp:
        tokenDocs = pickle.load(fp)
        print('Aunt Bee loaded tokenDocs.pkl')
    fp.close()

    with open('data/testWordsFound.pkl', 'rb') as fp:
        testWordsFound = pickle.load(fp)
        print('Aunt Bee loaded testWordsFound.pkl')
    fp.close()

    with open('data/testWordsNotFound.pkl', 'rb') as fp:
        testWordsNotFound = pickle.load(fp)
        print('Aunt Bee loaded testWordsNotFound.pkl')
    fp.close()

    with open('data/taggedInputDocs.pkl', 'rb') as fp:
        taggedInputDocs = pickle.load(fp)
        print('Aunt Bee loaded taggedInputDocs.pkl')
    fp.close()

    with open('data/tree.pkl', 'rb') as fp:
        tree = pickle.load(fp)
        print('Aunt Bee loaded tree.pkl')
    fp.close()

    with open('data/endTrim.pkl', 'rb') as fp:
        endTrim = pickle.load(fp)
        print('Aunt Bee loaded endTrim.pkl')
    fp.close()

    with open('data/frontTrim.pkl', 'rb') as fp:
        frontTrim = pickle.load(fp)
        print('Aunt Bee loaded frontTrim.pkl')
    fp.close()
    
    return tokenDocs, testWordsFound, testWordsNotFound, taggedInputDocs, tree, endTrim, frontTrim


def sentenceGrinder(taggedInputDocs):

    inSent    = ''
    sType     = []
    sSubj     = []
    sSubjAttr = []
    sVerb     = []
    sObj      = []
    sObjAttr  = []
    sDT       = []
    sIN       = []
    sPP       = []
    sMD       = []
    sWDT      = []

    ccFlag = False
    inFlag = False
    dtFlag = False

    print('sentenceGrinder... Start...')

    for sentence in taggedInputDocs:
        sentObj = Sentence(inSent, sType, sSubj, sSubjAttr, sVerb, sObj, sObjAttr, sDT, sIN, sPP, sMD, sWDT)
        sentObj.inSent = sentence
        tokenIndex = 0
        for token in sentence:
            if token[1] in ['NNP','NN','NNS']:
                print('found NNx {} at {}'.format(token, tokenIndex))
                nounAttributes = getNounAttributes(token)
                print(type(nounAttributes))
                print('getNounAttributes returned: ', nounAttributes)

                if tokenIndex == 0:
                    sentObj.sType.appned('declarative')

                if inFlag and dtFlag: # Looking for "in the NN"
                    sentObj.sObj.append(token[0])
                    sentObj.sObjAttr.append(nounAttributes)
                    sentObj.sPP.append(''.join(sIN))
                    sentObj.sPP.append(''.join(sDT))
                    sentObj.sPP.append(token[0])
                    inFlag = False
                    dtFlag = False
                else:
                    sentObj.sSubj.append(token[0])
                    sentObj.sSubjAttr.append(nounAttributes)

                if ccFlag:
                    sentObj.sSubj.append(token[0])
                    sentObj.sSubjAttr.append(nounAttributes)
                    ccFlag = False
                    
            elif token[1] in ['VB','VBD','VBG','VBN','VBP','VPZ']:
                print('found VBx {} at {}'.format(token, tokenIndex))

                if tokenIndex == 0:
                    sentObj.sType.append('imperative')

                sentObj.sVerb.append(token[0])
                
            elif token[1] in ['CC']:
                print('found CC {} at {}'.format(token, tokenIndex))

                ccFlag = True
                
            elif token[1] in ['CD']:
                print('found CD {} at {}'.format(token, tokenIndex))
                
            elif token[1] in ['DT']:
                print('found DT {} at {}'.format(token, tokenIndex))

                sentObj.sDT.append(token[0])
                dtFlag = True
                
            elif token[1] in ['EX']:
                print('found EX {} at {}'.format(token, tokenIndex))
                
            elif token[1] in ['IN']:
                print('found IN {} at {}'.format(token, tokenIndex))

                sentObj.sIN.append(token[0])
                inFlag = True
                
            elif token[1] in ['JJ']:
                print('found JJ {} at {}'.format(token, tokenIndex))
                
            elif token[1] in ['JJR']:
                print('found JJR {} at {}'.format(token, tokenIndex))
                
            elif token[1] in ['JJS']:
                print('found JJS {} at {}'.format(token, tokenIndex))
                
            elif token[1] in ['MD']:
                print('found MD {} at {}'.format(token, tokenIndex))

                sentObj.sMD.append(token[0])
                
            elif token[1] in ['PRP']:
                print('found PRP {} at {}'.format(token, tokenIndex))
              
            elif token[1] in ['PRP$']:
                print('found PRP$ {} at {}'.format(token, tokenIndex))

            elif token[1] in ['RB']:
                print('found RB {} at {}'.format(token, tokenIndex))

            elif token[1] in ['TO']:
                print('found TO {} at {}'.format(token, tokenIndex))

            elif token[1] in ['UH']:
                print('found UH {} at {}'.format(token, tokenIndex))

            elif token[1] in ['WDT']:
                print('found WDT {} at {}'.format(token, tokenIndex))
                if tokenIndex == 0:
                    sentObj.sType.append('interrogative')

            elif token[1] in ['WP']:
                print('found WP {} at {}'.format(token, tokenIndex))
                if tokenIndex == 0:
                    sentObj.sType.append('interrogative')

            elif token[1] in ['WRB']:
                print('found WRB {} at {}'.format(token, tokenIndex))
                if tokenIndex == 0:
                    sentObj.sType.append('interrogative')

            else:
                print('UNKOWN TOKEN found {} at {}'.format(token, tokenIndex))

            tokenIndex += 1
                
    print('sentenceGrinder... End.')
    return sentObj


def getNounAttributes(token):

    nnFile = 'kb/nn'
    nnpFile = 'kb/nnp'
    nnsFile = 'kb/nns'

    if token[1] == 'NN':
        f = open(nnFile, "r")
#        print('opened NN')
    elif token[1] == 'NNP':
        f = open(nnpFile, "r")
#        print('opened NNP')
    elif token[1] == 'NNS':
        f = open(nnsFile, "r")
#        print('opened NNS')
    else:
        print('Unknown filename: {}  Must be NN, NNP, or NNS.'.format(token[1]))
        return None

    for entry in f:
        tmpList = entry.split(';')
        if tmpList[0] == token[0].strip():
            entry = entry.strip('\n')
#            print('Found token {} in KB {}'.format(token, entry))
            return entry

    f.close()

    return None


def getMyData(me):

    nnpFile = nnFile = 'kb/nnp' # Where simp data resides
#    print(me)

    f = open(nnpFile, "r")
    for entry in f:
        tmpList = entry.split(';')
        if tmpList[0] == me:
            entry = entry.strip('\n')
#            print('Found token {} in KB {}'.format(me, entry))
            return entry
    f.close()

    return None


def saySomething(sentObj):

    questionFlag = False
    questionsFound = []
    factsFound = []

    firstWord   = ''
    secondWord  = ''
    sentenceObj = ''

    tmpSent = []

    simpAttr = getMyData('simp')

    print('simpAttr: ', simpAttr)
    print('type simpAttr: ', type(simpAttr))

    simpData = simpAttr.split(';')
    print(simpData)
    simpCanDo = simpData[3].split(',')
    print(simpCanDo) 


    for k, v in vars(sentObj).items():
        print(k, v)

    if sentObj.sType[0] == 'imperative':
        if sentObj.sVerb[0] not in simpCanDo:
            print('I am {} and I cannot {}'.format(simpData[0], sentObj.sVerb[0]))

    for subj, attr in zip(sentObj.sSubj, sentObj.sSubjAttr):
        print(subj, attr)
        tmpFact = []
        if attr == None:
            print('I do not know anything about ', subj)
            questionsFound.append(subj)
            questionFlag = True
        else:            
            subjAttributes = attr.split(';')
            tmpFact.append(subj)
            for v in sentObj.sVerb:
                if v in subjAttributes[3]:
                    print('{} can {}'.format(subj, v))
                    tmpFact.append(v)
            factsFound.append(tmpFact)

    print('factsFound: ', factsFound)
    print('questionsFound: ', questionsFound)

    if questionFlag:
        print('questionFlag true: ', questionFlag)
        # What is the tag of the unknow?
        for q in questionsFound:
            print('q: ', q)
            for word in sentObj.inSent:
                print('word: ', word)
                if q == word[0]:
                    print('word[1]: ', word[1])
                    if word[1] == 'NNP':
                        firstWord = 'WP' # What or who
                        secondWord = 'VBZ' # Is, does, and others that may not make sence
                        

        print(firstWord, secondWord)
        tmpSent.append(firstWord)
        tmpSent.append(secondWord)
        
        print(tmpSent)

        words = []
        f = open('test.cfg', "r")
        for entry in f:
            tmpWord = []
            if entry[0] == '#': # Skip
                continue
            else:
                entryList = entry.split('->')
                tag = entryList[0].strip()
                word = entryList[1].strip()
                if tag in tmpSent:
                    tmpWord.append(word)
                    tmpWord.append(tag)
            if len(tmpWord) > 0:
                words.append(tmpWord)
        f.close()
 
        print(words)

        # Now how to extract nonsensical words and form a sentence from 'words'
        # Knowing we have three types let's cheat...
        VBZs = []
        WPs = []
        obj = [] # ?

        for word in words:
            print(word)
            if word[1] in 'WP':
                WPs.append(word)
            elif word[1] in 'VBZ':
                VBZs.append(word)

        print(WPs)
        print(VBZs)
            
            
        
            
        

        


    return 'the cow says moo'


if __name__ == "__main__":

    print('responseGenerator... Start...')

    # Get what we know from processGrammar.py
    #
    tokenDocs, testWordsFound, testWordsNotFound, taggedInputDocs, tree, endTrim, frontTrim = getPickles()

    # Now the fun begins...
    #
    if tree == None:
        print('endTrim: ', endTrim)
        print('frontTrim: ', frontTrim)
    else:
#        print(tree)
#        print(type(tree))
#        tStr = tree.pformat_latex_qtree()
#        print('-' * 5)
#        print(tStr)
        print('-' * 5)
        print(taggedInputDocs)
        print('len taggedInputDocs[0]: ', len(taggedInputDocs[0]))
        print('-' * 5)
        sentObj = sentenceGrinder(taggedInputDocs)
        print('-' * 5)


        # Let's see if we can spit someting our the makes sence and is not canned
        print(saySomething(sentObj))
    
