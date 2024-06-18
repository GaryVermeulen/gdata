#
# processRawCorpus.py
#
#

import os
import sys
import string
import warnings


import spacy # spacy is a pig

from commonConfig import Sentence
from commonConfig import very_simple_contractions
from commonUtils import connectMongo

import pickle

pickleFile = 'data/processedCorpora.p'
pf = 'data/untaggedCorpora.p'

#nlp = spacy.load("en_core_web_sm") # lg has best accuracy
nlp = spacy.load("en_core_web_lg")

def getRawCorpus():
    # Read the raw corpus file(s)
    corpora = []
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

    print('Reading input file(s)...')

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


def processRawCorporaStrings(rawCorpora):
    # Take string and break into sentences

    bookName = ''
    rawCorpusString = ''
    processedCorpora = []

    print('Processing strings into sentences...')

    for corpus in rawCorpora:

        tmpLst = []
        tmpSent = ''
        newSentences = []

        startQuote = False
        lastCharSentTerm = False

        bookName = corpus[0]
        rawCorpusString = corpus[1]

        print('bookName: ', bookName)

        for char in rawCorpusString:
            if char == '.':     # We'll need to handle Mr. & Mrs.
                if startQuote:
                    tmpSent = tmpSent + '.'
                else:
                    newSentences.append(tmpSent + '.')
                    tmpSent = ''
                lastCharSentTerm = True
            elif char == ',':   #
                tmpSent = tmpSent + ',' 
                lastCharDot = False
            elif char == '?':   # We'll need to handle multiple ???
                if startQuote:
                    tmpSent = tmpSent + '?'
                else:
                    newSentences.append(tmpSent + '?')
                    tmpSent = ''
                lastCharSentTerm = True
            elif char == '!':   # We'll need to handle multiple !!!
                if startQuote:
                    tmpSent = tmpSent + '!'
                else:
                    newSentences.append(tmpSent + '!')
                    tmpSent = ''
                lastCharSentTerm = True
            elif char == ';':   # We'll need to handle multiple ;;;
                newSentences.append(tmpSent + '; ')
                tmpSent = ''
                lastCharSentTerm = True
            elif char == '"':   # Skip " chr 34
                #continue
                if lastCharSentTerm:
                    newSentences.append(tmpSent + '"')
                    tmpSent = ''
                else:
                    tmpSent = tmpSent + '"'
                startQuote = not startQuote
                lastCharSentTerm = False
            elif char == '*':   # Skip * chr 42
                continue
            elif char == '(':   # Skip ( chr 40
                continue
            elif char == ')':   # Skip ) chr 41
                continue
            elif char == chr(8216): # Replace unicode left quotation
                tmpSent = tmpSent + "'"
                lastCharSentTerm = False
            elif char == chr(8217): # Repalce unicode right quotation
                tmpSent = tmpSent + "'"
                lastCharSentTerm = False
            elif char == chr(8220): # Unicode left double quotation
                if lastCharSentTerm:
                    newSentences.append(tmpSent + '"')
                    tmpSent = ''
                else:
                    tmpSent = tmpSent + '"'
                startQuote = not startQuote
                lastCharSentTerm = False
            elif char == chr(8221): # Skip unicode right double quotation
                if lastCharSentTerm:
                    newSentences.append(tmpSent + '"')
                    tmpSent = ''
                else:
                    tmpSent = tmpSent + '"'
                startQuote = not startQuote
                lastCharSentTerm = False
            elif char == '\n':
                tmpSent = tmpSent + ' '
                lastCharSentTerm = False
            elif char == '–':
                tmpSent = tmpSent + '-'
                lastCharSentTerm = False
            else:
                tmpSent = tmpSent + char
                lastCharSentTerm = False    

        # Remove leading and double spaces
        tmpLst = []
        for sent in newSentences:
            sent = sent.lstrip()
            sent = sent.replace("  ", " ")
            if len(sent) > 1:
                tmpLst.append(sent)

        newSentences = tmpLst

        # Correct periods with no space
        tmpLst = []
        nextChar = ''
        
        for sent in newSentences:   
            newSent = ''
            charCnt = 0
            
            for char in sent:
                if len(sent) > (charCnt + 1):
                    nextChar = sent[charCnt + 1]
                
                if char == ".":
                    if nextChar in string.ascii_lowercase:
                        newSent = newSent + char + ' '
                    elif nextChar in string.ascii_uppercase:
                        newSent = newSent + char + ' '
                    else:
                        newSent = newSent + char
                elif char == ",":
                    if nextChar in string.ascii_lowercase:
                        newSent = newSent + char + ' '
                    elif nextChar in string.ascii_uppercase:
                        newSent = newSent + char + ' '
                    else:
                        newSent = newSent + char
                else:
                    newSent = newSent + char
                    
                charCnt += 1
            tmpLst.append(newSent)
            
        newSentences = tmpLst
        
        processedCorpora.append((bookName, newSentences))

    print('Strings processed.')
    return processedCorpora # newSent


def expandContractions(processedCorpora):
    # Go through list(s) and expand contractions

    print('start: expandContractions...')

    expandedCorpora = []

    for corpus in processedCorpora:
        bookName = corpus[0]
        bookSents = corpus[1]

        print('bookName: ', bookName)

        newBookSents = []
        untaggedBook = []

        # Split into word tokens and isolate punctuation except "'"
        for sent in bookSents:
            words = sent.split()

            # Work the first char of the word
            newWords = []
            for word in words:
                if len(word) > 1: 
                    if word[0] == '"':
                        newWords.append(word[0])
                        newWords.append(word[1:])
                    else:
                        newWords.append(word)
                else:
                    newWords.append(word)
            
            # Work the last char of the word
            tmpWords = newWords.copy()
            newWords = []
            for word in tmpWords:
                tmpWord = ''
                if word[-1] == ',':
                    newWords.append(word[:len(word) - 1])
                    newWords.append(',')
                elif word[-1] == '"':
                    if len(word) > 1:
                        if word[-2] in ['.', ',', '?', '!']:
                            newWords.append(word[:len(word) - 2])
                            if word[-2] == '.':
                                newWords.append('.')
                                newWords.append('"')
                            elif word[-2] == ',':
                                newWords.append(',')
                                newWords.append('"')
                            elif word[-2] == '?':
                                newWords.append('?')
                                newWords.append('"')
                            elif word[-2] == '!':
                                newWords.append('!')
                                newWords.append('"')
                        else:
                            newWords.append(word[:len(word) - 1])
                            newWords.append('"')
                    else:
                        newWords.append(word)
                elif word[-1] == '.':
                    newWords.append(word[:len(word) - 1])
                    newWords.append('.')
                elif word[-1] == '!':
                    newWords.append(word[:len(word) - 1])
                    newWords.append('!')
                elif word[-1] == '?':
                    newWords.append(word[:len(word) - 1])
                    newWords.append('?')
                else:
                    newWords.append(word)

                # Expand contractions
                verySimple = False
                expandedSentence = []
                for word in newWords:
                    if word.find("'") != -1: # Doesn't handle idioms such as: someone's
                        if word in very_simple_contractions.keys():
                            result = very_simple_contractions[word]
                            resultList = result.split()
                            verySimple = True
                            for r in resultList:
                                expandedSentence.append(r)
                        else:
                            verySimple = False
                            expandedSentence.append(word)

                    else:
                        expandedSentence.append(word)

            newBookSents.append(expandedSentence)
            
        expandedCorpora.append((bookName, newBookSents))


    print('Completed: expandContractions.')
    return expandedCorpora


def tagCorpora(expandedCorpora):

    print('start: tagCorpora...')

    taggedCorpora = []
    OBJECT_DEPS = {"dobj", "dative", "attr", "oprd"}
    SUBJECT_DEPS = {"nsubj", "nsubjpass", "csubj", "agent", "expl"}

    for corpus in expandedCorpora:
        bookName = corpus[0]
        bookSents = corpus[1]

        print('bookName: ', bookName)

        taggedBookSents = []

        for sent in bookSents:
            taggedSent = []
            sub = []
            obj = []
            verb = []
            # Remove (for now) hyphens e.g. D-E-L-I-C-I-O-U-S to DELICIOUS  
            noHyphens = removeHyphens(sent)

            doc = nlp(' '.join(noHyphens))

            # Extract minimal info to keep size down
            # This is most likely change
            # word.pos_, word.tag_, word.dep_, word.shape_, word.is_alpha, word.is_stop            
            for token in doc:
                word = token.text
                lemma = token.lemma_
                pos = token.pos_
                tag = token.tag_
                is_stop = token.is_stop
                dep = token.dep_

                warnings.filterwarnings("error")
                try:
                    dep_exp = spacy.explain(token.dep_)
                except UserWarning as w:
                    #print('*** Something is wrong: ', w)
                    dep_exp = "UNKNOWN"
                warnings.resetwarnings()

                # grab the verbs
                if token.pos_ == "VERB":
                    verb.append(token.text)
                # is this the object?
                if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
                    obj.append(token.text)
                # is this the subject?
                if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
                    sub.append(token.text)

                taggedWord = {
                    "word": word,
                    "lemma": lemma,
                    "pos": pos,
                    "tag": tag,
                    "is_stop": is_stop,
                    "dep": dep,
                    "dep_exp": dep_exp
                }

                taggedSent.append(taggedWord)

                sentObj = Sentence(noHyphens, taggedSent, "TYPE", sub, verb, obj)

            taggedBookSents.append(sentObj)

        taggedCorpora.append((bookName, taggedBookSents))

    print('completed: tagCorpora.')
    return taggedCorpora


def removeHyphens(expandedSentence):

    noHyphens = []

    for word in expandedSentence:
        cnt = word.count('-')
        index = -1

        if len(word) > 1:
            if cnt > 1:
                
                try:
                    index = word.index('-')
                except ValueError:
                    index = 0
                
                if index >= 1: # Not looking for: -H  
                    # Pretty sure we have a hyphenated word, so remove hyphens...
                    uWord = ''
                    for char in word:
                        if char != '-':
                            uWord = uWord + char

                    noHyphens.append(uWord)
            else:
                noHyphens.append(word)
        else:
            noHyphens.append(word)
            
    return noHyphens


def buildLex():

    print(' --- start buildLex() ---')

    rawCorpora = getRawCorpus()
    
    processedCorpora = processRawCorporaStrings(rawCorpora)

    expandedCorpora = expandContractions(processedCorpora)

    taggedCorpora = tagCorpora(expandedCorpora)

    print('dumping taggedCorpora to pickle...')
    with open(pickleFile, "wb") as f:
        pickle.dump(taggedCorpora, f)
    
    print('------------')

    display = input('Display new input <Y/n>? ')

    if display in ['Y', 'y']:
        for corpus in taggedCorpora:
            print('corpus type: ', type(corpus))
            print('corpus len: ', len(corpus))
            print('corpus:')
            #print(corpus)
            print('------')
            print('bookName: ', corpus[0])
            print('sents?')
            print(type(corpus[1]))
            print(len(corpus[1]))
            for sents in corpus[1]:
                print(type(sents))
                sents.printAll()
     
    print(' --- end buildLex() ---')
    return taggedCorpora


#
#
#
if __name__ == "__main__":

    print('Start: processRawCorpora (__main__)')
    taggedCorpora = buildLex()

    print('taggedCorpora type: ', type(taggedCorpora))
    print('taggedCorpora len: ', len(taggedCorpora))
    print('End: processRawCorpora (__main__)')  
