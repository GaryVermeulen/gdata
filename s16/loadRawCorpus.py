#
# loadRawCorpus.py
#
# New: 11/10/24
#

import os
import string
import pickle
import spacy
import warnings

from commonConfig import very_simple_contractions
from commonConfig import Sentence

debug = False

nlp = spacy.load("en_core_web_lg")

def getRawCorpus():
    # Read the raw corpus file(s)
    corpus = []
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/inputCorpus'
    dirList = os.listdir(dataPath)

    #print('Reading input file(s)...')

    # Read corpus input--should only be one file!
    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r', encoding="utf8") as f: # Added , encoding="utf8" for Win PC
            while (line := f.readline()):
                corpusStr += line
        f.close()
        bookName = inFile[: -4]
        corpus.append((bookName, corpusStr))
        corpusStr = ''
        
    #print('Input corpus read.')

    return corpus


def processRawCorpusStrings(rawCorpus):
    # Take string and break into sentences

    bookName = ''
    rawCorpusString = ''
    processedCorpus = []

    #print('Processing strings into sentences...')

    for corpus in rawCorpus:

        tmpLst = []
        tmpSent = ''
        newSentences = []

        startQuote = False
        lastCharSentTerm = False

        bookName = corpus[0]
        rawCorpusString = corpus[1]

        #print('bookName: ', bookName)

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
        
        processedCorpus.append((bookName, newSentences))

    #print('Strings processed.')
    return processedCorpus # newSent


def expandContractions(processedCorpus):
    # Go through list(s) and expand contractions

    #print('start: expandContractions...')

    expandedCorpus = []

    for corpus in processedCorpus:
        bookName = corpus[0]
        bookSents = corpus[1]

        #print('bookName: ', bookName)

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
                    if word.find("'") != -1: 
                        # Doesn't handle idioms such as: someone's, or possessives ex: Jimmy's
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
            
        expandedCorpus.append((bookName, newBookSents))


    #print('Completed: expandContractions.')
    return expandedCorpus


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


def tagCorpus(expandedCorpus):

    #print('start: tagCorpus...')

    taggedCorpus = []
    OBJECT_DEPS = ["dobj", "dative", "attr", "oprd"]
    SUBJECT_DEPS = ["nsubj", "nsubjpass", "csubj", "agent", "expl"]

    for corpus in expandedCorpus:
        bookName = corpus[0]
        bookSents = corpus[1]

        #print('bookName: ', bookName)

        taggedBookSents = []

        for sent in bookSents:
            taggedSentLong = []
            taggedSentShort = []
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
                hdep = token.head.dep_

                warnings.filterwarnings("error")
                try:
                    dep_exp = spacy.explain(token.dep_)
                except UserWarning as w:
                    #print('*** Something is wrong: ', w)
                    dep_exp = "UNKNOWN"
                warnings.resetwarnings()

                taggedWordLong = {
                    "word": word,
                    "lemma": lemma,
                    "pos": pos,
                    "tag": tag,
                    "is_stop": is_stop,
                    "dep": dep,
                    "hdep": hdep,
                    "dep_exp": dep_exp
                }

                taggedWordShort = {
                    "word": word,
                    "pos": pos,
                    "tag": tag
                }


                # grab the verbs
                #if token.pos_ == "VERB":
                #    #verb.append(token.text)
                #    verb.append(taggedWordLong)
                #    
                # is this the object?
                #if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
                #    obj.append(taggedWordLong)
                #
                #    #obj.append(token.text)
                #    #print('token.text?: ', token.text)
                #    #print('token.dep_?: ', token.dep_)
                #    #print('token.head.dep_?: ', token.head.dep_)
                #    #print('OBJECT_DEPS?: ', OBJECT_DEPS)
                #    
                # is this the subject?
                #if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
                #    sub.append(taggedWordLong)
                #
                #    #sub.append(token.text)
                #    #print('token.text?: ', token.text)
                #    #print('token.dep_?: ', token.dep_)
                #    #print('token.head.dep_?: ', token.head.dep_)
                #    #rint('SUBJECT_DEPS?: ', SUBJECT_DEPS)

                taggedSentLong.append(taggedWordLong)
                taggedSentShort.append(taggedWordShort)

                #sentObj = Sentence(noHyphens, taggedSentShort, taggedSentLong, [], "TYPE UNK", sub, verb, obj)
                sentObj = Sentence(noHyphens, taggedSentShort, taggedSentLong, [], "TYPE UNK", [], [], [])

            taggedBookSents.append(sentObj)

        taggedCorpus.append((bookName, taggedBookSents))

    #print('completed: tagCorpus.')
    return taggedCorpus

def loadAndProcess():

    rawCorpus = getRawCorpus()

    if debug:
        print('raw ----------')
        print(len(rawCorpus))
        print(type(rawCorpus))
        for i in rawCorpus:
            print(i)
        print('----------')

    processedCorpus = processRawCorpusStrings(rawCorpus)

    if debug:
        print('processed ----------')
        print(len(processedCorpus))
        print(type(processedCorpus))
        for i in processedCorpus:
            print(i)
        print('----------')

    expandedCorpus = expandContractions(processedCorpus)

    if debug:
        print('expanded ----------')
        print(len(expandedCorpus))
        print(type(expandedCorpus))
        for i in expandedCorpus:
            print("Book Name: ", i[0])
            for j in i[1]:
                print(j)
        print('Saving untagged data to pickle...')
        with open("pickleJar/b4tag.p", "wb") as f:
            pickle.dump(expandedCorpus, f)
        f.close()
        print('Saved: expandedCorpus to pickle.')
        print('----------')

    taggedCorpus = tagCorpus(expandedCorpus)
        
    if debug:
        cnt = 0
        print('tagged ----------')
        print(len(taggedCorpus))
        print(type(taggedCorpus))
        for i in taggedCorpus:
            print("Book Name: ", i[0])
            for j in i[1]:
                cnt += 1
                print('--- {} ---'.format(cnt))
            #    print(j)
                j.printAll()
        print('Saving tagged data to pickle...')
        with open("pickleJar/tagged.p", "wb") as f:
            pickle.dump(taggedCorpus, f)
        f.close()
        print('Saved: taggedCorpus to pickle.')    

    return taggedCorpus 


if __name__ == "__main__":

    print("START loadRawCorpus (main)...")

    taggedCorpus = loadAndProcess()

    print("++++++++++++++++")
    debug = True
    if debug:
        cnt = 0
        print(len(taggedCorpus))
        print(type(taggedCorpus))
        for i in taggedCorpus:
            print("Book Name: ", i[0])
            for j in i[1]:
                cnt += 1
                print('--- {} ---'.format(cnt))
            #    print(j)
                j.printAll()

    
    print("END loadRawCorpus (main)...")
