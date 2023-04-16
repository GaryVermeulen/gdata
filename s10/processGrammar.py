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


def buildCFG(dataDict):

    rules = getCFGRules()

    firstLine = True
    
    for key, value in dataDict.items():
        word = dataDict[key]['Word']
        tag = dataDict[key]['Tag']
        word = word.strip()
        tag = tag.strip()
            
        if firstLine:
            rules = rules + tag + ' -> ' + word
            firstLine = False
        elif rules.find(word) == -1:
            rules = rules + '\n' + tag + ' -> ' + word

    cf = open('test.cfg', 'w')
    cf.write(rules)
    cf.close()

    return


def buildTaggedDocs(topicalCorpus):

    taggedDocs = []

#    print('topicalCorpus: ', topicalCorpus)

    nlp = spacy.load("en_core_web_lg") # Going for the best accuracy
    for sentence in topicalCorpus:
        strSentence = ' '.join(sentence)
#        print(strSentence)
#        if len(strSentence) > 10:
#            testSent = strSentence
        doc = nlp(strSentence)
#        print('doc: ', doc)
        tmpDoc = []
        for token in doc:            
#            print('token.text: ', token.text)    
#            print(f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
            tmpToken = ((str(token.text)), (str(token.tag_)))
            tmpDoc.append(tmpToken)

        taggedDocs.append(tmpDoc)

    return taggedDocs


def chkWords(testSents):

    wordsFound = []
    wordsNotFound = []

    with open('data/newDict.pkl', 'rb') as fp:
            newDict = pickle.load(fp)
            print('Aunt Bee loaded newDict.pkl')
    fp.close()

#    for key, value in ourDict.items():
#        print('key: {} value: {}'.format(key, value))
#    
#    print('input expandedCorpusSents: ', expandedCorpusSents)
    
    for s in testSents:
#        print('s: ', s)
        for w in s:
            for key, value in newDict.items():
#                print(key, value)
                if w == newDict[key]['Word']:
                    print('key: ', key)
                    print('word: ', newDict[key]['Word'])
                    print('tag: ', newDict[key]['Tag'])
                    wordsFound.append(w)
                    
    for s in testSents:
        for w in s:
            if w not in wordsFound:
                wordsNotFound.append(w)


            
#            print('w: ', w)
#            for key in newDict:
#                
#                if w == key[:-2]:
#                    print('found: ', key[:-2])
#                    wordsFound.append(w)
#                else:
#                    if w not in wordsFound:
#                    print('not found: ', key[:-2])
#                        wordsNotFound.append(w)
                            
    # Remove duplicates
#    wordsFound = list(dict.fromkeys(wordsFound))
#    wordsNotFound = list(dict.fromkeys(wordsNotFound))                     

    return wordsFound, wordsNotFound


def buildTokenDocs(taggedDocs):

    tokenDocs = []

    for doc in taggedDocs:
#        print('---')
#        print('doc: ', doc)
        rawSent = ''
        tokenDoc = []
        for tokens in doc:
            if rawSent == '':
                rawSent = tokens[0]
            else:
                rawSent = rawSent + ' ' + tokens[0]
            tokenDoc.append(tokens[1])
#        print('rawSent: ', rawSent)
#        print('tokDoc: ', tokenDoc)
        tokenDocs.append(tokenDoc)

    return tokenDocs



if __name__ == "__main__":

    draw = False
    
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
    
#    testSent = [['see', 'jimmy', 'run', 'in', 'the', 'park', 'with', 'engelbert']]
    testSent = [['see', 'jimmy', 'run', 'in', 'the', 'park', 'with', 'pookie']]

    testWordsFound, testWordsNotFound = chkWords(testSent)

    print('testWordsFound:')
    print(len(testWordsFound))
    print(type(testWordsFound))
    print(testWordsFound)
    for w in testWordsFound:
        print(w)
    
    print('testWordsNotFound:')
    print(len(testWordsNotFound))
    print(type(testWordsNotFound))
    print(testWordsNotFound)
    for w in testWordsNotFound:
        print(w)

    print('-' * 5)

    taggedInputDocs = buildTaggedDocs(testSent)
    print('len taggedDocs: ', len(taggedInputDocs))
    print('type taggedDocs: ', type(taggedInputDocs))

    for test in taggedInputDocs:
        print(test)
    
    tree = chkGrammar(' '.join(testSent[0]), draw)


    """
    

    for sentence in topicalCorpus:
        print('-' * 10)
        print(sentence)
        tree = chkGrammar(' '.join(sentence), draw)
        while tree == None:
            if len(sentence) > 0:
                sentence.pop()
                tree = chkGrammar(' '.join(sentence), draw)
            elif len(sentence) < 1:
                break

    """
