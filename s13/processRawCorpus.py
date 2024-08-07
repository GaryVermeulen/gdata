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


def loadStarterDictionary():
    # Starter tagged BoW
    
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

    with open('data/starterSentences2.txt', 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.strip()
                line = line.replace('.', '')
                
                startSentList.append(line)
    f.close()

    return startSentList


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


def buildTaggedBoW(taggedCorpus):

    # taggedBoW = loadStarterDictionary()
    # No longer using StarterDictionary
    taggedBoW = []

    for s in taggedCorpus:
        for w in s:
            if w not in taggedBoW:
                if w[1] == nnp:
                    taggedBoW.append(w)
                elif w[1] == prp:
                    if w[0] == "I":
                        taggedBoW.append(w)
                    else:
                        taggedBoW.append((w[0].lower(),w[1]))
                else:
                    taggedBoW.append((w[0].lower(),w[1]))

    taggedBoW = list(dict.fromkeys(taggedBoW))

    return(taggedBoW)


def processRawCorpusString(rawCorpora):

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

    cnt = 0

    print(' --- start buildLex() ---')

    rawCorpora = getRawCorpus()

#    print(type(rawCorpora))
#    print(len(rawCorpora))
#    for i in rawCorpora:
#        print(i)
    
    processedCorpora = processRawCorpusString(rawCorpora)
    
#    print(type(processedCorpora))
#    print(len(processedCorpora))
#    for i in processedCorpora:
#        print(i)
    
#    print('Loaded and processed {} sentences from corpus.'.format(len(processedCorpus)))

    # Add starter sentences
#    startSentLis{} starter sentences.'.format(len(startSentList)))

    # Merge and remove empty entries
#    completeUntaggedCorpus = processedCorpus + startSentList
#    completeUntaggedCorpus = [x for x in completeUntaggedCorpus if not len(x) < 1] # Remove empty entries []
#    print('Loaded {} sentences.'.format(len(completeUntaggedCorpus)))

    # Change don't to do not and tag
    #
    taggedCorporaLst = expandAndTagSents(processedCorpora)
    
#    print(type(taggedCorpora))
#    print(len(taggedCorpora))
#    for i in taggedCorporaLst:
#        print('###: \n', i)
    
    
#    print('Expanded tagged sentences: ', len(completeTaggedCorpus))

    # Create a tagged BoW's
#    taggedBoW = buildTaggedBoW(completeTaggedCorpus)
#    print('Created Tagged Bag Of Words: ', len(taggedBoW))

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    untaggedCorpora = simpDB["untaggedCorpora"]
    taggedCorpora = simpDB["taggedCorpora"]
#    tagged_BoW = simpDB["taggedBoW"]

    # For now we will start fresh each time
    untaggedCorpora.drop()
    taggedCorpora.drop()
#    tagged_BoW.drop()

    for corpus in processedCorpora: 
        untaggedCorpora.insert_one({"bookName": corpus[0], "untaggedSentences": corpus[1]})

    for corpus in taggedCorporaLst:
        taggedCorpora.insert_one({"bookName": corpus[0], "taggedSentences": corpus[1]})
#        print('bookName: ', corpus[0])
#        print('sents   : ', corpus[1])
#        for sents in corpus[1]:
#            print(sents)

        
        
#    for s in completeTaggedCorpus:      
#        tmpSent = []
#        for w in s:
#            tmpSent.append({"word": w[0], "tag": w[1]})
        
#        taggedCorpus.insert_one({"taggedSentence": tmpSent})

#    for t in taggedBoW:
#        tagged_BoW.insert_one({"word": t[0], "tag":t[1]})
     
    print(' --- end buildLex() ---')
    return [] # taggedCorpus



#
#
#
if __name__ == "__main__":

    print('Start: processRawCorpus (__main__)')
    taggedCorpus = buildLex()

#    res = input("Assimilate <Y/N>? ")
#
#    if res in ['y', 'Y']:
#        # Process taggedCorpus for knowledge
#        assimilate(taggedCorpus, None)
    
    print('End: processRawCorpus (__main__)')  
