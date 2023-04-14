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
from pathlib import Path


cfgFile = 'test.cfg'


def getPickles():

    with open('data/newDict.pkl', 'rb') as fp:
        topicalDict = pickle.load(fp)
        print('Aunt Bee loaded newDict.pkl')
    fp.close()

    with open('data/ourCorpus.pkl', 'rb') as fp:
        topicalCorpus = pickle.load(fp)
        print('Aunt Bee loaded ourCorpus.pkl')
    fp.close()
    

    return topicalDict, topicalCorpus


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


def buildCFG(data):

    rules = getCFGRules()

    firstLine = True
    
    for d in data:
        if firstLine:
            rules = rules + d[1] + ' -> ' + d[0]
            firstLine = False
        elif rules.find(d[0]) == -1:
            rules = rules + '\n' + d[-1] + ' -> ' + d[0]

    cf = open('testGrammar.cfg', 'w')
    cf.write(rules)
    cf.close()

    return


def buildTaggedDocs(topicalCorpus):

    taggedDocs = []

    print('topicalCorpus: ', topicalCorpus)

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

    
    
    print('Processing grammar...')

    topicalDict, topicalCorpus = getPickles()

    print('len topicalDict: ', len(topicalDict))
    print('type topicalDict: ', type(topicalDict))
#    for x, y in topicalDict.items():
#        print('x: {} y: {}'.format(x,y))
    
    print('len topicalCorpus: ', len(topicalCorpus))
    print('type topicalCorpus: ', type(topicalCorpus))
    print('-' * 5)



    taggedDocs = buildTaggedDocs(topicalCorpus)
    print('len taggedDocs: ', len(taggedDocs))
    print('type taggedDocs: ', type(taggedDocs))


    tokenDocs = buildTokenDocs(taggedDocs)
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
        
#    buildCFG(docs)

    testSent = [['see', 'jimmy', 'run']]

    taggedInputDocs = buildTaggedDocs(testSent)
    print('len taggedDocs: ', len(taggedInputDocs))
    print('type taggedDocs: ', type(taggedInputDocs))

    for test in taggedInputDocs:
        print(test)
    



    """
    draw = False

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
