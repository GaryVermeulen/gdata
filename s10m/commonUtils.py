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


# Checks tagged user input aginst taggedBoW for conflicts
def chkTagging(taggedInput, tagged_BoW):

    tagging = []
    mismatch = []
    multiple = []
    unknown = []

    for w in taggedInput:
        tmpTag = []
        word = w[0]
        tag = w[1]
        tmpTag.append(word)
        tmpTag.append(tag)

        query = {"word":w[0]}
        records = list(tagged_BoW.find(query))

        if len(records) < 1:
            print('{} not found in BoW.'.format(w[0]))
        else:
            for record in records:
                tmpTag.append(record.get("tag"))
                              
        tagging.append(tmpTag)
    
    for t in tagging:
        if len(t) > 2:
            if t[1] != t[2]:
                mismatch.append(t)
            if len(t) > 3:
                multiple.append(t)
        else:
            unknown.append(t)

    return mismatch, multiple, unknown


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

