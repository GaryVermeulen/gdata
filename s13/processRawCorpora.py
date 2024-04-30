#
# processRawCorpus.py
#
#

import os

from commonConfig import common2LetterWords
from commonConfig import nnp, prp
from commonUtils import connectMongo
from expandAndTag import expandAndTag





def getRawCorpus():
    # Read the raw corpus file(s)
    corpora = []
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
        bookName = inFile[: -4]
        corpora.append((bookName, corpusStr))
        corpusStr = ''

    return corpora


def expandAndTagSents(processedCorpora):

    taggedCorpora = []
    bookName = ''
    corpusStrings = []

    for corpus in processedCorpora:

        bookName = corpus[0]
        completeUntaggedCorpus = corpus[1]
        expandedSents = []
        sentCnt = 0

        for s in completeUntaggedCorpus:
            sentCnt += 1
            expandedSentence = []

            expandedSentence = expandAndTag(s)       
      
            expandedSents.append(expandedSentence)
            
        taggedCorpora.append((bookName, expandedSents))

    return taggedCorpora # expandedSents


def processRawCorporaStrings(rawCorpora):

    bookName = ''
    rawCorpusString = ''
    processedCorpora = []

#    print(type(rawCorpora))
#    print(len(rawCorpora))

    for corpus in rawCorpora:

        tmpLst = []
        tmpSent = ''
        newSent = []

        bookName = corpus[0]
        rawCorpusString = corpus[1]

#        print('bookName: ', bookName)

        for char in rawCorpusString:
            if char == '.':     # We'll need to handle Mr. & Mrs.
                #newSent.append(tmpSent + '.')
                newSent.append(tmpSent)
                tmpSent = ''
            elif char == ',':   #
                continue
            elif char == '?':   # We'll need to handle multiple ???
                newSent.append(tmpSent + '?')
                tmpSent = ''
            elif char == '!':   # We'll need to handle multiple !!!
                newSent.append(tmpSent + '!')
                tmpSent = ''
            elif char == ';':   # We'll need to handle multiple ;;;
                newSent.append(tmpSent + ';')
                tmpSent = ''
            elif char == '"':   # Skip " chr 34
                continue
            elif char == '*':   # Skip * chr 42
                continue
            elif char == '(':   # Skip ( chr 40
                continue
            elif char == ')':   # Skip ) chr 41
                continue
            elif char == chr(8216): # Replace unicode left quotation
                tmpSent = tmpSent + "'"
            elif char == chr(8217): # Repalce unicode right quotation
                tmpSent = tmpSent + "'"
            elif char == chr(8220): # Skip unicode left double quotation
                continue
            elif char == chr(8221): # Skip unicode right double quotation
                continue
            elif char == '\n':
                tmpSent = tmpSent + ' '
            else:
                tmpSent = tmpSent + char

        # Remove leading spaces and --
        for sent in newSent:
            sent = sent.lstrip()
            if len(sent) > 1:
                if sent[0] == '-' and sent[1] == '-':
                    sent = sent[2:]
            tmpLst.append(sent)

        # remove dash at end of word: word1- word2
        newSent.clear()
        for sent in tmpLst:
            tmpSent = ''
            tmpSentLst = sent.split()
            for word in tmpSentLst:
                if word[-1] == '-':
                    word = word[:-1]
                if tmpSent == '':
                    tmpSent = tmpSent + word
                else:
                    tmpSent = tmpSent + ' ' + word
            newSent.append(tmpSent)

        # Replace dash with space: word1-word2
        tmpLst.clear()
        for sent in newSent:
            newS = ""
            newS = sent.replace("-", " ")
            if newSent == "":
                tmpLst.append(sent)
            else:
                tmpLst.append(newS)

        # Remove single char sentences and double spaces
        newSent.clear()
        for sent in tmpLst:
            sent = sent.replace("  ", " ")
            if len(sent) > 1:
                newSent.append(sent)

        processedCorpora.append((bookName, newSent))

    return processedCorpora # newSent


def buildLex():

    print(' --- start buildLex() ---')

    rawCorpora = getRawCorpus()
    
    processedCorpora = processRawCorporaStrings(rawCorpora)

    # Change don't to do not and tag
    #
    taggedCorporaLst = expandAndTagSents(processedCorpora)

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    untaggedCorpora = simpDB["untaggedCorpora"]
    taggedCorpora = simpDB["taggedCorpora"]

    # For now we will start fresh each time
    untaggedCorpora.drop()
    taggedCorpora.drop()

    for corpus in processedCorpora: 
        untaggedCorpora.insert_one({"bookName": corpus[0], "untaggedSentences": corpus[1]})

    for corpus in taggedCorporaLst:
        taggedCorpora.insert_one({"bookName": corpus[0], "taggedSentences": corpus[1]})
     
    print(' --- end buildLex() ---')
    return # taggedCorpus


def readCheckMongo():
    mdb = connectMongo()
    simpDB = mdb["simp"]
    #untaggedCorpora = simpDB["untaggedCorpora"]
    taggedCorpora = simpDB["taggedCorpora"]

    cursorLst = list(taggedCorpora.find({}))

    for c in cursorLst:
        print(c)



    return
#
#
#
if __name__ == "__main__":

    print('Start: processRawCorpora (__main__)')
    buildLex()

    readCheckMongo()
    
    print('End: processRawCorpora (__main__)')  
