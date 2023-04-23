#
# processCorpus.py
#
#

import os
import pickle
import spacy

from simpConfig import simple_contractions
from simpConfig import verbose



def getRawData():
    # Read the corpus files
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

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
                line = line.lower()
                corpusStr += line
    f.close()

    return corpusStr


def expandSents(corpusSents):

    expandedSents = []

    for s in corpusSents:

        expandedSentence = []
        tmpSent = s.split()

        for w in tmpSent:
            if w.find("'") != -1:
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
                    resultList = result.split()
                    for r in resultList:
                        expandedSentence.append(r)
                else:
                    expandedSentence.append(w)

            elif w.find(";") != -1:     # Remove
                w = w.replace(';', '')
                expandedSentence.append(w)
            elif w.find(",") != -1:     # Remove
                w = w.replace(',', '')
                expandedSentence.append(w)
            elif w in [' ', '-', ';', ',', '.', '..', '...']: # Skip over things we don't want
                continue 
            else:
                expandedSentence.append(w)

        expandedSents.append(expandedSentence)    

    return expandedSents


def cleanCorpus(expandedCorpusSents):
    cleanerCorpus = []
    bowList = []

    for sent in expandedCorpusSents:
        if len(sent) > 0:
            for word in sent:
                word = word.strip()
                if len(word) > 0:
                    bowList.append(word)
    
    
    
    return cleanerCorpus


if __name__ == "__main__":

    print('Processing corpus...')

    corpusString = getRawData()

    print('corpusString:')
    print(len(corpusString))
    print(type(corpusString))
#    print(corpusString[0:200])
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
    
    for s in expandedCorpusSents:
        print(s)
        for w in s:
            if w == "knowif":
                print('>>> bad s: ', s)
    print('-' * 5)

    cleanerCorpus = cleanCorpus(expandedCorpusSents)

