#
# processCorpus.py
#
#

import os
import pickle
# import spacy

from simpConfig import simple_contractions
from simpConfig import verbose



def getCorpus():
    # Read the corpus files
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

    for s in corpusSents:
        expandedSentence = []
        tmpSent = s.split()

        for w in tmpSent:
            if w.find("'") != -1: # Doesn't handle idioms such as: someone's
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
            elif w.find(",") != -1:     # Replace
                w = w.replace('-', ' ') 
                expandedSentence.append(w)
            elif w.find("(") != -1:     # Replace
                w = w.replace('(', ' ') 
                expandedSentence.append(w)
            elif w.find("(") != -1:     # Replace
                w = w.replace(')', ' ')
                expandedSentence.append(w)
            elif w in [' ', ';', ',', '.', '..', '...']: # Skip over things we don't want to deal with
                continue 
            else:
                expandedSentence.append(w)

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


    cleanerCorpus = rejectNotFound(expandedCorpusSents, badWords)
    
    return cleanerCorpus


def chkUnkownWords(wordsNotFound):
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


def mergeCorpus(cleanerCorpus, starterCorpus):

    return cleanerCorpus + starterCorpus


if __name__ == "__main__":

    print('Processing corpus...')

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
    """
    for w in starterDictList:
        print(w)
  
    print('-' * 5)
    """
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
    for s in expandedCorpusSents:
        print(s)
        for w in s:
            if w == "knowif":
                print('>>> bad s: ', s)
    """
    print('-' * 5)
    
    cleanerCorpus = cleanCorpus(expandedCorpusSents, starterDictList)
    
    print('cleanerCorpus:')
    print(len(cleanerCorpus))
    print(type(cleanerCorpus))
    """
    for s in cleanerCorpus:
        print(s)
        for w in s:
            if w == "knowif":
                print('>>> bad s: ', s)
    """
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
    for s in newCorpus:
        print(s)

    # Save new working corpus...
    with open('newCorpus.pkl', 'wb') as fp:
        pickle.dump(newCorpus, fp)
        print('Aunt Bee made a newCorpus pickle')
    fp.close()

    print('processCorpus Complete.')  
