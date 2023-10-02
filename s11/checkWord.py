#
# checkWord.py
#
# Check Bow, taggedCorpus, and KB for a given word.

from commonUtils import connectMongo

def checkWord(word):

    print('--- Start checkWord ---')

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]

    taggedCorpusList = list(taggedCorpus.find())
    tagged_BoW_List = list(tagged_BoW.find())
    nnxKB_List = list(nnxKB.find())

    if word == None or word == '':
        word = input('Enter word: ')

    print('Searching BoWs for: ', word)
    bow = {"bow": False}
    for w in tagged_BoW_List:
        if word == w["word"]:
            print("Found {} in BoWs".format(word))
            print(w)
            bow = {"bow": True}
    print('-' * 10)
    taggedCorpus = {"taggedCorpus": False}
    print('Searching tagged corpus for: ', word)
    for s in taggedCorpusList:
        #print(s)
        for w in s["taggedSentence"]:
            #print(w)
            if word == w["word"]:
                print("Found {} in tagged corpus".format(word))
                print(s)
                taggedCorpus = {"taggedCorpus": True}
    print('-' * 10)
    kb = {"kb": False}
    print('Searching KB for: ', word)
    for k in nnxKB_List:
        if word == k["_id"]:
            print("Found {} in KB".format(word))
            print(k)
            kb = {"kb": True}

    results = (bow, taggedCorpus, kb)
    print('--- End checkWord ---')

    return results


if __name__ == "__main__":


    print('--- Start checkWord.py __main__ ---')

    word = input('Enter word: ')
    results = checkWord(word)
    print('\nResults:')
    print(results)
    
    print('\n--- End checkWord.py __main__ ---')
