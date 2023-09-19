#
# mongoTest.py
# MongoDb testing
#
import pymongo

from commonUtils import connectMongo



if __name__ == "__main__":

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]

    cursor_nnp_BoW = tagged_BoW.find({"tag": "NNP"})
    cursor_nnp_KB = nnxKB.find({"tag": "NNP"})

    print(' --- KB ---')
    for docKB in cursor_nnp_KB:
        print(docKB)
        c = tagged_BoW.find({"word": docKB["_id"]})
        for i in c:
            print('match:', i)
            

    print(' --- BoW ---')
    for docBoW in cursor_nnp_BoW:
        print(docBoW)
        c = nnxKB.find({"_id": docBoW["word"]})
        for i in c:
            print('match:', i)



        
            #if docBoW["word"] == docKB["_id"]:
            #    print('Match')
            #    print(docBoW)
            #    print(docKB)
            #else:
            #    print('.', end = '')
                
