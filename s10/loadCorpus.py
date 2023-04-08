#
# loadCorpus.py
#

import os
import spacy
import pickle
from simpConfig import simple_contractions
from simpConfig import verbose



def getRawData():
    # Read the test files
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
    tmpSents = corpusSents[120:146]

    for s in tmpSents:
#    for s in sents:

        expandedSentence = []
        tmpSent = s.split()
#        print('tmpSent: ', tmpSent)
        for w in tmpSent:
#            print('w: ', w)

            if w.find("'") != -1:
#                print("found ' in w: ", w)
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
#                    print('result: ', result)
                    resultList = result.split()
                    for r in resultList:
                        expandedSentence.append(r)
                else:
#                    print("w ' w:", w)
                    expandedSentence.append(w)

            elif w.find(";") != -1:     # Remove
                w = w.replace(';', '')
#                print('replace ; ', w)
                expandedSentence.append(w)
            elif w.find(",") != -1:     # Remove
                w = w.replace(',', '')
#                print('replace , ', w)
                expandedSentence.append(w)
            elif w in [' ', '-', ';', ',', '.', '..', '...']: # Skip over things we don't want
#                print('skipping: ', w)
                continue 
            else:
                expandedSentence.append(w)

#        print('vS: ', expandedSentence)
        expandedSents.append(expandedSentence)    

    return expandedSents

def getPickle():

    with open('data/ourDict.pkl', 'rb') as fp:
        ourDict = pickle.load(fp)
        print('Aunt Bee loaded ourDict.pkl')
    fp.close()

    return ourDict


def verifyWords(expandedCorpusSents):

    wordsFound = []
    wordsNotFound = []

    ourDict = getPickle()

    for s in expandedCorpusSents:
#        print(s)
        for w in s:
            if w in ourDict.keys():
#                print('found w in dict: ', w)
                wordsFound.append(w)
            else:
#                print('did not find w in dict: ', w)
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

#        print("Looking up: ", word)

        req = Request(
            url = "http://www.dictionary.com/browse/" + word.strip() + "",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        try:
            htmlFile = urlopen(req).read()
            found = True
        except:
#            print('not found...')
            notFound.append(word)
            found = False
            continue
          
        soup = BeautifulSoup(htmlFile, 'html.parser')

        soup1 = soup.find("meta", attrs={'name':'description'})


        try:
            soup1 = soup1.get_text()
            found = True
        except AttributeError:
#            print('Cannot find such word!')
#            print(word)
#            print('Check spelling.')
            #notFound.append(word)
            found = False
            continue
        if found:
            
            soup2 =soup.find(class_="luna-pos")
            txt = soup2.get_text()
            txt = os.linesep.join([s for s in txt.splitlines() if s]) # ?
            txtLst = txt.split('\n')

            soup3 = soup.find("meta", attrs={'name':'description'})
#            txt3 = soup3.get_text()
#            txt3 = os.linesep.join([s for s in txt3.splitlines() if s])

#            print('Found: ' + str(word))
#            print('soup1: ', soup1)
#            print('soup2: ', soup2)
#            print('soup3: ', soup3)
#            print('txt: ', txt)
#            print('txtLst: ', txtLst)

        newWords.append(word + ';' + txt + ';' + str(soup3))
	
    print("Done Scraping.")

    return newWords, notFound



def buildDict(words):
    """
    nlp = spacy.load("en_core_web_lg")

    myDict = {}

    strWords = str(words)
    strWords = strWords.replace("'", "")
    strWords = strWords.replace("'", "")
    strWords = strWords.replace("[", "")
    strWords = strWords.replace("]", "")
    strWords = strWords.replace(",", "")
    strWords = strWords.replace(";", "")

    taggedWords = nlp(strWords)

    for token in taggedWords:
        attributes = {"POS": token.pos_, "Tag": token.tag_, "TagExplain": spacy.explain(token.tag_), "Lemma": str(token.lemma_)}
        myDict.update({token.text: attributes})
    """
    return # myDict, taggedWords


def buildTaggedSentences(vSents):

    taggedSentences = []


    return taggedSentences


if __name__ == "__main__":

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
    print('-' * 5)

    wordsFound, wordsNotFound = verifyWords(expandedCorpusSents)

    print('wordsFound:')
    print(len(wordsFound))
    print(type(wordsFound))
    print('wordsNotFound:')
    print(len(wordsNotFound))
    print(type(wordsNotFound))
    
    
#    if verbose:
#        for w in wordsNotFound:
#            print('>>', w, '<<')
#            print('len w: ', len(w))
#            print('--')
#    
    print('-' * 5)

    newWords, notFound = getWordsNotFound(wordsNotFound)

    print('newWords:')
    print(len(newWords))
    print(type(newWords))
    print('notFound:')
    print(len(notFound))
    print(type(notFound))

    if verbose:
        for w in newWords:
            print('>>', w, '<<')
            print('len w: ', len(w))
            print('--')

        for w in notFound:
            print('>>', w, '<<')
            print('len w: ', len(w))
            print('--')

    


    """
    corpusDict, taggedWords = buildDict(corpusString)

    print('corpusDict: ')
    print(len(corpusDict))
    print(type(corpusDict))

    print('taggedWords:')
    print(len(taggedWords))
    print(type(taggedWords))

    
#    for token in taggedWords:
#        print(f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_):{40}} {str(token.lemma_)}')
#        attributes = {"POS": token.pos_, "Tag": token.tag_, "TagExplain": spacy.explain(token.tag_), "Lemma": str(token.lemma_)}
#        myDict.update({token.text: attributes})
#    
#    for x, y in myDict.items():
#        print(x, y)


#    with open('myDict.pkl', 'wb') as fp:
#        pickle.dump(myDict, fp)
#        print('made a dictionary pickle')
#    fp.close()
#
#    with open('taggedWords.pkl', 'wb') as fp:
#        pickle.dump(taggedWords, fp)
#        print('made a taggedWords pickle')
#    fp.close()

#    print('-' * 5)


    print('-' * 5)

    vettedSentences = vetSentences(corpusSents, corpusDict)


#    print('-' * 5)
#
#    taggedSentences = buildTaggedSentences(vettedSentences)


    print('corpusSents:')
    print(len(corpusSents))
    print(type(corpusSents))
    print('vettedSentencecs:')
    print(len(vettedSentences))
    print(type(vettedSentences))

    for vs in vettedSentences:
        print('..', vs, '..')

    
    vsLst = []
    for vs in vettedSentences:
#        print('vs: ', vs)
        vsLst.append(' '.join(vs))

    with open('vettedSents.txt', 'w') as f:
        f.write('\n'.join(vsLst))
    f.close()
    """
