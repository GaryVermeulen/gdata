# processSO.py
#
# Are the Subject and Objects in the existing KB(s)?
# If not: Build/add to unresolved/unproven KB(s)...~?
# Errors from SVO will only compound here!

import pickle

PCP = 'data/processedCorpora.p'
PKBP = 'data/processedKB.p'


def loadPickleData():

    with open(PCP, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    with open(PKBP, 'rb') as fp:
        kb = pickle.load(fp)
#        print('Aunt Bee loaded kb pickle.')
    fp.close()

    return corpora, kb


def whatDoWeKnow(corpora, kb):

    subjects = []
    verbs = []
    objects = []

    known = []
    unknown = []

    for c in corpora:
        #print('bookName: ', c[0])
        for i in c[1]:
            #i.printAll()
            for s in i.subject:
                if (s not in subjects) and (s['pos'] != "PRON"):
                        subjects.append(s)

            for s in i.object:
                if (s not in objects) and (s['pos'] != "PRON"):
                        objects.append(s)

                        
    for s in subjects:
        for k in kb:
            #print('s: {}, k[word]: {}'.format(s, k['word']))
            if s['word'] == k['word']:
                #print('KNOWN: ', k)
                known.append(k)
    
    for s in subjects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknown.append(s)

    for s in objects:
        for k in kb:
            #print('s: {}, k[word]: {}'.format(s, k['word']))
            if s['word'] == k['word']:
                #print('KNOWN: ', k)
                known.append(k)
    
    for s in objects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknown.append(s)
                

    return known, unknown


def makePendingKB(unknown):

    pendingKB = []

    for u in unknown:
        pKB = {"word": u["word"],
                "tag": u["tag"],
                "isNonfiction": True,
                "isAlive": True,
                "canDo": "UNK",
                "superClass": "UNK"}

        if (pKB not in pendingKB) and (pKB["tag"] in ["NN", "NNP"]) :
            pendingKB.append(pKB)


    return pendingKB

#
#
#
if __name__ == "__main__":

    print("Start: processSO...")


    corpora, kb = loadPickleData()

    known, unknown = whatDoWeKnow(corpora, kb)

    pendingKB = makePendingKB(unknown)
    
    print('-----------------')
    for i in known:
        print('KNOWN: ', i)

    print('-----------------')
    for i in unknown:
        print('UNKNOWN: ', i)

    print('-----------------')
    for i in pendingKB:
        print('PENDING: ', i)


    print("Completed: processSO.")
