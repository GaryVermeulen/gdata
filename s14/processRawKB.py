#
# processRawKB.py
#

from commonUtils import connectMongo
import pickle

pickleFile = 'data/processedKB.p'

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
                    isNonfiction = True
                else:
                    isNonfiction = False
                    
                if tmp[3] == "T":
                    isAlive = True
                else:
                    isAlive = False
                    
                tmpDict = {
                    #"_id":tmp[0],
                    "word": tmp[0],
                    "tag": tmp[1],
                    "isNonfiction": isNonfiction,
                    "isAlive": isAlive,
                    "canDo": tmp[4],
                    "superclass": tmp[5]
                }
                kbList.append(tmpDict)
    f.close()
                                   
    return kbList


def buildMongoKB(kb):
    
    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]

    nnxKB = simpDB["starterKB"]

    # For now start fresh every run
    nnxKB.drop()

    # root
    #root = {"_id": "GodParticle", "tag": "NNP", "isAlive": False, "canDo": "everything", "superclass": None}
    #nnxKB.insert_one(root)
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

    print('dumping kb to pickle...')
    with open(pickleFile, "wb") as f:
        pickle.dump(kb, f)
    
    print('------------')
 
    #
    print(buildMongoKB(kb))

    print('processKB Complete.')
