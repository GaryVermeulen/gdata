#
# commonUtils.py
#

#import os
import sys
import pymongo

from commonConfig import *



def connectMongo():

    myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")

    return myclient


def getInflectionTag(tag):

    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'
    elif tag in [nn, nnp, nns]:
        return 'n'
    elif tag in [jj, jjr, jjs]:
        return 'a'

    return 'x'


def getInflections(word, tag, baseWordSearch, allInflections):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag))

    if len(allInflections) == 0:
        allInflections = loadPickle('inflections')
    
    for line in allInflections:
        if word in line:
#            print('found {} at {} {}'.format(word, cnt, line))
#            print('tag: ', tag)
            if line[1] == tag:
#                print('found v {} with tag {} at {} {}'.format(word, tag, cnt, line))
                if baseWordSearch:
#                    print('base word match {} at {} {}'.format(word, cnt, line))
                    return line
                else: # Search inflections only
                    idx = 0
                    for i in line:
                        if idx > 1:
                            if i == word:
#                                print('i: ', i)
#                                print('idx: ', idx)
#                                print('Non-base word match {} at {} {}'.format(word, cnt, line))
                                return line
                        idx += 1
#        cnt += 1

    return []

# Checks tagged user input aginst taggedBoW for conflicts
def chkTagging(taggedInput, tagged_BoW):

    tagging = []

    for w in taggedInput:
        tmpTag = []
        word = w[0]
        tag = w[1]
        tmpTag.append(word)
        tmpTag.append(tag)

        node = tagged_BoW.find({},{"taggedBoW":w[0]})

        print(w[0])
        print(node)
        
        for item in node:
            print(item)
        
        """
        for t in taggedBoW:    
            if w[0] == t[0]:
                tmpTag.append(t[1])
                print('t and i match: ')
                print('w; ', w)
                print('t: ', t)
        tagging.append(tmpTag)
        """
    """
    print('---')
    for t in tagging:
        print('t: ')
        print(t)
    """

    return 'tags match BoW or do not match BoW'

