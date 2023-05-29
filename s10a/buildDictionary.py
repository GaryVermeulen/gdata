#
# buildDictionary.py
#
# Build a word dictionary from pickles
#

import os
import pickle

from datetime import datetime
from simpConfig import *
#from commonUtils import chkUnkownWords
from commonUtils import scrapeWeb

dictionaryFile = 'pickles/mainDictionary.pkl'



def getTaggedList():

    with open('pickles/newTaggedList.pkl', 'rb') as fp:
        taggedList = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()

    return taggedList
 

def saveExisting():
    now = datetime.now()
    timeStamp = now.strftime("%m%d%y-%H%M%S")

    if os.path.isfile(dictionaryFile):
        os.rename(dictionaryFile, dictionaryFile + '.' + timeStamp)


def createNew():
    print('Creating new dictioanry...')

    newWords = []
    notFound = []
    cnt = 0

    taggedList = getTaggedList()

    for taggedWord in taggedList:
#        tmp = []
        print('taggedWord: ', taggedWord)
#        tmp.append(taggedWord[0])
#        newWord, notWord = chkUnkownWords(tmp)
        newWord, notWord = scrapeWeb(taggedWord[0])
    
        if len(newWord) > 0:
            tmp = []
            tmp.append(newWord)
            tmp.append(taggedWord[1])
            newWords.append(tmp)
        else:
            notFound.append(notWord)

        cnt += 1

        if cnt > 5:
            break

    print('newWords: ', len(newWords))
    print('notFound: ', len(notFound))
    for w in newWords:
        print(w)
    

def appendExisting():
    print('Appending to existing dictionary...')
    


if __name__ == "__main__":

    results = ''

    if os.path.isfile(dictionaryFile):
        print('Existing dictionary found!')
        while results not in ['O', 'o', 'A', 'a']:
            results = input('Overwrite or Append <O|A>?')

        if results in ['O', 'o']:
            saveExisting()
            createNew()
        else:
            appendExisting()
    else:
        print('Existing dictionary not found, creating new...')
        createNew()    


    
