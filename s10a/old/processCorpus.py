#
# processCorpus.py
#
#

import os
import pickle
import spacy

from simpConfig import simple_contractions
from simpConfig import verbose
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
        with open(dataPath + '/' + inFile, 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.replace('!', '.') # To simplify downstream processing
                line = line.replace('?', '.')
                line = line.replace('"', '')
                
                line = line.replace(chr(8216), "'") # Left single quote
                line = line.replace(chr(8217), "'") # Right single quote
                line = line.replace(chr(8220), '') # Left double quote
                line = line.replace(chr(8221), '') # Right double quote
                line = line.lower() # ??Or should we leave it??
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
                    print('>>{}<< not in simple contractions'.format(w))
                continue
                        
            clean_word = ''.join(filter(str.isalnum, w))

            if len(clean_word) > 0:
                expandedSentence.append(clean_word)
                
        expandedSents.append(expandedSentence)    

    return expandedSents


def cleanCorpus(expandedCorpusSents, starterDictList):
    cleanerCorpus = []
    bowList = []
    starterBOWList = []

    for sent in expandedCorpusSents:
        if len(sent) > 0:
            for word in sent:
                word = word.strip()
                if len(word) > 0:
                    bowList.append(word)
    print('before len bowList: ', len(bowList))

    bowList = list(dict.fromkeys(bowList))

    print('after len bowList: ', len(bowList))

#    for w in bowList:
#        print(w)

    for entry in starterDictList:
        starterBOWList.append(entry[0])
    
    bowSet = set(bowList)
    starterSet = set(starterBOWList)

    diff = bowSet.difference(starterSet)

#    for d in diff:
#        print(d)

    print('len diff: ', len(diff))

    goodWords, badWords = chkUnkownWords(diff)

    print('-' * 5)
    print('len goodWords: ', len(goodWords))
    print('len badWords: ', len(badWords))
    for w in badWords:
        print(w)

    cleanerCorpus = rejectNotFound(expandedCorpusSents, badWords)
    
    return cleanerCorpus


def rejectNotFound(expandedCorpusSents, notFound):

    goodSents = []
    skipSent = False

    for s in expandedCorpusSents:
        for w in s:
            if w in notFound:
                skipSent = True
        if skipSent:
            skipSent = False
            continue
        else:
            skipSent = False
            goodSents.append(s)
    
    return goodSents


def mergeCorpus(cleanerCorpus, starterCorpus):

    return cleanerCorpus + starterCorpus


def tagCleanerCorpus(cleanerCorpus):

    taggedCorpus = []

    nlp = spacy.load("en_core_web_lg") # lg has best accuracy

    for sentence in cleanerCorpus:
        strSentence = ' '.join(sentence)
        doc = nlp(strSentence)
        for token in doc:            
            tmpToken = ((str(token.text)), (str(token.tag_)))
            taggedCorpus.append(tmpToken)

    taggedCorpus = list(dict.fromkeys(taggedCorpus)) # Remove duplicates

    return taggedCorpus

def buildLex():

    corpusString = getRawCorpus()
    corpusSents = corpusString.split('.')
    expandedCorpusSents = expandSents(corpusSents) # Change don't  to do not

    cnt = 1
    for s in expandedCorpusSents:
        print('{}, {}'.format(cnt, s))
        cnt += 1
            


    return 'a bunch of stuff'


#
#
#
if __name__ == "__main__":

    print('Processing corpus...')

    results = buildLex()


    """

    corpusString = getCorpus()

    starterDictList = loadStarterDictionary()

    print('corpusString:')
    print(len(corpusString))
    print(type(corpusString))
#    print(corpusString[0:200])
    print('-' * 5)
    print('starterDictList:')
    print(len(starterDictList))
    print(type(starterDictList))
    
    for w in starterDictList:
        print(w)
  
    # Save new working dictionary...
    with open('pickles/starterDictList.pkl', 'wb') as fp:
        pickle.dump(starterDictList, fp)
        print('Aunt Bee made a starterDictList pickle')
    fp.close()

    print('-' * 5)
    
    corpusSents = corpusString.split('.')

    print('corpusSents:')
    print(len(corpusSents))
    print(type(corpusSents))
    print('-' * 5)

    expandedCorpusSents = expandSents(corpusSents)

    print('expandedCorpusSents:')
    print(len(expandedCorpusSents))
    print(type(expandedCorpusSents))
    """
    """
    for s in expandedCorpusSents:
        print(s)
        for w in s:
            if w == "knowif":
                print('>>> bad s: ', s)
    """
    """
    print('-' * 5)
    
    cleanerCorpus = cleanCorpus(expandedCorpusSents, starterDictList)
    
    print('cleanerCorpus:')
    print(len(cleanerCorpus))
    print(type(cleanerCorpus))
    """
    """
    for s in cleanerCorpus:
        print(s)
        for w in s:
            if w == "knowif":
                print('>>> bad s: ', s)
    """
    """
    print('-' * 5)

    taggedCorpus = tagCleanerCorpus(cleanerCorpus)

    print('taggedCorpus:')
    print(len(taggedCorpus))
    print(type(taggedCorpus))

    for t in taggedCorpus:
        print(t)

    # Merge starter and corpus dictionaries
    newTaggedList = taggedCorpus + starterDictList

    print('newTaggedList:')
    print(len(newTaggedList))
    print(type(newTaggedList))

    newTaggedList = list(dict.fromkeys(newTaggedList)) # Remove duplicates

    counter = 0
    for t in newTaggedList:
        counter += 1
        print(counter, t)
    

    # Save new tagged list w/starter...
    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(newTaggedList, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()

    
    print('-' * 5)

    starterCorpus = loadStarterSentences()

    print('starterCorpus:')
    print(len(starterCorpus))
    print(type(starterCorpus))
    print('-' * 5)

    newCorpus = mergeCorpus(cleanerCorpus, starterCorpus)

    print('newCorpus:')
    print(len(newCorpus))
    print(type(newCorpus))
#    for s in newCorpus:
#        print(s)

    # Save new working corpus...
    with open('pickles/newCorpus.pkl', 'wb') as fp:
        pickle.dump(newCorpus, fp)
        print('Aunt Bee made a newCorpus pickle')
    fp.close()


    # Tag the combined corpus and retain the sentences
    tagSent = []
    for sentence in newCorpus:
        
        strSentence = ' '.join(sentence)
        doc = nlp(strSentence)

        tagSent.append(doc)
        """
        """
        for token in doc:            
            tmpToken = ((str(token.text)), (str(token.tag_)))
            taggedCorpus.append(tmpToken)
        """
        """
    # Save new working corpus...
    with open('pickles/taggedCorpusSents.pkl', 'wb') as fp:
        pickle.dump(tagSent, fp)
        print('Aunt Bee made a taggedCorpusSents.pkl pickle')
    fp.close()
    """

    print('processCorpus Complete.')  