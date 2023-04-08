#
# Construct small dictionary w/POS tags and short description
#       -- This is very rudimentary and imcomplete
#       -- makeDict.py
#
# Input: Small dictionary text file created by lorenza12 (4/18/2018)
#       -- No or imcomplete NNPs, NNS, and no verb tense
#
# Output:
#   attributes = {'Word': Word, 'POS':PoS, 'Tag': PoSTag, 'Description': Description}
#   myDict.update({word_text_n: attributes}) Where n = entry number
#

import pickle


def readInput():

    dictList = []
    
    with open('data/wordDictionary.txt', 'r') as f:
        while (line := f.readline().rstrip()):
                dictList.append(line)
    f.close()

    return dictList


def getTag(pos):

    posTag = 'Unknown'

    if pos == 'noun':
        posTag = 'NN'
    elif pos == 'pronoun':
        posTag = 'PRP'
    elif pos == 'verb':
        posTag = 'VB'
    elif pos == 'adjective':
        posTag = 'JJ'
    elif pos == 'adverb':
        posTag = 'RB'
    elif pos == 'preposition': # Didn't see any in file
        posTag = 'IN'           
    elif pos == 'conjunction': # Didn't see any in file
        posTag = 'CC'
    elif pos == 'interjection': # Didn't see any in file
        posTag = 'UH'
        
    return posTag


def makeDict(dictList):

    ourDict = {}
    lastWord = ''
    wordCount = 1
    
    for line in dictList:

        tmpLineList = []
        tmpLineList = line.split('|')
        word = tmpLineList[0]

        if word != lastWord:
            wordCount = 1
            
        word_n = word + '_' + str(wordCount)
        PoSTag = getTag(tmpLineList[1])
        attributes = {'Word': word, 'POS': tmpLineList[1], 'Tag': PoSTag, 'Description': tmpLineList[2]}
        ourDict.update({word_n: attributes})

        wordCount += 1
        lastWord = word

    return ourDict


def makeDictPickle(ourDict):

    with open('data/ourDict.pkl', 'wb') as fp:
        pickle.dump(ourDict, fp)
        print('Aunt Bee made a dictionary pickle')
    fp.close()

    return 



if __name__ == "__main__":

    rawDictList = readInput()

    print('len rawDictList:', len(rawDictList))
    
    ourDict = makeDict(rawDictList)

    print('len type ourDict:', len(rawDictList), type(ourDict))

#    for k, v in ourDict.items():
#        print('k: ', k)
#        print('v: ', v)

    makeDictPickle(ourDict)   

    
