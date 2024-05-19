#
# readCorpora.py
#
# Read input book(s)...
#

from collections import Counter

from commonUtils import connectMongo
from findSVO import findSVO




#
#
#
if __name__ == "__main__":

    bookSentenceObjects = []

    mdb = connectMongo()
    simpDB = mdb["simp"]
    taggedCorpora = simpDB["taggedCorpora"]

    cursorLst = list(taggedCorpora.find({}))

    for c in cursorLst:
        print(c["bookName"])
        print('======')
        for s in c["taggedSentences"]:
            print(s)
            
            svoObj = findSVO(s)
            svoObj.printAll()
            print('---')

            for subj in svoObj.subject:
                bookSentenceObjects.append(subj)
            

        print('------')

        print('bookSentenceObjects (subjects):')
        print(bookSentenceObjects)

        print('------')

        objects = []
        for item in bookSentenceObjects:
            objects.append(item[0]) 

        x = Counter(objects)

        print(x)
        
