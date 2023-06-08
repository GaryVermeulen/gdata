#
# buildDictionary.py
#
# Build a word dictionary from pickles
#

import os
import pickle

from datetime import datetime
from simpConfig import *
from mrScrapper import *
#from commonUtils import chkUnkownWords
#from commonUtils import scrapeWeb

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

def saveNewDict(p):
    with open(dictionaryFile, 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a mainDictionary pickle')
    fp.close()


def createNew():

    simpDict = {}
    cnt = 0
    
    print('Creating new dictioanry...')

    taggedList = getTaggedList()

    for taggedWord in taggedList:
        print('taggedWord: ', taggedWord)

        newWordDef = scrapeAndProcess(taggedWord)

        simpDict[taggedWord[0]] = newWordDef

        """
        cnt += 1

        if cnt > 5:
            break
        """
    """
    print('-' * 5)
    print('simpDict: ', len(simpDict))
    for w, d in simpDict.items():
        print(w, d)
        print('-' * 5)
    """
    saveNewDict(simpDict)
    

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


    
