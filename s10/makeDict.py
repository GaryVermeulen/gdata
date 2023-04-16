#
# makeDict.py
#
# Make a starter Pyton dictionary of CFG terminals from a text file.
#
import pickle


def readInput():

    dictList = []
    
    with open('data/starterDictionary.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            tmpLine = []
            if line[0] != '#':
                dictList.append(line.split(','))
                
    f.close()

    return dictList


def makeDict(dictList):

    ourDict = {}
    lastWord = ''
    wordCount = 1
    
    for line in dictList:
        
        word = line[0]
        tag = line[1]

        if word != lastWord:
            wordCount = 1
            
        word_n = word + '_' + str(wordCount)
        
        attributes = {'Word': word, 'Tag': tag}
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

    print(type(rawDictList))
    print('len rawDictList:', len(rawDictList))
    print(rawDictList)
    
    ourDict = makeDict(rawDictList)

    print('len type ourDict:', len(rawDictList), type(ourDict))
    """
    for k, v in ourDict.items():
        print('k: ', k)
        print('v: ', v)
    """
    makeDictPickle(ourDict)   

    
