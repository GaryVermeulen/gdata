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
    dataPath = progPath + '/data/Corpus'
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

def getPickle(whichPickle):

    if whichPickle == 'ourDict.pkl':
        with open('data/ourDict.pkl', 'rb') as fp:
            ourDict = pickle.load(fp)
            print('Aunt Bee loaded ourDict.pkl')
        fp.close()
    elif whichPickle == 'newDict.pkl':
        with open('data/newDict.pkl', 'rb') as fp:
            ourDict = pickle.load(fp)
            print('Aunt Bee loaded newDict.pkl')
        fp.close()
    else:
        print('Unknown pickle problem: ', whichPickle)
        ourDict = None
        
    return ourDict


def verifyWords(expandedCorpusSents, whichPickle):

    wordsFound = []
    wordsNotFound = []

    print('verifyWords - whichPickle: ', whichPickle)

    ourDict = getPickle(whichPickle)

#    for key, value in ourDict.items():
#        print('key: {} value: {}'.format(key, value))
#    
#    print('input expandedCorpusSents: ', expandedCorpusSents)
    
    for s in expandedCorpusSents:
#        print('s: ', s)
        for w in s:
#            print('w: ', w)
            for key in ourDict:
                
                if w == key[:-2]:
#                    print('found: ', key[:-2])
                    wordsFound.append(w)
                else:
#                    print('not found: ', key[:-2])
                    wordsNotFound.append(w)
                            
    # Remove duplicates
    wordsFound = list(dict.fromkeys(wordsFound))
    wordsNotFound = list(dict.fromkeys(wordsNotFound))                     

    return wordsFound, wordsNotFound


def getWordsNotFound(wordsNotFound):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup

    newWords = []
    notFound = []
	
    print("Starting scrape for {} words".format(len(wordsNotFound)))
    for word in wordsNotFound:
        print('.', end='')

        req = Request(
            url = "http://www.dictionary.com/browse/" + word.strip() + "",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        try:
            htmlFile = urlopen(req).read()
            found = True
        except:
            notFound.append(word)
            found = False
            continue
          
        soup = BeautifulSoup(htmlFile, 'html.parser')
        soup1 = soup.find("meta", attrs={'name':'description'})

        try:
            soup1 = soup1.get_text()
            found = True
        except AttributeError:
            found = False
            continue
        if found:            
            soup2 =soup.find(class_="luna-pos")
            txt = soup2.get_text()
            pos = os.linesep.join([s for s in txt.splitlines() if s])
            pos = pos.replace(',', '')

            soup3 = soup.find("meta", attrs={'name':'description'})                        
            txt3 = str(soup3)
            txt4 = removeHTML(txt3) # Soup get_text not working or I can't figure it our :-(

        newWords.append(word + ';' + pos + ';' + txt4)
	
    print("\nScraping Completed.")

    return newWords, notFound


def removeHTML(txt):

    txt = txt.replace('<meta content="', '') # Start of htmp string
    txt = txt.replace('See additional meanings and similar words.', '')
    txt = txt.replace('See more.', '')
    txt = txt.replace('" name="description"/>', '')

    return txt


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


def getTag(pos):
    # Much more work needed here!
    posTag = 'Unknown'

    if pos == 'noun':
        posTag = 'NN'
    elif pos == 'plural noun':
        posTag = 'NNS'
    elif pos == 'pronoun':
        posTag = 'PRP'
    elif pos =='plural pronoun': # Not ready, so PRP for now
        posTag = 'PRP'
    elif pos == 'verb':
        posTag = 'VB'
    elif pos == 'verb (used with object)': # Not ready, so VB for now
        posTag = 'VB'
    elif pos == 'verb (used with object)': # Not ready, so VB for now
        posTag = 'VB'
    elif pos == 'auxiliary verb': # Not ready, so VB for now
        posTag = 'VB'
    elif pos == 'adjective':
        posTag = 'JJ'
    elif pos == 'adverb':
        posTag = 'RB'
    elif pos == 'preposition': 
        posTag = 'IN'           
    elif pos == 'conjunction': 
        posTag = 'CC'
    elif pos == 'interjection':
        posTag = 'UH'
    elif pos == 'definite article':
        posTag = 'DT'
        
    return posTag


def tagCorpus(expandedCorpusSents):

    taggedDocs = []

    nlp = spacy.load("en_core_web_lg") # Going for the best accuracy

    for sentence in expandedCorpusSents:
        strSentence = ' '.join(sentence)
#        print(strSentence)
#        if len(strSentence) > 10:
#            testSent = strSentence
        doc = nlp(strSentence)
#        print('doc: ', doc)
        tmpDoc = []
        for token in doc:            
#            print('token.text: ', token.text)    
#            print(f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
            tmpToken = ((str(token.text)), (str(token.tag_)))
            tmpDoc.append(tmpToken)

        taggedDocs.append(tmpDoc)

    return taggedDocs

def updateDict(newWords, taggedCorpus):
    # It is assumed these words are new (not in existing dict)
    # And that there one entry per list
    # newWords.append(word + ';' + pos + ';' + txt4)
    
    wordCount = 1
    oldDict = getPickle('ourDict.pkl')

    print('oldDict len: ', len(oldDict))

    for word in newWords:
        wordList = word.split(';')
        newWord = wordList[0]

        for s in taggedCorpus:
            for w in s:
                if w[0] == newWord:
                    newTag = w[1]

                    newWord_n = newWord + '_' + str(wordCount)
                    attributes = {'Word': newWord, 'Tag': newTag}
        oldDict.update({newWord_n: attributes})
        
    return oldDict



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
        for w in s:
            if w == "knowif":
                print('bad s: ', s)
    print('-' * 5)

    wordsFound, wordsNotFound = verifyWords(expandedCorpusSents, 'ourDict.pkl')

    print('wordsFound:')
    print(len(wordsFound))
    print(type(wordsFound))
    print('wordsNotFound:')
    print(len(wordsNotFound))
    print(type(wordsNotFound))

    newWords, notFound = getWordsNotFound(wordsNotFound)

    print('newWords:')
    print(len(newWords))
    print(type(newWords))
    print('notFound:')
    print(len(notFound))
    print(type(notFound))
    print('-' * 5)

    goodSents = rejectNotFound(expandedCorpusSents, notFound) # Drop sents with unknown words
    
    print('goodSents:')
    print(len(goodSents))
    print(type(goodSents))
    for s in goodSents:
        for w in s:
            if w == "knowif":
                print('bad s: ', s)
    print('-' * 5)    

    taggedCorpus = tagCorpus(goodSents)

    print('taggedCorpus:')
    print(len(taggedCorpus))
    print(type(taggedCorpus))
    for s in taggedCorpus:
        for token in s:
            if token[0] == "knowif":
                print(s)

    # Save cleaned corpus to pickle
    with open('data/taggedCorpus.pkl', 'wb') as fp:
        pickle.dump(taggedCorpus, fp)
        print('Aunt Bee made a taggedCorpus pickle')
    fp.close()

    print('-' * 5)                           
 

    # Save cleaned corpus to pickle
    with open('data/ourCorpus.pkl', 'wb') as fp:
        pickle.dump(goodSents, fp)
        print('Aunt Bee made a corpus pickle')
    fp.close()

    print('-' * 5)

    ourDict = getPickle('ourDict.pkl')

    print('ourDict:')
    print(len(ourDict))
    print(type(ourDict))

   
    # Needed for processing new words from user input
    newDict = updateDict(newWords, taggedCorpus)

    print('newDict:')
    print(len(newDict))
    print(type(newDict))

    # Save updated dict
    with open('data/newDict.pkl', 'wb') as fp:
        pickle.dump(newDict, fp)
        print('Aunt Bee made a new dict pickle')
    fp.close()

