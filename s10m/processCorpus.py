#
# processCorpus.py
#
#

import os
import spacy # spacy is a pig

from commonConfig import simple_contractions
from commonConfig import verbose
from commonUtils import chkUnkownWords


nlp = spacy.load("en_core_web_lg") # lg has best accuracy



def getRawCorpus():
    # Read the raw corpus files
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

    # Read corpus input
    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r', encoding="utf8") as f: # Added , encoding="utf8" for Win PC
            while (line := f.readline()):
                corpusStr += line
    f.close()

    return corpusStr


def loadStarterDictionary():

    startList = []

    with open('data/starterDictionary.txt', 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.strip()
                line = line.split(',')
                tup = (line[0].strip(),line[1].strip())
                startList.append(tup)
    f.close()

    return startList


def loadStarterSentences():

    startSentList = []

    with open('data/starterSentences.txt', 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.strip()
                tmp = line.split()
                startSentList.append(tmp)
    f.close()

    return startSentList


def expandSents(corpusSents):

    expandedSents = []
    wordCnt = 0

    for s in corpusSents:
        expandedSentence = []
        tmpSent = s.split()

        for w in tmpSent:
            
            w = w.strip()
            wordCnt += 1
            
            if w.find("'") != -1: # Doesn't handle idioms such as: someone's
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
                    resultList = result.split()
                    for r in resultList:
                        expandedSentence.append(r)
                else:
                    print('>>{}<< not in  contractions'.format(w))
                continue
                        
            clean_word = ''.join(filter(str.isalnum, w))

            if len(clean_word) > 0:
                expandedSentence.append(clean_word)
                
        expandedSents.append(expandedSentence)    

    return expandedSents


def buildTaggedBoW(taggedCorpus):

    taggedBoW = loadStarterDictionary()

    for s in taggedCorpus:
        for w in s:
            if w not in taggedBoW:
                taggedBoW.append(w)

    return(taggedBoW)


def processRawCorpusString(rawCorpusString):

    tmpLst = []
    tmpSent = ''
    newSent = []


    for char in rawCorpusString:
        if char == '.':     # We'll need to handle multiple ...
            newSent.append(tmpSent + '.')
            tmpSent = ''
        elif char == '?':   # We'll need to handle multiple ???
            newSent.append(tmpSent + '?')
            tmpSent = ''
        elif char == '!':   # We'll need to handle multiple !!!
            newSent.append(tmpSent + '!')
            tmpSent = ''
        elif char == ';':   # We'll need to handle multiple ;;;
            newSent.append(tmpSent + ';')
            tmpSent = ''
        elif char == '"':   # Skip "
            continue 
        elif char == '\n':
            tmpSent = tmpSent + ' '
        else:
            tmpSent = tmpSent + char

    for sent in newSent:
        sent = sent.lstrip()
        if sent[0] == '-' and sent[1] == '-':
            sent = sent[2:]
        tmpLst.append(sent)
        
            

    return tmpLst


def buildLex():

    cnt = 0

    print(' --- start buildLex() ---')

    rawCorpusString = getRawCorpus()

    print(len(rawCorpusString))
    print(type(rawCorpusString))
#    print(rawCorpusString)

    processedCorpus = processRawCorpusString(rawCorpusString)

    print('---')

    print(len(processedCorpus))
    print(type(processedCorpus))
#    print(processedCorpus)
#    for line in processedCorpus:
#        print(line)
    while cnt < len(processedCorpus):
        print('{}: ->{}<-'.format(cnt, processedCorpus[cnt]))
        cnt += 1
    

    """
    corpusSents = corpusString.split('.')
    expandedCorpusSents = expandSents(corpusSents) # Change don't  to do not
    startSentList = loadStarterSentences()

    completeUntaggedCorpus = expandedCorpusSents + startSentList

    completeUntaggedCorpus = [x for x in completeUntaggedCorpus if not len(x) < 1] # Remove empty entries [] 

    # Let's see what we have thus far...
    print(len(completeUntaggedCorpus))
    print(type(completeUntaggedCorpus))

    for x in completeUntaggedCorpus:
        print(x)
    """
    
    """
    # Build/convert into tagged sentences
    taggedCorpus = []
    for s in completeUntaggedCorpus:
        if len(s) > 0: # Just to make sure
            doc = nlp(' '.join(s))
            tagSent = []
            for token in doc:
                tmpToken = ((str(token.text)), (str(token.tag_)))
                tagSent.append(tmpToken)
            taggedCorpus.append(tagSent)


    taggedBoW = buildTaggedBoW(taggedCorpus)
    """


    """
    cnt = 1
    for s in taggedBoW:
        print('{}, {}'.format(cnt, s))
        cnt += 1

    print('len: ', len(taggedBoW))
    """     
    print(' --- end buildLex() ---')
    return 'Built: untaggedCorpusSents, taggedCorpusSents, and taggedBoW'


#
#
#
if __name__ == "__main__":

    print('Start: processCorpus (__main__): buildLex')
    print(buildLex())
    print('End: processCorpus (__main__): buildLex')  
