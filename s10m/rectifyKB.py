#
# rectifyKB.py
#
# 1) Check for tagging errors in BoW and tagged senetences
#       Only checking on lower case NNPs
# 2) Verify and add NN and NNPs in BoW but not in KB
#       This could be can of worms
#

from commonUtils import connectMongo
from commonConfig import validTags


def updateTagInBoW(w, cleanTagged_BoW_List):

    print('word:', w["word"])
    print('tag: ', w["tag"])

    for i in cleanTagged_BoW_List:
        if i[0] == w["word"]:
            i[1] = w["tag"]
            print(i)
            
    return cleanTagged_BoW_List


def updateCaseInBoW(w, cleanTagged_BoW_List):

    print('word:', w["word"])
    print('tag: ', w["tag"])

    for i in cleanTagged_BoW_List:
        if i[0] == w["word"].lower():
            print('i before: ', i)
            i[0] = w["word"]
            print('i after: ', i)
    
    return cleanTagged_BoW_List


def lowerCaseCheck(tagged_BoW, taggedCorpus):

    print('- lowerCaseCheck Start -')

    cleanTaggedCorpusList = []
    cleanTagged_BoW_List = []

    taggedCorpusList = list(taggedCorpus.find())
    tagged_BoW_List = list(tagged_BoW.find())

    # Not sure this will be needed going all Python
    bowNNP_Lst = list(tagged_BoW.find({"tag": "NNP"})) 

    # There may be a better way, but let's go the Pyhton way
    
    for t in taggedCorpusList:
        #print(t["taggedSentence"])
        cleanTaggedCorpusList.append(t["taggedSentence"])

    for t in tagged_BoW_List:
        #print(t)
        tmpWordTag = []
        word = t["word"]
        tag = t["tag"]
        tmpWordTag.append(word)
        tmpWordTag.append(tag)
        cleanTagged_BoW_List.append(tmpWordTag)

    newCleanTaggedCorpusList = []
    
    for s in cleanTaggedCorpusList:
        for w in s:
            if w["tag"] == "NNP":
                if w["word"].islower():
                    print('Found lower case NNP:')
                    print(w)
                    print('In tagged corpus sentence:')
                    print(s)
                    result = input('Enter correct POS tag, CAP (capitalize), or <CR> to keep NNP and case: ')

                    if result in validTags:
                        w["tag"] = result

                        print("new tag:")
                        print(w)
                        cleanTagged_BoW_List = updateTagInBoW(w, cleanTagged_BoW_List)
                    elif result in ['cap', 'Cap', 'CAP']:
                        w["word"] = w["word"].capitalize()
                
                        print('New T (upCase):')
                        print(w)
                        cleanTagged_BoW_List = updateCaseInBoW(w, cleanTagged_BoW_List)
                    print('new s:')
                    print(s)
                    print('------')
    print('verify:')
    print('-' * 10)
    for s in cleanTaggedCorpusList:
        for w in s:
            if w["tag"] == "NNP":
                if w["word"].islower():
                    print('Found lower case NNP:')
                    print(w)
    
    print('-' * 10)
    for w in cleanTagged_BoW_List:
        if w[1] == "NNP":
            if w[0].islower():
                print('Found lower case NNP in BoW:')
                print(w)
                
    print('-' * 10)
    print('Save to Mongo')
    result = input('Save above to Mongo <Y/n>?')

    if result in ['y', 'Y']:
        tagged_BoW.drop()
        taggedCorpus.drop()

        for s in cleanTaggedCorpusList:
            tmpSent = []
            for w in s:
                tmpSent.append({"word": w["word"], "tag": w["tag"]})
        
            taggedCorpus.insert_one({"taggedSentence": tmpSent})

        for t in cleanTagged_BoW_List:
            tagged_BoW.insert_one({"word": t[0], "tag":t[1]})

        print('Saved')
    else:
        print('Not saved')   

    print('- lowerCaseCheck End -')
    return


def nnxNotInKB(tagged_BoW, taggedCorpus, nnxKB):

    print('- nnxNotInKB Start -')

    totalNNX = 0
    foundNNX = 0
    notFound = 0

    taggedCorpusList = list(taggedCorpus.find())
    tagged_BoW_List = list(tagged_BoW.find())
    nnxKB_List = list(nnxKB.find())

    print('len BoW: ', len(tagged_BoW_List))
    print('len KB : ', len(nnxKB_List))

    for w in tagged_BoW_List:
        
        if w["tag"] == "NNP" or w["tag"] == "NN":
            totalNNX += 1
#            print("w: ", w)
            for nnx in nnxKB_List:
                if w["word"] == nnx["_id"]:
                    foundNNX += 1
#                    print("Found BoW w: ", w)
#                    print("In KB: ", nnx)
                
    notFound = totalNNX - foundNNX

    print('Found {} NNXs in KB'.format(foundNNX))
    print('{} NNXs not found in KB'.format(notFound))
    print('{} Total NNXs in BoWs'.format(totalNNX))

    print('- nnxNotInKB End -')

    return


#
#
if __name__ == "__main__":

    print('--- Start rectifyKB.py ---')

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]

#    lowerCaseCheck(tagged_BoW, taggedCorpus)

    nnxNotInKB(tagged_BoW, taggedCorpus, nnxKB)


    print('--- End   rectifyKB.py ---')
