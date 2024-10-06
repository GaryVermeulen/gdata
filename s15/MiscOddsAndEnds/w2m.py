# w2m.py
# Take Wiki XML/JSON and make MongoDB
#
import os
import json
import pymongo
import time
import datetime
import socket

def connectMongo():

    #if socket.gethostname() == 'system76-pc':
    if socket.gethostname() == 'pop-os':
        # Home server
        #myclient = pymongo.MongoClient("mongodb://10.0.0.20:27017")
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    else:
        # Assume work server
        #myclient = pymongo.MongoClient("mongodb://192.168.0.16:27017")
        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        
    return myclient


def readWiki():
    # Read the raw corpus file(s)--There is so much data
    # cannot read it all into memory :-(
    wikiList = []
    corpusStr = ''
    #progPath = os.getcwd()
    #dataPath = progPath + '/Corpus'
    #dataPath = '/home/gary/tmp/archive/enwiki20201020'
    dataPath = '/home/gary/data/archive/enwiki20201020'
    dirList = os.listdir(dataPath)
    fileCount = 0
    global docCount

    print('Reading Wiki Input File(s)...')

    mdb = connectMongo()
    simpDB = mdb["simp"]
    wikiData = simpDB["wikiData"]

    wikiData.drop() # Start fresh

    # Read corpus input
    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r', encoding="utf8") as f: # Added , encoding="utf8" for Win PC
            fileCount += 1
            print("{}: Processing file: {}".format(fileCount, inFile))

            data = json.load(f)

            print('len data: ', len(data))
            print('type data: ', type(data))
            for d in data:
                #print(d)
                #print('     len d: ', len(d))
                #print('     type d: ', type(d))
                #print('     keys d: ', d.keys())
                #wikiList.append(d)
                wID = d['id']
                wTitle = d['title']
                wTitleLC = d['title'].lower()
                wText = d['text']

                wikiData.insert_one({'id': wID, 'title': wTitle, 'titleLC': wTitleLC, 'text': wText})
                docCount += 1
            print('-----')
            
        f.close()

    print('Reading Wiki Input Completed.')

    return wikiList




if __name__ == "__main__":

    
    start = time.time()
    docCount = 0
    print("Starting at:")
    print(datetime.datetime.now())
    print("----------")

    wikiList = readWiki()

    print('len:  ', len(wikiList))
    print('type: ', type(wikiList))
    print('docCount: ', docCount)

#    for i in wikiList:
#        print(len(i))
#        print(type(i))
#        print('---')
#        print('i:')
#        print(i)

    end = time.time()
    print("\nET: ", end - start)
    print("FIN at:")
    print(datetime.datetime.now())
