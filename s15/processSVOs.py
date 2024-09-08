# processSVOs.py
#
# Supplement to Space; Find missing SVOs, and
# check for consistency.


import pickle
from collections import Counter
from findSVO import findSVO
from commonConfig import Sentence
from resolvePronouns import resolvePronouns


pickleInputFile = 'pickleJar/taggedCorpora.p'
pickleFileOut = 'pickleJar/processedCorporaSVO.p'

def loadPickleData():

    with open(pickleInputFile, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    return corpora


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
            #svoObj = findSVO(s.inputSent, s.taggedSentLong)
            svoObj = findSVO(s.inputSent, s.epistropheSent)
            objArr.append(svoObj)
            
        newCorpora.append((bookName, objArr))

#    pickle.dump(newCorpora, open(pickleFileOut, "wb" ) )

    return newCorpora


def mergeCorpora(corpora, foundSVOs):

    mergedCorpora = []

    # First let's just see what we have...
    # for corpus in corpora

    for corpus in corpora:
        c_bookName = corpus[0]
        c_bookSentObjs = corpus[1]
        tmpBook = []
        for c_sentObj in c_bookSentObjs:
            #c_sentObj.printAll()

            for f_corpus in foundSVOs:
                #print(f_corpus)
                f_bookName = f_corpus[0]
                f_bookSentObjs = f_corpus[1]
                
                if c_bookName == f_bookName:

                    new_bookSentObjs = []
                    
                    for f_sentObj in f_bookSentObjs:
                        if c_sentObj.inputSent == f_sentObj.inputSent:
                            #print('c_sentObj.inputSent == f_sentObj.inputSent')
                            inputSent       = c_sentObj.inputSent
                            taggedSentShort = c_sentObj.taggedSentShort
                            taggedSentLong  = c_sentObj.taggedSentLong
                            epistropheSent  = c_sentObj.epistropheSent
                            sType           = f_sentObj.type # Spacy does not provide basic sentence type

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

                            new_bookSent = Sentence(inputSent, taggedSentShort, taggedSentLong, epistropheSent, sType, sSubj, sVerb, sObj)
                            new_bookSent.printAll()

                            new_bookSentObjs.append(new_bookSent)
                            #print('---')

                    #mergedCorpora.append((c_bookName, new_bookSentObjs))
                    tmpBook.append(new_bookSent)
        mergedCorpora.append([c_bookName, tmpBook])
                    

    return mergedCorpora


#
#
#
if __name__ == "__main__":

    print("Start: processSVOs...")

    corpora = loadPickleData()

    # Resolve pronouns
    resolvedCorpora = resolvePronouns(corpora)

    # Determine any missing subjects or objects
    # from both Spacy and findSVO, and merge.

    newCorpora = findSVOs(resolvedCorpora)

#    for corpus in newCorpora:
#        print(corpus[0])
#        for sent in corpus[1]:
#            sent.printAll()


    # Fill (merge) empty subject and object with non-empty 
    mergedCorpora = mergeCorpora(corpora, newCorpora)
    #
    for corpus in mergedCorpora:
        print(corpus[0])
        for sent in corpus[1]:
            sent.printAll()

    # Save mergedCorpora
    with open(pickleFileOut, "wb") as f:
        pickle.dump(mergedCorpora, f)
    

    print("Completed: processSVOs.")
