#
# processRawCorpus.py
#
#

import os
import sys

from commonConfig import nnp, prp
from commonUtils import connectMongo
from commonConfig import very_simple_contractions

from expandAndTag import expandAndTag

import nltk
from nltk.tokenize import word_tokenize



def getRawCorpus():
    # Read the raw corpus file(s)
    corpora = []
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

    print('Reading input...')

    # Read corpus input
    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r', encoding="utf8") as f: # Added , encoding="utf8" for Win PC
            while (line := f.readline()):
                corpusStr += line
        f.close()
        bookName = inFile[: -4]
        corpora.append((bookName, corpusStr))
        corpusStr = ''

    print('Input read.')

    return corpora


def expandAndTagSents(processedCorpora):

    taggedCorpora = []
    bookName = ''
    corpusStrings = []

    print('expandAndTag', end = '')

    for corpus in processedCorpora:

        bookName = corpus[0]
        completeUntaggedCorpus = corpus[1]
        expandedSents = []
        sentCnt = 0
        print('\n   processing: ', bookName)

        for s in completeUntaggedCorpus:
            sentCnt += 1
            expandedSentence = []

            expandedSentence = expandAndTag(s)       
            expandedSents.append(expandedSentence)
            print('.', end = '')
            
        taggedCorpora.append((bookName, expandedSents))

    print('\nexpandAndTag Completed.')

    return taggedCorpora # expandedSents


def sentenceParser(tokens):

    s = []
    tmp = []
    startQuote = False
    endQuote = False
    
    inQuote = False
    
    tokIndex = 0
    
    for tok in tokens:
        print("tok: ", tok)
        print("tmp: ", tmp)

        if tok == '"':
            tmp.append(tok)
            if inQuote:
                inQuote = False
            else:
                inQuote = True
        else:
            if tok in ['.', '?', '!']:
                if inQuote:
                    tmp.append(tok)
                else:
                    tmp.append(tok)
                    s.append(tmp)
                    print('2nd clear: ')
                    print(tmp)
                    tmp = []
            else:
                tmp.append(tok)
                
        print('s: ')
        print(s)

        
        tokIndex += 1

    print('+++')
    print(s)
    return s


def fixTokens(tokens):

    # Fix characters types and NLTK bug

    correctedTokens = []

    for tok in tokens:
        if '.' in tok: # This assumes simple two words joined by a '.'
            if len(tok) == 1:
                correctedTokens.append(tok)
            else:
                tokLst = tok.split('.')
                if len(tokLst) != 2:
                    print("Error with len of tokLst != 2")
                    print(tokLst)
                    
                correctedTokens.append(tokLst[0])
                correctedTokens.append('.')
                if len(tokLst[1]) > 0:
                    correctedTokens.append(tokLst[1])
        elif tok == chr(8216): # Replace unicode left quotation
            correctedTokens.append("'")
            #tmpSent = tmpSent + "'"
        elif tok == chr(8217): # Repalce unicode right quotation
            correctedTokens.append("'")
            #tmpSent = tmpSent + "'"
        else:
            correctedTokens.append(tok)


    return correctedTokens


def expandTokens(correctedTokens):

    expandedTokens = []
    lastTok = ''
    nextTok = ''
    tokenCnt = 0

    for tok in correctedTokens:

        print("tokenCnt: ", tokenCnt)
        print("tok:     ", tok)
        
        if len(correctedTokens) > (tokenCnt + 1):
            nextTok = correctedTokens[tokenCnt + 1] # What if the last token is a "'"?
        
        if tok == "'":
            print("lastTok: ", lastTok)  
            print("nextTok: ", nextTok)
            print("Possible contraction: ", lastTok + tok + nextTok)

            if (lastTok + tok + nextTok) in very_simple_contractions.keys():
                result = very_simple_contractions[lastTok + tok + nextTok]
                resultList = result.split()
                rCnt = 0
                for r in resultList:
                    if rCnt == 0:
                        expandedTokens[len(expandedTokens) -1] = r
                    else:
                        expandedTokens.append(r)
                    rCnt += 1
            else:   # Keep for later processing i.e. possive
                    # Also make back into one token
                    expandedTokens[len(expandedTokens) -1] = lastTok + tok # + nextTok
        else:
            if lastTok != "'":
                expandedTokens.append(tok)

        lastTok = tok
        tokenCnt += 1


    return expandedTokens


def buildLex():

    processedCorpora = []

    print(' --- start buildLex() ---')

    rawCorpora = getRawCorpus()

    for corpus in rawCorpora:
        bookName = corpus[0]
        bookText = corpus[1]

        print('bookName: ', bookName)
        print('bookText::')
        print(bookText)
    
        print("---")

        tokens = word_tokenize(bookText)

        # Unfortunately NLTK has some bugs and we can get incorrect tokens.
        # Example: 'responsibility.Then'
        # So we need to go through each token looking for a '.' within the token.
        #
        correctedTokens = fixTokens(tokens)

        #print("After fixTokens...")
        #print(type(correctedTokens))
        #print(len(correctedTokens))
        #print("---:")
        #print(correctedTokens)

        # My preference is to expand contractions
        #
        expanedTokens = expandTokens(correctedTokens)

        print("After expandTokens...")
        print(type(expanedTokens))
        print(len(expanedTokens))
        print("---:")

        for t in expanedTokens:
            print(t)

#        s = sentenceParser(tokens)
#        print(type(s))
#        print(len(s))
#        print("---:")
#        print(s)
#        
#
#        processedCorpora.append((bookName, tokens))
#
#    print("------")
#    print(type(processedCorpora))
#    print(len(processedCorpora))
#    print(processedCorpora)
    

    sys.exit("TEMP EXIT")
    
    ##processedCorpora = processRawCorporaStrings(rawCorpora)

    # Change don't to do not and tag
    #
    ##taggedCorporaLst = expandAndTagSents(processedCorpora)

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    untaggedCorpora = simpDB["untaggedCorpora"]
    taggedCorpora = simpDB["taggedCorpora"]

    drop = input('Drop exsiting collections <Y,n>? ')

    if drop in ['Y', 'y']:
        untaggedCorpora.drop()
        taggedCorpora.drop()
    else:
        # Check for duplicates
        newBookNames = []
        for corpus in processedCorpora: # Can be tagged or untagged, just checking book names
            newBookNames.append(corpus[0])

        for bookName in newBookNames:
            myQuery = {"bookName": bookName}
            myDoc = untaggedCorpora.find(myQuery)
            for x in myDoc:
                if x["bookName"] == bookName:
                    print("bookName: {} Exists (duplicate) Exiting...".format(bookName))
                    print(newBookNames)
                    sys.exit(0)

    for corpus in processedCorpora: 
        untaggedCorpora.insert_one({"bookName": corpus[0], "untaggedSentences": corpus[1]})

    for corpus in taggedCorporaLst: # Make string to save space?
        # Storing as a string saves space by about 50%
        ##sentsLst = []
        ##for sent in corpus[1]:
        ##    sentsLst.append(str(sent))
        ##taggedCorpora.insert_one({"bookName": corpus[0], "taggedSentences": sentsLst})

        # Retain data structure 
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
        print(c["bookName"])
        for s in c["taggedSentences"]:
            print(s)

    return
#
#
#
if __name__ == "__main__":

    print('Start: processRawCorpora (__main__)')
    buildLex()

    display = input('Display new input <Y/n>?')

    if display in ['Y', 'y']:
        readCheckMongo()
    
    print('End: processRawCorpora (__main__)')  