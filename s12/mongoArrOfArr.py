# mongoArrOfArr.py
# MongoDB test: search an array of arrys for a word
#
# _id: ObjectID(123...)
# taggedSentence: Array (len)
#   0: Object
#      word: "however"
#      tag: "RB"
#   1: Object
#      word: "before"
#      tag: "IN"
#
#
import pymongo
import socket


def connectMongo():

    if socket.gethostname() == 'system76-pc':
        # Home server
        myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
    else:
        # Assume work server
        myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")

    return myclient


word = "her"
tag = "PRP$"
mdb = connectMongo()
simpDB = mdb["simp"]

taggedCorpus = simpDB["taggedCorpus"]

cursor = taggedCorpus.find({"taggedSentence": {"$elemMatch": {"word": word, "tag": tag}}})

for c in cursor:
    print('-----')
    print(c)

print('==========================')
tag = "PRP"
cursor = taggedCorpus.find({"taggedSentence": {"$elemMatch": {"word": word, "tag": tag}}})

for c in cursor:
    print('-----')
    print(c)
