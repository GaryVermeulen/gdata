#
# mongoTest.py
# MongoDb testing
#
import pymongo

from commonUtils import connectMongo

def listSuperclasses(nnxKB):

    all_nnxKB = list(nnxKB.find())
    superClassList = []

    for i in all_nnxKB:
        if i["superclass"] not in superClassList:
            #if i["superclass"] != None: # root does not have a superclass
            superClassList.append(i["superclass"])
                
#    for i in superClassList:
#        print(i)

    return superClassList


def walkTree(kb_cursor):

    print()


    return "something"

    


if __name__ == "__main__":

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]

    sClassList = listSuperclasses(nnxKB)

    kb_cursor_list = list(nnxKB.find())

    node = walkTree(kb_cursor_list)

    """
    for node in kb_cursor:
        #print(node)
        print('_id: ', node["_id"])
        print('similar: ', node["similar"])
        print('tag: ', node["tag"])
        print('canDo: ', node["canDo"])
        print('superclass: ', node["superclass"])
    """
        
        
    """
    cursor_nnp_BoW = tagged_BoW.find({"tag": "NNP"})
    cursor_nnp_KB = nnxKB.find({"tag": "NNP"})

    print(' --- KB ---')
    for docKB in cursor_nnp_KB:
        print(docKB)
        c = tagged_BoW.find({"word": docKB["_id"]})
        for i in c:
            print('match:', i)
            

    print(' --- BoW ---')
    toAdd = []
    for docBoW in cursor_nnp_BoW:
        print(docBoW)
        toAdd.append(docBoW)
        c = nnxKB.find({"_id": docBoW["word"]})
        for i in c:
            print('match:', i)
            toAdd.pop()

    print(' --- toAdd ---')
    for i in toAdd:
        print(i)

        
            #if docBoW["word"] == docKB["_id"]:
            #    print('Match')
            #    print(docBoW)
            #    print(docKB)
            #else:
            #    print('.', end = '')
                
    """
