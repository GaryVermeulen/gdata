#
# processCorpus.py
#
#

import os
import spacy # spacy is a pig

from commonConfig import simple_contractions
from commonConfig import verbose
from commonConfig import common2LetterWords
from commonConfig import nnp

from commonUtils import connectMongo


nlp = spacy.load("en_core_web_sm") # lg has best accuracy



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
                tmp = line.split()
                startSentList.append(tmp)
    f.close()

    return startSentList


def expandSents(corpusSents):

    expandedSents = []
    wordCnt = 0
    sentCnt = 0

    for s in corpusSents:
        sentCnt += 1
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
                    print('Line {}: {}'.format(sentCnt, s))
                continue
                        
            clean_word = ''.join(filter(str.isalnum, w))

            if len(clean_word) > 0:
                expandedSentence.append(clean_word)
                
        expandedSents.append(expandedSentence)    

    return expandedSents


def buildTaggedBoW(taggedCorpus):

    # taggedBoW = loadStarterDictionary()
    # No longer using StarterDictionary
    taggedBoW = []

    for s in taggedCorpus:
        for w in s:
            if w not in taggedBoW:
                if w[1] == nnp:
                    taggedBoW.append(w)
                else:
                    taggedBoW.append((w[0].lower(),w[1]))

    taggedBoW = list(dict.fromkeys(taggedBoW))

    return(taggedBoW)


def processRawCorpusString(rawCorpusString):

    tmpLst = []
    tmpSent = ''
    newSent = []

    for char in rawCorpusString:
        if char == '.':     # We'll need to handle Mr. & Mrs.
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

    return newSent


def normalizeCase(s):
    # Adjust the case of words in an input sentence to our liking
    s_norm = []
    wordPosition = 0
    for w in s:
        wordPosition += 1
        if wordPosition == 1: # First word in an English sentence should be capitalized
            if len(w) == 2:
                if w in common2LetterWords: # May not catch some strange stuff
                    w = w.capitalize()
                    s_norm.append(w)
                    continue
                else: # Assuming an initial nickname "AJ"
                    s_norm.append(w)
                    continue
            else:
                w = w.capitalize()
                s_norm.append(w)
                continue

        if wordPosition > 1: # Is the whole word upper case (except I)? If so make all lower
            if w.isupper(): # All upper
                if w in ['I']:
                    s_norm.append(w)
                    continue
                else:
                    if len(w) == 2: # Attempt to handle initial nicknames "AJ"
                        if w.lower() in common2LetterWords: # Most likey not an initial nickname
                            w = w.lower()
                            s_norm.append(w)
                            continue
                        else: # Assuming an initial nickname "AJ"
                            s_norm.append(w)
                            continue
                    else:
                        w = w.lower()
                        s_norm.append(w)
                        continue
            else: # Mixed or first char upper
                if w == 'i':
                    s_norm.append(w.upper())
                    continue
                else:
                    if len(w) == 2: # Attempt to handle initial nicknames "AJ"
                        if w in common2LetterWords: # Most likey not an initial nickname
                            w = w.lower()
                            s_norm.append(w)
                            continue
                        else: # Assuming an initial nickname "AJ"
                            s_norm.append(w)
                            continue
                    else: # May need to dig deeper here...~?
                        s_norm.append(w)

        if wordPosition == len(s):
            wordPostion = 0

    return s_norm


def buildLex():

    cnt = 0

    print(' --- start buildLex() ---')

    rawCorpusString = getRawCorpus()
    processedCorpus = processRawCorpusString(rawCorpusString)
    print('Loaded and processed {} sentences from corpus.'.format(len(processedCorpus)))

    # Change don't to do not
    expandedCorpusSents = expandSents(processedCorpus) # Change don't  to do not    
    print('Expanded sentences: ', len(expandedCorpusSents))
          
    # Add starter sentences
    startSentList = loadStarterSentences()
    print('Loaded {} starter sentences.'.format(len(startSentList)))
          
    completeUntaggedCorpus = expandedCorpusSents + startSentList
    completeUntaggedCorpus = [x for x in completeUntaggedCorpus if not len(x) < 1] # Remove empty entries []
    print('Processed {} sentences.'.format(len(completeUntaggedCorpus)))        
    
    # Build/convert into tagged sentences
    completeTaggedCorpus = []
    for s in completeUntaggedCorpus:

        s_norm = normalizeCase(s) # Normal/adjust case

        if len(s_norm) > 0: # Just to make sure
            doc = nlp(' '.join(s_norm))
            tagSent = []
            for token in doc:
                tmpToken = ((str(token.text)), (str(token.tag_)))
                tagSent.append(tmpToken)
            completeTaggedCorpus.append(tagSent)

    print('Tagged {} sentences.'.format(len(completeTaggedCorpus)))

    taggedBoW = buildTaggedBoW(completeTaggedCorpus)
    print('Created Tagged Bag Of Words: ', len(taggedBoW))

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    untaggedCorpus = simpDB["untaggedCorpus"]
    taggedCorpus = simpDB["taggedCorpus"]
    tagged_BoW = simpDB["taggedBoW"]

    # For now we will start fresh each time
    untaggedCorpus.drop()
    taggedCorpus.drop()
    tagged_BoW.drop()

    for s in completeUntaggedCorpus:
        untaggedCorpus.insert_one({"untaggedSentence": s})
    
    for s in completeTaggedCorpus:
        
        tmpSent = []
        for w in s:
            tmpSent.append({"word": w[0], "tag": w[1]})
        
        taggedCorpus.insert_one({"taggedSentence": tmpSent})
        
        #taggedCorpus.insert_one({"taggedSentence": s})

    for t in taggedBoW:
        tagged_BoW.insert_one({"word": t[0], "tag":t[1]})
        
    print(' --- end buildLex() ---')
    return 'Built MongoDB simp w/collections: untaggedCoprus, taggedCoprus, taggedBoW'


#
#
#
if __name__ == "__main__":

    print('Start: processCorpus (__main__): buildLex')
    print(buildLex())
    print('End: processCorpus (__main__): buildLex')  
