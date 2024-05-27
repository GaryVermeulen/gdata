#
# processRawCorpus.py
#
#

import os
import sys
import string

import spacy # spacy is a pig

from commonConfig import nnp, prp
from commonConfig import very_simple_contractions
from commonConfig import validTags
from commonUtils import connectMongo

nlp = spacy.load("en_core_web_sm") # lg has best accuracy

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


def processRawCorporaStrings(rawCorpora):

    bookName = ''
    rawCorpusString = ''
    processedCorpora = []

    print('Processing strings...')

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

        # Remove leading spaces and --
        #for sent in newSent:
        #    sent = sent.lstrip()
        #    if len(sent) > 1:
        #        if sent[0] == '-' and sent[1] == '-':
        #            sent = sent[2:]
        #    tmpLst.append(sent)

        # remove dash at end of word: word1- word2
        #newSent.clear()
        #for sent in tmpLst:
        #    tmpSent = ''
        #    tmpSentLst = sent.split()
        #    for word in tmpSentLst:
        #        if word[-1] == '-':
        #            word = word[:-1]
        #        if tmpSent == '':
        #            tmpSent = tmpSent + word
        #        else:
        #            tmpSent = tmpSent + ' ' + word
        #    newSent.append(tmpSent)

        # Replace dash with space: word1-word2
        #tmpLst.clear()
        #for sent in newSent:
        #    newS = ""
        #    newS = sent.replace("-", "=")
        #    if newSent == "":
        #        tmpLst.append(sent)
        #    else:
        #        tmpLst.append(newS)

            #    –
            #    - 

        # Remove single char sentences and double spaces
        #newSent.clear()
        #for sent in tmpLst:
        #    sent = sent.replace("  ", " ")
        #    if len(sent) > 1:
        #        newSent.append(sent)

            

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


def expandAndTag(processedCorpora):

    expandedCorpora = []

    for corpus in processedCorpora:
        bookName = corpus[0]
        bookSents = corpus[1]

        print('bookName: ', bookName)

        newBookSents = []

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

            
            # Remove (for now) hyphens    
            noHyphens = removeHyphens(expandedSentence)

            # Tag expanded sentence
            #doc = nlp(' '.join(expandedSentence))
            doc = nlp(' '.join(noHyphens))

            tagSent = []
            for token in doc:
                tmpToken = ((str(token.text)), (str(token.tag_)))
                tagSent.append(tmpToken)

            # Fix for had/would 
            idx = 0
            if not verySimple:
                newTagSent = []
                for w in tagSent:
                    if w[0] == "'d":
                        if tagSent[idx + 1][1] in [rb, vbn, jj]:
                            w = ("had", vbd)
                        else:
                            w = ("would", "MD")
                        
                    newTagSent.append(w)
                    idx += 1
                    
                tagSent = newTagSent

            # Check for tagging errors
            # Tagging errors: ['Moebus', 'NNP'] and '['Moebus', 'NN'], and ['goldfish', 'JJ']
            #
            # For the goldfish problem check inflectionsCol and simpDict
            correctedTagSent = correctTagSent(tagSent)

            print('---TOP--')
            print('correctedTagSent:')
            print(correctedTagSent)
            print('---BOT--')
#            newBookSents.append(expandedSentence)
            newBookSents.append(tagSent)

#        print('newBookSents: ', newBookSents)
#        for w in newBookSents:
#            print(w)
#
#        print('---')

        expandedCorpora.append((bookName, newBookSents))


    return expandedCorpora


def correctTagSent(tagSent):

    correctedTagSent = []
    

    print('tagSent:')
    print(tagSent)

    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflectionsCol"]
    simpDict = simpDB["simpDict"]

    for taggedWord in tagSent:
        tagOK = False
        word = taggedWord[0]
        tag = taggedWord[1]

        capWord = word.capitalize() # For search simpDict

        myQuery = {"word": capWord}

        # First, check simpDict
        dictDoc = []
        myDoc = simpDict.find(myQuery)
        for x in myDoc:
            xWord = x["word"]
            xTag = x["tag"]
            dictDoc.append([xWord, xTag])

        lowWord = word.lower()
        myQuery = {"word": lowWord}
        # Now check inflectionsCol
        inflecDoc = []
        inflecs = ''
        myDoc = inflectionsCol.find(myQuery)
        for i in myDoc:
            iWord = i["word"]
            iTag = i["tag"]
            inflecs = i["inflections"]
            inflecDoc.append([iWord, iTag])


        print('dictDoc:')
        print(dictDoc)
        print('inflecDoc:')
        print(inflecDoc)
        print('taggedWord:')
        print(taggedWord)

        if tag in validTags: # Skip over odd punctuation tags
            print('Searching dictDoc')
            for dictWord in dictDoc:
                if dictWord[1] == taggedWord[1]:
                    tagOK = True
                    break
            
            if not tagOK:
                print('Searching inflecDoc')
                for inflecWord in inflecDoc:
                    if inflecWord[1] == taggedWord[1]:
                        tagOK = True
                        break
            
            if not tagOK:
                print('Searching inflections in inflecDoc')
                print(inflecs)
                for i in inflecs:
                    if i == word:
                        print('word found in inflections: ', i)
                        print('inflection base word tag: ', iTag)
        else:
            tagOK = True # Free pass

        

        if tagOK:
            print('OK')
        else:
            print('NOT OK')

        print('---')

            

    print('--------')

            
#            if xTag == tag:
#                print('tag ok')
#                correctedTagSent.append(word)
#            else:
#                print("Replacing tag: {} with simpDict tag: {} For word: {}".format(tag, xTag, word))
#                correctedTagSent.append([word, xTag])


    return correctedTagSent
    


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

    processedCorpora = []

    print(' --- start buildLex() ---')

    rawCorpora = getRawCorpus()

#    for corpus in rawCorpora:
#        bookName = corpus[0]
#        bookText = corpus[1]
#
#        print('bookName: ', bookName)
#        print('bookText::')
#        print(bookText)
#    
#        print("---")
    
    processedCorpora = processRawCorporaStrings(rawCorpora)

#    print('after processRawCorporaStrings')
#    print(type(processedCorpora))
#    print(len(processedCorpora))
#
#    for corpus in processedCorpora:
#        for c in corpus:
#            bookName = corpus[0]
#            bookText = corpus[1]
#
#            print('bookName: ', bookName)
#            print('bookText: ')
#            print(type(bookText))
#            print(len(bookText))
#
#            for s in bookText:
#                print(s)


    expandedCorpora = expandAndTag(processedCorpora)

    print('after expandContractions...')
    print(type(expandedCorpora))
    print(len(expandedCorpora))
    for corpus in expandedCorpora:
        for c in corpus:
            bookName = corpus[0]
            bookText = corpus[1]
#
            print('bookName: ', bookName)
            print('bookText: ')
            print(type(bookText))
            print(len(bookText))
            for s in bookText:
                print(s)
#
            print('---')
#            print(bookText)

#    sys.exit("TEMP EXIT")

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

    for corpus in expandedCorpora: # Make string to save space?
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
