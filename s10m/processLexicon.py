# processLexicon.py
#
# Build dictionary/lexicon from BoW
#

from mrScrapper import scrapeAndProcess
from commonUtils import connectMongo


def buildLex():

    bigList = []
    cnt = 0

    mdb = connectMongo()
    simpDB = mdb["simp"]
    taggedBoW = simpDB["taggedBoW"]
    lexicon = simpDB["lexicon"]

#    for x in taggedBoW.find():
#        print(x)

    taggedBoWList = list(taggedBoW.find())

    print(len(taggedBoWList))
    print(type(taggedBoWList))

    for x in taggedBoWList:
        print(x)
        print(x['word'])
        print(x['tag'])

        taggedWord = ((x['word'], x['tag']))

        print('taggedWord: ', taggedWord)

        newWordDef = scrapeAndProcess(taggedWord)

        newWordDef = formatWordDef(newWordDef)

        lexicon.insert_many(newWordDef)
            

        cnt =+ 1
        if cnt > 10:
            break

    print('-' * 5)
    print(len(bigList))

    return 'buildLex return'


def formatWordDef(newWordDef):

    dLst = []
    
    for d in newWordDef:
        print(d)
        print(d[0][0])
        print(d[1][0])

        #if d[1][0] == 'noun'
        if len(d) == 3:
            print(d[2])
            dLst.append({"word": d[0][0], "tag": d[1][0], "definition": d[2]})
        else:
            print(d[3])
            dLst.append({"word": d[0][0], "tag": d[1][0], "definition": d[3]})
            

    return dLst



#
#
if __name__ == "__main__":

    print('Processing processLexicon (__main__)...')

    results = buildLex()

    print('Completed processLexicon (__main__)...')
