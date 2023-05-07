#
# processGrammar.py
#

import os
import pickle
import spacy
import grammarTools

from grammarTools import Grammar
from grammarTools import EarleyParse
from grammarTools import chkGrammar
#from processCorpus import verifyWords
from pathlib import Path


cfgFile = 'test.cfg'


def getPickles():

    with open('data/ourDict.pkl', 'rb') as fp:
        ourDict = pickle.load(fp)
        print('Aunt Bee loaded ourDict.pkl')
    fp.close()

    with open('data/newDict.pkl', 'rb') as fp:
        newDict = pickle.load(fp)
        print('Aunt Bee loaded newDict.pkl')
    fp.close()

    with open('data/ourCorpus.pkl', 'rb') as fp:
        ourCorpus = pickle.load(fp)
        print('Aunt Bee loaded ourCorpus.pkl')
    fp.close()

    with open('data/taggedCorpus.pkl', 'rb') as fp:
        taggedCorpus = pickle.load(fp)
        print('Aunt Bee loaded taggedCorpus.pkl')
    fp.close()

    return ourDict, newDict, ourCorpus, taggedCorpus


def getCFGRules():

    rules = ''

    progPath = os.getcwd()
    dataPath = progPath + '/cfg'

    file = Path(dataPath + '/cfg_rules.cfg')

    if file.is_file():

        rf = open(dataPath + '/cfg_rules.cfg', 'r') # Get base rules
        rules = rf.read()
        rf.close()
    else:
        print("File not found: " + str(dataPath + '/' + fRules))
        sys.exit("CFG Rules file not found")

    return(rules)


def buildCFG(newDict):

    rules = getCFGRules()

    firstLine = True

    print(len(newDict))
    print(type(newDict))
    print(newDict.get("eat_1"))
    print(newDict.get("do_1"))

    
    
    for key, value in newDict.items():
        word = newDict[key]['Word']
        tag = newDict[key]['Tag']
        word = word.strip()
        tag = tag.strip()
            
        if firstLine:
            rules = rules + tag + ' -> ' + word
            firstLine = False
#        elif rules.find(word) == -1: # unfortunately blocks "do" if there's a "dog"
        else: # Blindly processes everything
            if word == 'do':
                print('FOUND {} with tag {}'.format(word, tag))
            rules = rules + '\n' + tag + ' -> ' + word

    cf = open('test.cfg', 'w')
    cf.write(rules)
    cf.close()

    return


def buildTaggedDocs(topicalCorpus):

    taggedDocs = []

    nlp = spacy.load("en_core_web_lg") # Going for the best accuracy
    for sentence in topicalCorpus:
        strSentence = ' '.join(sentence)
        doc = nlp(strSentence)
        tmpDoc = []
        for token in doc:            
            tmpToken = ((str(token.text)), (str(token.tag_)))
            tmpDoc.append(tmpToken)

        taggedDocs.append(tmpDoc)

    return taggedDocs


def chkWords(testSents, newDict):

    wordsFound = []
    wordsNotFound = []

#    with open('data/newDict.pkl', 'rb') as fp:
#            newDict = pickle.load(fp)
#            print('Aunt Bee loaded newDict.pkl')
#    fp.close()
    
    for s in testSents:
        for w in s:
            for key, value in newDict.items():
                if w == newDict[key]['Word']:
#                    print('key: ', key)
#                    print('word: ', newDict[key]['Word'])
#                    print('tag: ', newDict[key]['Tag'])
                    wordsFound.append(w)
                    
    for s in testSents:
        for w in s:
            if w not in wordsFound:
                wordsNotFound.append(w)                     

    return wordsFound, wordsNotFound


def buildTokenDocs(taggedDocs):

    tokenDocs = []

    for doc in taggedDocs:
        rawSent = ''
        tokenDoc = []
        for tokens in doc:
            if rawSent == '':
                rawSent = tokens[0]
            else:
                rawSent = rawSent + ' ' + tokens[0]
            tokenDoc.append(tokens[1])
        tokenDocs.append(tokenDoc)

    return tokenDocs


def processInput(testSents):

    endTrim = []
    frontTrim = []
    
    tree = chkGrammar(' '.join(testSents[0]), draw)

    # Save tree to pickle
    with open('data/tree.pkl', 'wb') as fp:
        pickle.dump(tree, fp)
        print('Aunt Bee made a tree pickle')
    fp.close()

    if tree == None:
        # Check sentecne by removing end word(s)

        for sentence in testSents:
            tree = chkGrammar(' '.join(sentence), draw)
            i = 0
            tmp = sentence.copy()
            while i < len(sentence):
                tmp.pop()
                tree = chkGrammar(' '.join(tmp), draw)
                if tree != None:
                    endTrim.append(tmp.copy())
                i += 1

        # Check sentence by removing front word(s)
        for sentence in testSents:
            tree = chkGrammar(' '.join(sentence), draw)
            i = 0
            tmp = sentence.copy()
            while i < len(sentence):
                tmp.pop(0)
                tree = chkGrammar(' '.join(tmp), draw)
                if tree != None:
                    frontTrim.append(tmp.copy())
                i += 1

    return tree, endTrim, frontTrim



if __name__ == "__main__":

    draw = False
    foundMatch = False
    
    print('Processing grammar...')

    ourDict, newDict, ourCorpus, taggedCorpus = getPickles()

    print('len ourDict: ', len(ourDict))
    print('type ourDict: ', type(ourDict))
    print('len newDict: ', len(newDict))
    print('type newDict: ', type(newDict))
    print('-' * 5)
#    for x, y in topicalDict.items():
#        print('x: {} y: {}'.format(x,y))
    
    print('len ourCorpus: ', len(ourCorpus))
    print('type ourCorpus: ', type(ourCorpus))
    print('len taggedCorpus: ', len(taggedCorpus))
    print('type taggedCorpus: ', type(taggedCorpus))
    print('-' * 5)

    tokenDocs = buildTokenDocs(taggedCorpus)
    print('len tokenDocs: ', len(tokenDocs))
    print('type tokenDocs: ', type(tokenDocs))
    print('-' * 5)
#    for tok in tokenDocs:
#        print(tok)

    # Save tokenDocs to pickle
    with open('data/tokenDocs.pkl', 'wb') as fp:
        pickle.dump(tokenDocs, fp)
        print('Aunt Bee made a tokenDocs pickle')
    fp.close()

    print('-' * 5)
    buildCFG(newDict)
    print('cfg built')
    
#    testSents = [['see', 'jimmy', 'run', 'in', 'the', 'park', 'with', 'engelbert']]
#    testSents = [['see', 'jimmy', 'run', 'in', 'the', 'park', 'with', 'pookie']]
#    testSents = [['jimmy', 'and', 'pookie', 'ran', 'in', 'the', 'park']]
#    testSents = [['pookie', 'ran', 'in', 'the', 'park']]
#    testSents = [['who', 'is', 'jimmy']]
#    testSents = [['what', 'can', 'jimmy', 'do']]
    testSents = [['jimmy', 'can', 'not', 'run', 'in', 'the', 'park']]

    print('-' * 5)
    print('len testSents: ', len(testSents))
    print('type testSents: ', type(testSents))
    print('testSents:')
    for sent in testSents:
        print(sent)
    
    testWordsFound, testWordsNotFound = chkWords(testSents, newDict)

    print('testWordsFound:')
    print(len(testWordsFound))
    print(type(testWordsFound))
    print(testWordsFound)
#    for w in testWordsFound:
#        print(w)
    
    print('testWordsNotFound:')
    print(len(testWordsNotFound))
    print(type(testWordsNotFound))
    print(testWordsNotFound)
#    for w in testWordsNotFound:
#        print(w)

    # Save testWordsFound to pickle
    with open('data/testWordsFound.pkl', 'wb') as fp:
        pickle.dump(testWordsFound, fp)
        print('Aunt Bee made a testWordsFound pickle')
    fp.close()

    # Save testWordsNotFound to pickle
    with open('data/testWordsNotFound.pkl', 'wb') as fp:
        pickle.dump(testWordsNotFound, fp)
        print('Aunt Bee made a testWordsNotFound pickle')
    fp.close()
    

    print('-' * 5)

    taggedInputDocs = buildTaggedDocs(testSents)
    print('len taggedDocs: ', len(taggedInputDocs))
    print('type taggedDocs: ', type(taggedInputDocs))
    for test in taggedInputDocs:
        print(test)
    print('-' * 5)

    # Save taggedInputDocs to pickle
    with open('data/taggedInputDocs.pkl', 'wb') as fp:
        pickle.dump(taggedInputDocs, fp)
        print('Aunt Bee made a taggedInputDocs pickle')
    fp.close()    
                   
    tree, endTrim, frontTrim = processInput(testSents)



    if tree == None:
        print('len endTrim: ', len(endTrim))
        print('type endTrim: ', type(endTrim))
        for test in endTrim:
            print(test)

        print('len frontTrim: ', len(frontTrim))
        print('type frontTrim: ', type(frontTrim))
        for test in frontTrim:
            print(test)

        print('-' * 5)

        # Save endTrim to pickle
        with open('data/endTrim.pkl', 'wb') as fp:
            pickle.dump(endTrim, fp)
            print('Aunt Bee made a endTrim pickle')
        fp.close()

        # Save frontTrim to pickle
        with open('data/frontTrim.pkl', 'wb') as fp:
            pickle.dump(frontTrim, fp)
            print('Aunt Bee made a frontTrim pickle')
        fp.close()

        # Compare taggedInputDocs to tokenDocs
        tmp_taggedInputDocs = [['PRP', 'VBP', 'RB', 'JJ']]
        for doc in tokenDocs:
            for inDoc in taggedInputDocs:
#            for inDoc in tmp_taggedInputDocs:
                tmpDoc = []
                for w in inDoc:
                    tmpDoc.append(w[1])
                
                if doc == tmpDoc:
#                if doc == inDoc:
                    print('*** match: ')
                    print('doc: ', doc)
                    print('inDoc: ', tmpDoc)
                    foundMatch = True
#                else:
#                    print('NO match: ')
#                    print('doc: ', doc)
#                    print('inDoc: ', inDoc)
        if not foundMatch:
            print('tmpDoc {} not found in tokenDocs'.format(tmpDoc))
        print('foundMatch: ', foundMatch)    
    else:
        print(tree)

