#
# processRawKB.py
#

from commonUtils import connectMongo

def loadRawKB():
    # Read the ordered starter kb file
    # For now only handling NNPs and NNs--we'll deal with plurals later

    kbList = []
    isAlive = False
    
    with open('kb/orderedInputLong.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                print(tmp)
                if tmp[2] == "T":
                    isAlive = True
                else:
                    isAlive = False
                tmpDict = {
                    "_id":tmp[0],
                    "tag":tmp[1],
                    "isAlive": isAlive,
                    "canDo":tmp[3],
                    "superclass":tmp[4]
                }
                kbList.append(tmpDict)
    f.close()
                                   
    return kbList


def buildKB(kb):
    
    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]

    nnxKB = simpDB["nnxKB"]

    # For now start fresh every run
    nnxKB.drop()

    # root
    root = {"_id": "GodParticle", "tag": "NNP", "isAlive": False, "canDo": "everything", "superclass": None}
    nnxKB.insert_one(root)
    # The rest from the predefined list
    nnxKB.insert_many(kb)

    return "Added KB to simp"




if __name__ == "__main__":

    print('Processing KB...')
    
    kb = loadRawKB() 
    print('kb:')
    print(len(kb))
    print(type(kb))
    for k in kb:
        print(k)    
        
    print('-' * 5)

    print(buildKB(kb))

    print('processKB Complete.')
