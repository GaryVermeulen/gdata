# processSO.py
#
# Are the Subject and Objects in the existing KB(s)?
# If not: Build/add to unresolved/unproven KB(s)...~?
# Errors from SVO will only compound here!

import pickle
import findSVO

PCP = 'data/processedCorpora.p'
PKBP = 'data/processedKB.p'
FSVOP = 'data/foundSVO.p'

def loadPickleData():

    with open(PCP, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    with open(PKBP, 'rb') as fp:
        kb = pickle.load(fp)
#        print('Aunt Bee loaded kb pickle.')
    fp.close()

    with open(FSVOP, 'rb') as fp:
        foundSVOs = pickle.load(fp)
    fp.close()

    return corpora, kb, foundSVOs


def whatDoWeKnowFromSpacy(corpora, kb):

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


def whatDoWeKnowFromFindSVO(foundSVOs, kb):

    subjects = []
    verbs = []
    objects = []
    
    knownSO = []
    unknownSO = []

    for i in foundSVOs:
        #print('type: ', i.type)

        if i.subject == None:
            print('subject: None')
        else:
            for s in i.subject:
                #print('subject: ', s)

                if (s not in subjects) and (s['pos'] != "PRON"):
                        subjects.append(s)

        if i.object == None:
            print('object: None')
        else:
            for o in i.object:
                #print('object: ', o)

                if (o not in objects) and (o['pos'] != "PRON"):
                        objects.append(o)

    for s in subjects:
        for k in kb:
            #print('s: {}, k[word]: {}'.format(s, k['word']))
            if s['word'] == k['word']:
                #print('KNOWN: ', k)
                knownSO.append(k)
    
    for s in subjects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknownSO.append(s)

    for s in objects:
        for k in kb:
            #print('s: {}, k[word]: {}'.format(s, k['word']))
            if s['word'] == k['word']:
                #print('KNOWN: ', k)
                knownSo.append(k)
    
    for s in objects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknownSO.append(s)    


    return knownSO, unknownSO



#
#
#
if __name__ == "__main__":

    print("Start: processSVOs...")


    corpora, kb, foundSVOs = loadPickleData()

    known, unknown = whatDoWeKnowFromSpacy(corpora, kb)

    pendingKB = makePendingKB(unknown)

    print('From Spacy info:')
    print('-----------------')
    for i in known:
        print('KNOWN: ', i)

    print('-----------------')
    for i in unknown:
        print('UNKNOWN: ', i)

    print('-----------------')
    for i in pendingKB:
        print('PENDING: ', i)

    print('From findSVO info:')   
    print('-----------------')
    #for i in foundSVOs:
    #    print('i: ', i)
    #    i.printAll()
    
    knownSOs, unknownSOs = whatDoWeKnowFromFindSVO(foundSVOs, kb)

    
    pendingKBx = makePendingKB(unknownSOs)

    print('-----------------')
    for i in knownSOs:
        print('KNOWN: ', i)

    print('-----------------')
    for i in unknownSOs:
        print('UNKNOWN: ', i)

    print('-----------------')
    for i in pendingKBx:
        print('PENDING: ', i)
        
    

    print("Completed: processSVOs.")
