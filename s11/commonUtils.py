#
# commonUtils.py
#

import socket
import sys
import pymongo

from commonConfig import *



def connectMongo():

    if socket.gethostname() == 'system76-pc':
        # Home server
        myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
    else:
        # Assume work server
        myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")

    return myclient


def listSuperclasses(nnxKB):

    all_nnxKB = list(nnxKB.find())
    superClassList = []

    for i in all_nnxKB:
        if i["superclass"] not in superClassList:
            if i["superclass"] != None: # root does not have a superclass
                superClassList.append(i["superclass"])
                
    for i in superClassList:
        print(i)

    return superClassList


def listKB_Entries(nnxKB):

    all_nnxKB = list(nnxKB.find())
    entriesList = []

    for i in all_nnxKB:
        if i["_id"] not in entriesList:
            entriesList.append(i["_id"])
                
    for i in entriesList:
        print(i)

    return entriesList


def isEntry(taggedWord, nnxKB):

    for e in list(nnxKB.find()):
        if taggedWord[0].lower() == e["_id"].lower():
            return True

    return False


def getEntryAll(taggedWord, nnxKB):

    allEntries = []
    
    for e in list(nnxKB.find()):
        if taggedWord[0].lower() == e["_id"].lower():
            allEntries.append(((taggedWord[0], taggedWord[1]),(e["_id"], e["tag"])))

    return allEntries


def isEntryBoW(taggedWord, tagged_BoW):

    for e in list(tagged_BoW.find()):
        if taggedWord[0].lower() == e["word"].lower():
            return True

    return False


def getEntryAllBoW(taggedWord, tagged_BoW):

    allEntries = []
    
    for e in list(tagged_BoW.find()):
        if taggedWord[0].lower() == e["word"].lower():
            allEntries.append(((taggedWord[0], taggedWord[1]),(e["word"], e["tag"])))

    return allEntries


# Current list of inflections is lacking, note prp)
def getInflectionTag(tag):
    """
    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'
    elif tag in [nn, nns]:
        return 'n'
    elif tag in [jj, jjr, jjs, rb, rbr, rbs]:
        return 'a'

    return 'x'
    """
    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return vb
    elif tag in [nn, nns]:
        return nn
    elif tag in [jj, jjr, jjs, rb, rbr, rbs]:
        return jj

    return 'x'



def getInflections(word, tag):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag))

    records = []
    inflects = []
    
    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflectionsCol"]

#    print('word: ', word)
#    print('tag: ', tag)

    query = {"inflections": word}
#    cursor = inflectionsCol.find(query)

    records = list(inflectionsCol.find(query))
    

#    for record in cursor:
#        records.append(record["inflections"])

    print('word: ', word)
    print('tag: ', tag)
    print('getInflections -> records: ', records)
    
    for r in records:
        if r["tag"] == tag:
            print('r: ', r)
            inflects.append(word)
            for i in r["inflections"]:
                inflects.append(i)
            return inflects

#    if len(records) > 0:
#        return records[0] # Always going to only one item in the list
    
    return ['inflection error']


def getBaseWordFromInflections(word):

    baseWord = 'NONE'

    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflectionsCol"]

    cursor = inflectionsCol.find({"inflections": word})

    for i in cursor:
        print("Found i in cursor: ", i)

        baseWord = i.get("word")
        baseWordInflections = i.get("inflections")

        print('baseWord: ', baseWord)
        print('baseWordInflections: ', baseWordInflections)

    if baseWord == 'NONE':
        return(baseWord, unk)

    return [baseWord, i.get("tag")]


def getBaseWordFromInflections2(word):

    baseWord = 'NONE'
    inflectLst = []

    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflectionsCol"]

    cursor = inflectionsCol.find({"inflections": word})

    for i in cursor:
        print("Found i in cursor: ", i)

        baseWord = i.get("word")
        baseWordTag = i.get("tag")
        baseWordInflections = i.get("inflections")

        print('baseWord: ', baseWord)
        print('baseWordInflections: ', baseWordInflections)

        inflectLst.append((baseWord, baseWordTag, baseWordInflections))

    if baseWord == 'NONE':
        return(baseWord, unk)

    return inflectLst


def isInInflections(inWord):

    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflectionsCol"]

    cursor = list(inflectionsCol.find({"inflections": inWord[0]}))

    if len(cursor) > 0:
        return True

    return False


# Checks tagged user input aginst taggedBoW for conflicts (original naive)
# Many TODOs
#
def chkTagging(taggedInput, tagged_BoW):
    # We'll keep this nightmare as-is for now and work on post SA tag checker 

    tagging = []
    mismatch = []
    multiple = []
    unknown = []
    baseWord = []
    wordPosition = 1

    # Naive checks
    # TODO:
    # Instead of just finding issues also try to deal with them:
    # tagMismatch    :  [['home', 'NN', 'RB', 'NN']]
    # tagMultiple    :  [['home', 'NN', 'RB', 'NN']]
    # tagUnknown     :  [xyz...]
    #
    for w in taggedInput:
        tmpTag = []
        tmpBaseWord = []
        word = w[0]
        tag = w[1]

        if wordPosition == 1:
            if tag not in ['NNP', 'NNPS']:
                word = word.lower()

        # org was to blindly pas it on... but let's check for multiple 
        tmpTag.append(word)
        tmpTag.append(tag)

        query = {"word": word}
        records = list(tagged_BoW.find(query))

        if len(records) < 1:
            print('{} not found in BoW.'.format(word))
            print('Looking at inflections array for word:', word)

            results = getBaseWordFromInflections(word)

            print('results: ', results)
            print(len(results))

            if len(results) > 0:
                #print('appending tmpBaseWord')
                tmpBaseWord.append(word)
                tmpBaseWord.append(tag)
                tmpBaseWord.append(results[0])
                tmpBaseWord.append(results[1])
                #print('tmpBaseWord" ', tmpBaseWord)
            
        else:
            for record in records:
                tmpTag.append(record.get("tag"))

                            
        tagging.append(tmpTag)
        if len(tmpBaseWord) > 0:
            baseWord.append(tmpBaseWord)
        wordPosition +=1
    
    for t in tagging:
        #print('t: ', t)
        #print(baseWord)
        if len(t) > 2:
            if t[1] != t[2]:
                mismatch.append(t)
            if len(t) > 3:
                multiple.append(t)
        else:
            if len(baseWord) == 0:
                unknown.append(t)


    # Check for tagging erros, ie. word can be NN or VB
    # ex: tagger returns: ('work', 'VB') instead of: ('work', 'NN')
    # [('he', 'PRP'), ('was', 'VBD'), ('late', 'JJ'), ('to', 'TO'), ('work', 'VB')]
    # 
    # Use transitive verb and nontransitive verb lists--uck
    # Yet another naive solution for a complex problem
    #
    # How to handle words that are both:
    # I walked.
    # I walked the dogs.
    # Daniel drives.
    # Daniel drives a large truck.
    # Barbara reads.
    # Barbara reads 10 books a month.
    # I understand.
    # I understand you.

    

    return mismatch, multiple, unknown, baseWord




#
def isWordKnown(inWord, inSentObj):
    # Is the word known and where?
    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    
    #print(" -- Start isWordKnown --")
    #print("inWord: ", inWord)

    foundWord = False

    word = inWord[0]
    tag  = inWord[1]

    # Lower case word in not NNx
    if tag not in ['NNP', 'NNPS']:
        word = word.lower()

    # Is the word in BoW?
    #print('Checking Bow...')
    if isEntryBoW(inWord, tagged_BoW):
        #print('Found {} in Bow'.format(word))
        tmpBoW = ('BoW', True)
        foundWord = True
    else:
        tmpBoW = ('BoW', False)

    # Is the word in inflectionsCol?
    #print('Checking inflectionsCol...')
    if isInInflections(inWord):
        #print('Found {} in inflectionsCol'.format(word))
        tmpInflects = ('inflectionsCol', True)
        foundWord = True
    else:
        tmpInflects = ('inflectionsCol', False)

    # Is the word in the nnxKB?
    #print('Checking nnxKB...')
    if isEntry(inWord, nnxKB):
        #print('Found {} in nnxKB'.format(word))
        tmp = ('nnxKB', True)
        foundWord = True
    else:
        tmp = ('nnxKB', False)

    inSentObj.data.append([inWord, tmpBoW, tmpInflects, tmp])

    return foundWord, inSentObj


def chk_nnxKB(item, nnxKB):

    print('chk_nnxKB looking for: ', item)
    
    query = {"_id": item}
    records = list(nnxKB.find(query))

    if len(records) < 1:
        print('KB item: {} not found in KB.'.format(item))
        return {}
    else:
        if len(records) == 1:
            return records[0]
        else:                
            print('{} records found for {} where we should have only one...~?'.format(len(records), item))
            return {}            
        
    # End chk_nnxKB


def chkCorpus(items, untaggedCorpus):

    records = []

    print('chkCorpus looking for: ', items)

    for item in items:
    
        query = {"untaggedSentence": item}
        cursor = untaggedCorpus.find(query)

        for record in cursor:
            records.append(record["untaggedSentence"])

    return records


def list2String(someList):

    stringList = ''

    if len(someList) == 0:
        return 'zero length list supplied'

    if isinstance(someList, list):
        for x in someList:
            stringList = stringList + ' ' + x
    elif isinstance(someList, tuple):
        stringList = someList[0]
    else:
        print('list2String list or tuple not provide.')

    return stringList


def expandSent(rawSentence):

    wordCnt = 0
    expandedSentence = []
    tmpSent = rawSentence.split()

    for w in tmpSent:
            
        w = w.strip()
        wordCnt += 1
            
        if w.find("'") != -1: # Doesn't handle idioms such as: someone's
            if w in simple_contractions.keys():
                result = simple_contractions[w]
                resultList = result.split()
                for r in resultList:
                    expandedSentence.append(r)
            else:
                print('>>{}<< not in  contractions'.format(w))
                print('rawSentecne: ', rawSentence)
            continue
                        
        clean_word = ''.join(filter(str.isalnum, w))

        if len(clean_word) > 0:
            expandedSentence.append(clean_word)
                
    return expandedSentence

