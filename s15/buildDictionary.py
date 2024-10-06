#
# buildDictionary.py
#
# Build a Mongo dictionary collection
# Input: Downloaded copy of "Oxford English Dictionary.txt"
# Note: This will only keep words with Penn Treebank POS tags.
# New: 3/24/2024; Modified: 8/2/2024
#

import socket
import pymongo
import itertools

def connectMongo():

    #if socket.gethostname() == 'system76-pc':
    #if socket.gethostname() == 'pop-os':
    #    # Home server
    #    #myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
    #    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    #else:
    #    # Assume work server
    #    myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")
    # All local
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    return myclient


def loadRawFile():
    rawDict = []
    lineCnt = 0

    with open('inputData/Oxford English Dictionary.txt', 'r') as f:
        while (line := f.readline()):
            line = line.strip()
            line = line.replace('\x7f', '')
            rawDict.append(line)
            lineCnt += 1
    f.close()

    print("read {} lines".format(lineCnt))

    return rawDict

def processRawDict(rawDict):
    lstDict = []
    lineCnt = 0
    
    for line in rawDict:
        tmpLine = []
        ckWord = ''
        tmpDef = ''
        if len(line) > 0:  # Skip blank lines
            newLine = line.split('  ') 
            if len(newLine) > 1: # Keep lines with definitions
                ckWord = newLine[0]
                if ckWord[0] == '-':
                    tmpLine.append(ckWord[1:])
                    tmpLine.append(newLine[1])
                    lstDict.append(tmpLine)
                elif ckWord[len(ckWord) - 1] == '-':
                    tmpLine.append(ckWord[:len(ckWord) - 1])
                    tmpLine.append(newLine[1])
                    lstDict.append(tmpLine)
                else:
                    lstDict.append(newLine)

                lineCnt +=1

    print("processed {} lines".format(lineCnt))

    print('B4; lstDict len: ', len(lstDict))

    # Attempt to remove any duplicates
    tmpLst = []
    for i in lstDict:
        if i not in tmpLst:
            tmpLst.append(i)

    ### Below does not work!?!?
    ##lstDict.sort()
    ##list(lstDict for lstDict,_ in itertools.groupby(lstDict))
    #lstDict = list(set(lstDict))

    print('After; lstDict=> tmpLst len: ', len(tmpLst))
            
    return tmpLst # lstDict

def tagLstDict(lstDict):
    lineCnt = 1
    taggedDict = []

    for line in lstDict:
#        if lineCnt < 20:
#            print('line: ', line)
        tmpLine = []
        word = line[0]
        definition = line[1]
        tag = ''
        tmpDef = definition.split()

        # Fix words: word1, word2...
        lastChar = word[len(word) - 1]
        if lastChar.isnumeric():
            word = word[:len(word) - 1]
        
        
        if tmpDef[0] in ['n.', '—n.']:
            tag = 'NN'
        elif tmpDef[0] in ['n.pl.', '—n.pl.']:
            tag = 'NNS'
        elif tmpDef[0] in ['v.', '—v.']:
            tag = 'VB'
        elif tmpDef[0] in ['adv.', '—adv.']:
            tag = 'RB'
        elif tmpDef[0] in ['adj.', '—adj.']:
            tag = 'JJ'
        elif tmpDef[0] in ['sym.', '—sym.', 'symb.', '—symb.']:
            tag = 'SYM'
        elif tmpDef[0] in ['pron.', '—pron.']:
            tag = 'PRP'
        else:
            tag = 'UNK'

        # Something funky with input...~?!
#        if len(tmpDef) < 2:
#            print('### {}: {}'.format(lineCnt, tmpDef))
#            print(line)

        if len(tmpDef) > 1:
        # In some cases POS is tmpDef[1]
            if tag == 'UNK':
                if tmpDef[1] in ['n.', '—n.']:
                    tag = 'NN'
                elif tmpDef[1] in ['v.', '—v.']:
                    tag = 'VB'
                elif tmpDef[1] in ['adv.', '—adv.']:
                    tag = 'RB'
                elif tmpDef[1] in ['adj.', '—adj.', 'Adj.']:
                    tag = 'JJ'
                elif (tmpDef[0] in ['poss.', '—poss.']) and (tmpDef[1] in ['pron.', '—pron.', 'Pron.', '—Pron.']):
                    tag = 'PRP$'
                else:
                    tag = 'UNK'

        tmpLine.append(lineCnt) # Record/index number
        tmpLine.append(word)
        tmpLine.append(tag)

        if len(line) > 2: # Try to catch multiple-double-spaces
            definition = line[1] + ' ' + line[2]
            tmpLine.append(definition)
        else:
            tmpLine.append(definition)
            
        taggedDict.append(tmpLine)

#        if lineCnt < 20:
#            print('definition: ', definition)

        lineCnt += 1

    print("tagged {} lines".format(lineCnt))

    return taggedDict

#
if __name__ == "__main__":

    cnt = 0

    rawDict = loadRawFile()

    for line in rawDict:
        print('cnt: {}: {}'.format(cnt, line))
        cnt += 1
        if cnt > 20:
            break

    cnt = 0
    lstDict = processRawDict(rawDict)

    for line in lstDict:
        print('cnt: {}: {}'.format(cnt, line))
        cnt += 1
        if cnt > 20:
            break
        
    cnt = 0
    taggedDict = tagLstDict(lstDict)

#    for line in taggedDict:
#        if line[2] == 'UNK':
#            print(line)
#        cnt += 1
#        if cnt > 20:
#            break


    mdb = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    simpDB = mdb["simp"]
    simpDictionary = simpDB["simpDictionary"]

    simpDictionary.drop()

    for line in taggedDict:
        if line[2] != 'UNK':
            simpDictionary.insert_one({"index": line[0], "word": line[1], "tag": line[2], "definition": line[3]})
        
        
    
