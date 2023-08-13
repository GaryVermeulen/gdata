#
# commonUtils.py
#

#import os
import sys
import pymongo

from commonConfig import *



def connectMongo():

    # Home server
    myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")

    # Work server
    #myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")

    return myclient


def getInflectionTag(tag):

    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'
    elif tag in [nn, nnp, nns]:
        return 'n'
    elif tag in [jj, jjr, jjs]:
        return 'a'

    return 'x'


def getInflections(word, tag):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag))

    records = []
    inflects = []
    
    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflectionsCol = simpDB["inflections"]

    print('word: ', word)
    print('tag: ', tag)

    query = {"inflections": word}
    cursor = inflectionsCol.find(query)

    for record in cursor:
        records.append(record["inflections"])

    print('records: ', records)

    for r in records:
        if r[1] == tag:
            inflects.append(r)
    
    return inflects

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


def chkCorpus(item, untaggedCorpus):

    records = []

    print('chkCorpus looking for: ', item)
    
    query = {"untaggedSentence": item}
    cursor = untaggedCorpus.find(query)

    for record in cursor:
        records.append(record["untaggedSentence"])

    return records
