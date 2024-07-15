# processSVOs.py
#
# Are the Subject and Objects in the existing KB(s)?
# If not: Build/add to unresolved/unproven KB(s)...~?
# Errors from SVO will only compound here--duh

import pickle
from collections import Counter
from findSVO3 import findSVO
from commonConfig import Sentence, nnx

PCP = 'data/processedCorpora.p'
PKBP = 'data/processedKB.p'
#FSVOP = 'data/foundSVO.p'
pickleFileOut = 'data/foundSVO.p'

def loadPickleData():

    with open(PCP, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    with open(PKBP, 'rb') as fp:
        kb = pickle.load(fp)
#        print('Aunt Bee loaded kb pickle.')
    fp.close()

#    with open(FSVOP, 'rb') as fp:
#        foundSVOs = pickle.load(fp)
#    fp.close()

    return corpora, kb


def whatDoWeKnowFromSpacy(corpora, kb):

    subjects = []
    verbs = []
    objects = []

    known = []
    unknown = []

    noSubjectSpacy = []
    noObjectSpacy = []

    for corpus in corpora:
        #print('bookName: ', c[0])
        for sent in corpus[1]:
            #i.printAll()
            if len(sent.subject) == 0:
                #print("No subject found via Spacy.")
                #print(sent.inputSent)
                #print(sent.taggedSent)
                noSubjectSpacy.append(sent)
            else:
                for s in sent.subject:
                    if (s not in subjects) and (s['pos'] != "PRON"):
                        subjects.append(s)

            if len(sent.object) == 0:
                #print("No object found via Spacy.")
                #print(sent.inputSent)
                #print(sent.taggedSent)
                noObjectSpacy.append(sent)
            else:
                for o in sent.object:
                    if (o not in objects) and (s['pos'] != "PRON"):
                        objects.append(o)
                        
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
                
    return known, unknown, noSubjectSpacy, noObjectSpacy


def makePendingKB(unknown):

    pendingKB = []
    justWords = []

    for u in unknown:
        pKB = {"word": u["word"],
                "tag": u["tag"],
                "isNonfiction": True,
                "isAlive": True,
                "canDo": "UNK",
                "superClass": "UNK"}

        #if (pKB not in pendingKB) and (pKB["tag"] in ["NN", "NNP"]) :
        if (pKB not in pendingKB) and (pKB["tag"] in nnx):
            pendingKB.append(pKB)

        # Look for dupilcate words 
        key_counts = Counter(d['word'] for d in pendingKB)
        uniqueValues = []
        duplicateValues = []
        for d in pendingKB:
            if key_counts[d['word']] == 1:
                uniqueValues.append(d)
            else:
                duplicateValues.append(d)

    for d in duplicateValues:
        print('dup: ', d)
            
    return pendingKB


def whatDoWeKnowFromFindSVO(foundSVOs, kb):

    subjects = []
    verbs = []
    objects = []
    
    knownSO = []
    unknownSO = []

    noSubjectSVO = []
    noObjectSVO = []

    for i in foundSVOs:
        #print('type: ', i.type)

        if i.subject == None:
            #print('No subject found:')
            #print(i.inputSent)
            #print(i.taggedSent)
            noSubjectSVO.append(i)
        else:
            for s in i.subject:
                #print('subject: ', s)

                if (s not in subjects) and (s['pos'] != "PRON"):
                        subjects.append(s)

        if i.object == None:
            #print('No object found: ')
            #print(i.inputSent)
            #print(i.taggedSent)
            noObjectSVO.append(i)
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
                knownSO.append(k)
    
    for s in objects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknownSO.append(s)

    return knownSO, unknownSO, noSubjectSVO, noObjectSVO


def findSVOs(corpora):
    newCorpora = []
    
    exitNow = False

    for corpus in corpora:
        objArr = []    
        bookName = corpus[0]
        bookText = corpus[1]
            
        tmpCnt = 0
        for s in bookText:
            tmpCnt += 1
            svoObj = findSVO(s.inputSent, s.taggedSent)
            objArr.append(svoObj)
            
        newCorpora.append((bookName, objArr))

    pickle.dump(newCorpora, open(pickleFileOut, "wb" ) )

    return newCorpora


def commonNoSubjects(noSubjectSpacy, noSubjectSVO):

    commonMissingSubjects = []

    for nSS in noSubjectSpacy:
        for nSSVO in noSubjectSVO:
            if nss.inputSent == nSSVO.inputSent:
                commonMissingSubjects.append(nSS)

    return commonMissingSubjects



def commonNoObjects(noObjectSpacy, noObjectSVO):

    commonMissingObjects = []

    for nOS in noObjectSpacy:
        for nOSVO in noObjectSVO:
            if nOS.inputSent == nOSVO.inputSent:
                commonMissingObjects.append(nOS)

    return commonMissingObjects


def mergeCorpora(corpora, foundSVOs):
    #
    # Create a new Sentence object with merged SVO data
    # from Spacy and findSVOs.
    #

    mergedCorpora = []

    for corpus in corpora: # Results from Spacy
        c_bookName = corpus[0]
        c_bookSentObjs = corpus[1]

        new_bookSentObjs = []
        for c_sentObj in c_bookSentObjs:
            for f_corpus in foundSVOs: # Results from findSVOs
                f_bookName = f_corpus[0]
                f_bookSentObjs = f_corpus[1]

                if c_bookName == f_bookName:        
                    for f_sentObj in f_bookSentObjs:
                        if c_sentObj.inputSent == f_sentObj.inputSent:
                            #print('c_sentObj.inputSent == f_sentObj.inputSent')
                            inputSent  = c_sentObj.inputSent
                            taggedSent = c_sentObj.taggedSent
                            sType      = f_sentObj.type # Spacy does not provide basic sentence type

                            # Check for subjects
                            if len(c_sentObj.subject) == 0 and isinstance(f_sentObj.subject, type(None)):
                                #print('len(c_sentObj.subject) == 0 and isinstance(f_sentObj.subject, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.subject)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.subject)
                                # Both are unknown
                                sSubj = c_sentObj.subject
                            elif len(c_sentObj.subject) > 0 and isinstance(f_sentObj.subject, type(None)):
                                #print('len(c_sentObj.subject) > 0 and isinstance(f_sentObj.subject, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.subject)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.subject)
                                # Only c_sentObj.subject is known
                                sSubj = c_sentObj.subject
                            elif len(c_sentObj.subject) == 0 and not isinstance(f_sentObj.subject, type(None)):
                                #print('len(c_sentObj.subject) == 0 and not isinstance(f_sentObj.subject, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.subject)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.subject)
                                # Only f_sentObj.subject is known
                                sSubj = f_sentObj.subject
                            else:
                                #print('else:')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.subject)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.subject)
                                # Both have something--ugh, more work...
                                sSubj = []
                                subjects = []
                                for sc in c_sentObj.subject:
                                    sSubj.append(sc)
                                    subjects.append(sc['word'])
                                for sf in f_sentObj.subject:
                                    if sf['word'] not in subjects:
                                        sSubj.append(sf)
                            #print('end subject')

                            # Check for verbs
                            if len(c_sentObj.verb) == 0 and isinstance(f_sentObj.verb, type(None)):
                                #print('len(c_sentObj.verb) == 0 and isinstance(f_sentObj.verb, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.verb)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.verb)
                                # Both are unknown
                                sVerb = c_sentObj.verb
                            elif len(c_sentObj.verb) > 0 and isinstance(f_sentObj.verb, type(None)):
                                #print('len(c_sentObj.verb) > 0 and isinstance(f_sentObj.verb, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.verb)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.verb)
                                # Only c_sentObj.verb is known
                                sVerb = c_sentObj.verb
                            elif len(c_sentObj.verb) == 0 and not isinstance(f_sentObj.verb, type(None)):
                                #print('len(c_sentObj.verb) == 0 and not isinstance(f_sentObj.verb, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.verb)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.verb)
                                # Only f_sentObj.verb is known
                                sVerb = f_sentObj.verb
                            else:
                                #print('else:')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.verb)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.verb)
                                # Both have something--ugh, more work...
                                sVerb = []
                                verbs = []
                                for vc in c_sentObj.verb:
                                    sVerb.append(vc)
                                    verbs.append(vc['word'])
                                for vf in f_sentObj.verb:
                                    if vf['word'] not in verbs:
                                        sVerb.append(vf)
                            #print('end of verb')

                            # Check for objects
                            if len(c_sentObj.object) == 0 and isinstance(f_sentObj.object, type(None)):
                                #print('len(c_sentObj.object) == 0 and isinstance(f_sentObj.object, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.object)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.object)
                                # Both are unknown
                                sObj = c_sentObj.object
                            elif len(c_sentObj.object) > 0 and isinstance(f_sentObj.object, type(None)):
                                #print('len(c_sentObj.object) > 0 and isinstance(f_sentObj.object, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.object)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.object)
                                # Only c_sentObj.object is known
                                sObj = c_sentObj.object
                            elif len(c_sentObj.object) == 0 and not isinstance(f_sentObj.object, type(None)):
                                #print('len(c_sentObj.object) == 0 and not isinstance(f_sentObj.object, type(None))')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.object)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.object)
                                # Only f_sentObj.object is known
                                sObj = f_sentObj.object
                            else:
                                #print('else:')
                                #print(c_sentObj.inputSent)
                                #print(c_sentObj.object)
                                #print(f_sentObj.inputSent)
                                #print(f_sentObj.object)
                                # Both have something--ugh, more work...
                                sObj = []
                                objects = []
                                for oc in c_sentObj.object:
                                    sObj.append(oc)
                                    objects.append(oc['word'])
                                for of in f_sentObj.object:
                                    if of['word'] not in objects:
                                        sObj.append(of)
                            #print('end object')

                            new_bookSent = Sentence(inputSent, taggedSent, sType, sSubj, sVerb, sObj)
                            #new_bookSent.printAll()

                            new_bookSentObjs.append(new_bookSent)
        #print('---')

        mergedCorpora.append((c_bookName, new_bookSentObjs))

    return mergedCorpora


def whatDoWeKnow(mergedCorpora, kb):

    subjects = []
    verbs = []
    objects = []

    known = []
    unknown = []

    noSubject = []
    noObject = []

    for corpus in mergedCorpora:
        #print('bookName: ', c[0])
        for sent in corpus[1]:
            #i.printAll()
            if len(sent.subject) == 0:
                #print("No subject found via Spacy.")
                #print(sent.inputSent)
                #print(sent.taggedSent)
                noSubject.append(sent)
            else:
                for s in sent.subject:
                    if (s not in subjects) and (s['pos'] != "PRON"):
                        subjects.append(s)

            if len(sent.object) == 0:
                #print("No object found via Spacy.")
                #print(sent.inputSent)
                #print(sent.taggedSent)
                noObject.append(sent)
            else:
                for o in sent.object:
                    if (o not in objects) and (s['pos'] != "PRON"):
                        objects.append(o)
                        
    tmpSub = []   
    for s in subjects:
        for k in kb:
            #print('s: {}, k[word]: {}'.format(s, k['word']))
            if s['word'] == k['word']:
                #print('KNOWN: ', k)
                if s['word'] not in tmpSub:
                    print('ADDING KNOWN: ', k)
                    tmpSub.append(s['word'])
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
                if s['word'] not in tmpSub:
                    known.append(k)
    
    for s in objects:
        for i in known:
            if s['word'] != i['word']:
                #print('UNKNOWN: ', s)
                unknown.append(s)

    

    return known, unknown


#
#
#
if __name__ == "__main__":

    print("Start: processSVOs...")

    corpora, kb = loadPickleData()

    # First determine any missing subjects or objects
    # from both Spacy and findSVO, and merge.

    corporaSVO = findSVOs(corpora)

    # Fill (merge) empty SVOs with non-empty 
    mergedCorpora = mergeCorpora(corpora, corporaSVO)

    print('=========')
    for corpus in mergedCorpora:
        print(corpus)
        bookName = corpus[0]
        bookSents = corpus[1]
        print(bookName)
        for s in bookSents:
            s.printAll()
            print('....')
        print('----')


    known, unknown = whatDoWeKnow(mergedCorpora, kb)

    print('whatWeKnow info:')
    print('-----------------')
    for i in known:
        print('KNOWN: ', i)

    print('-----------------')
    for i in unknown:
        print('UNKNOWN: ', i)


    pendingKB = makePendingKB(unknown)

    print('-----------------')
    for i in pendingKB:
        print('PENDING: ', i)
    

#    known, unknown, noSubjectSpacy, noObjectSpacy = whatDoWeKnowFromSpacy(corpora, kb)
#
#    pendingKB = makePendingKB(unknown)
#
#    print('From Spacy info:')
#    print('-----------------')
#    for i in known:
#        print('KNOWN: ', i)
#
#    print('-----------------')
#    for i in unknown:
#        print('UNKNOWN: ', i)
#
#    print('-----------------')
#    for i in pendingKB:
#        print('PENDING: ', i)
#
#    print('=================')
#    print('From findSVO info:')   
#    print('-----------------')
#    #for i in foundSVOs:
#    #    print('i: ', i)
#    #    i.printAll()
#    
#    knownSOs, unknownSOs, noSubjectSVO, noObjectSVO = whatDoWeKnowFromFindSVO(foundSVOs, kb)
#
#    
#    pendingKBx = makePendingKB(unknownSOs)
#
#    print('-----------------')
#    for i in knownSOs:
#        print('KNOWN: ', i)
#
#    print('-----------------')
#    for i in unknownSOs:
#        print('UNKNOWN: ', i)
#
#    print('-----------------')
#    for i in pendingKBx:
#        print('PENDING: ', i)
#
#    print('=================')
#    for ns in noSubjectSpacy:
#        ns.printAll()
#    print('-----------------')
#    for no in noObjectSpacy:
#        no.printAll()
#        print('----')
#        
#    print('=================')
#    for ns in noSubjectSVO:
#        ns.printAll()
#    print('-----------------')
#    for no in noObjectSVO:
#        no.printAll()
#        print('----')
#
#    commonMissingSubjects = commonNoSubjects(noSubjectSpacy, noSubjectSVO)
#
#    commonMissingObjects = commonNoObjects(noObjectSpacy, noObjectSVO)
#
#    print('commonMissingSubjects -----------------')
#    for ns in commonMissingSubjects:
#        ns.printAll()
#        print('----')
#
#    print('commonMissingObjects -----------------')
#    for no in commonMissingObjects:
#        no.printAll()
#        print('----')
#
#
    print("Completed: processSVOs.")
