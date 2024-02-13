#
# addWebWords.py
#
#   Take words scrpaed from the web and add them to webWords.
#

import pickle

from commonUtils import connectMongo


def makeWordDef(w):

    wordDef = {}
    tmpSims = []

    word = w[0]["word"][0]
    tag = w[0]["word"][1]

    for i in w:
        for x in i["similars"]:
            tmpSims.append(x)

    print("WORD: ", word)
    print("TAG:  ", tag)
    print(len(tmpSims))
    print('tmpSims: ', tmpSims)

    tmpSims = list(set(tmpSims))
    print('de-duped tmpSims: ', len(tmpSims))
    print('tmpSims: ', tmpSims)
    wordDef = {"word": word, "tag": tag, "similars": tmpSims}

    return wordDef


def addWebWord(w):
    mdb = connectMongo()
    simpDB = mdb["simp"]
    webWords = simpDB["webWords"]

     
    # For now just blindly add it
    for wordDef in w:
        
        results = webWords.insert_one(wordDef)
        print('insert results: ', results.inserted_id)
    

if __name__ == "__main__":

    print('--- addNNX.py -- __main__ ')
    
    with open('pickles/newWords.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newWords.pkl')
    fp.close()
    
    print("-" * 10)
    for word in ourPickle:
        for wordDef in word:
            print(wordDef)
    add = input("Continue to add <Y/n>? ")

    if add in ['y', 'Y']:
        for word in ourPickle:
            r = addWebWord(word)
            
