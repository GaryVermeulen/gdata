#
# kbChecker.py
#
# Was: simpGA.py
#
#   Grammar analysis of current corpus
# This evolved into a KB checker which adds to
# a kbResults object and doesn't really do any
# Grammar analysis, so saved as kbChecker.py
#


from commonConfig import verbose
from commonConfig import simp
#from commonConfig import Sentence
from commonConfig import kbResults

from commonUtils import connectMongo
from commonUtils import getInflectionTag
from commonUtils import getInflections
from commonUtils import chk_nnxKB
from commonUtils import chkCorpus



def getSimpKB(nnxKB):


    # Retrieve Simp KB
    simpKB = chk_nnxKB(simp, nnxKB)
    print('-' * 5)
    print(simpKB)
    print(simpKB["_id"])
    print(simpKB["similar"])
    print(simpKB["tag"])
    print(simpKB["isAlive"])
    print(simpKB["canDo"])
    print(simpKB["superclass"])

    return simpKB


def getSubjectsCorpus(sA_Obj, untaggedCorpus):

    # Check corpus for subject
    print('-' * 10)
    print('Checking corpus for: ', sA_Obj.getSubjects())
    subjectsCorpus = chkCorpus(sA_Obj.getSubjects(), untaggedCorpus)
    print('chkCorpus returned:')
    print(subjectsCorpus)

    return subjectsCorpus


def getSubjectsKB(sA_Obj, nnxKB):

    # Subject(s) KB check--are the subjects in the KB?
    subjectsInKB = []
    subjectsNotInKB = []
        
    if len(sA_Obj.sSubj) == 0:
        print('Something is wrong: No subject returned.')
    else:
        print('Checking KB for subject(s):', sA_Obj.sSubj)

        if isinstance(sA_Obj.sSubj, tuple):     # Just one subkect
            print('Processing single subject.')
            subjectKB = chk_nnxKB(sA_Obj.sSubj[0], nnxKB)
            print('subjectKB: ', subjectKB)

            if len(subjectKB) > 0:
                subjectsInKB.append(subjectKB)
            else:
                subjectsNotInKB.append(sA_Obj.sSubj[0])
            
        elif isinstance(sA_Obj.sSubj, list):    # multiple subjects
            print('Processing multiple subjects.')
            for sub in sA_Obj.sSubj:
                subjectKB = chk_nnxKB(sub[0], nnxKB)
                print('subjectKB: ', subjectKB)

                if len(subjectKB) > 0:
                    subjectsInKB.append(subjectKB)
                else:
                    subjectsNotInKB.append(sub[0])
    
        else:
            print('Unexpected subject type encountered: ', sA_Obj.sSubj[0])

    print('subjectsInKB: ', subjectsInKB)
    print('subjectsNotInKB: ', subjectsNotInKB)

    return subjectsInKB, subjectsNotInKB


def getObjectsKB(sA_Obj, nnxKB):
    # Object(s) KB check--are the objects in the KB?
    objectsInKB = []
    objectsNotInKB = []
        
    if len(sA_Obj.sObj) == 0:
        print('Something is wrong: No object returned.')
    else:
        print('Checking KB for object(s):', sA_Obj.sObj)

        if isinstance(sA_Obj.sObj, tuple):     # Just one object
            print('Processing single object.')
            objectKB = chk_nnxKB(sA_Obj.sObj[0], nnxKB)
            print('objectKB: ', objectKB)

            if len(objectKB) > 0:
                objectsInKB.append(objectKB)
            else:
                objectsNotInKB.append(sA_Obj.sObj[0])
            
        elif isinstance(sA_Obj.sObj, list):    # multiple objects
            print('Processing multiple objects.')
            for obj in sA_Obj.sObj:
                objectKB = chk_nnxKB(obj[0], nnxKB)
                print('objectKB: ', objectKB)

                if len(objectKB) > 0:
                    objectsInKB.append(objectKB)
                else:
                    objectsNotInKB.append(obj[0])
    
        else:
            print('Unexpected object type encountered: ', sA_Obj.sObj[0])

    print('objectsInKB: ', objectsInKB)
    print('objectsNotInKB: ', objectsNotInKB)

    return objectsInKB, objectsNotInKB


def getIndObjectsKB(sA_Obj, nnxKB):
    # Indirect object(s) KB check--are the indirect objects in the KB?
    indObjectsInKB = []
    indObjectsNotInKB = []
        
    if len(sA_Obj.sInObj) == 0:
        print('Something may be wrong: No indirect object returned.')
    else:
        print('Checking KB for indirect object(s):', sA_Obj.sInObj)

        if isinstance(sA_Obj.sInObj, tuple):     # Just one indirect object
            print('Processing single indirect object.')
            indObjectKB = chk_nnxKB(sA_Obj.sInObj[0], nnxKB)
            print('indObjectKB: ', indObjectKB)

            if len(indObjectKB) > 0:
                indObjectsInKB.append(indObjectKB)
            else:
                indObjectsNotInKB.append(sA_Obj.sInObj[0])
            
        elif isinstance(sA_Obj.sInObj, list):    # multiple indirect objects
            print('Processing multiple indirect objects.')
            for indObj in sA_Obj.sInObj:
                indObjectKB = chk_nnxKB(indObj[0], nnxKB)
                print('indObjectKB: ', indObjectKB)

                if len(indObjectKB) > 0:
                    indObjectsInKB.append(indObjectKB)
                else:
                    indObjectsNotInKB.append(indObj[0])
    
        else:
            print('Unexpected indirect object type encountered: ', sA_Obj.sInObj[0])

    print('indObjectsInKB: ', indObjectsInKB)
    print('indObjectsNotInKB: ', indObjectsNotInKB)

    return indObjectsInKB, indObjectsNotInKB


def getVerbInflections(verbsAndTags):

    inflections = []
#    print('getVerbInflections: ', verbsAndTags)

    for verb in verbsAndTags:
        v = verb[0]
        t = verb[1]

        tag = getInflectionTag(t)
        inflections.append(getInflections(v, tag))

        #inflections.append(getInflections(v, t))

        #i = getInflections(v, tag)
        #print('getVerbInflections -> i: ', i)

    return inflections


def saidBefore(sA_Obj, taggedCorpus):

    tmpInSent = ''
    result = False
    
    for w in sA_Obj.inSent:
        if tmpInSent == '':
            tmpInSent = tmpInSent + w[0]
        else:
            tmpInSent = tmpInSent + ' ' + w[0]

    for s in taggedCorpus:
        tmpSent = ' '.join(s)
        if tmpInSent == tmpSent:
#            print('MATCH')
#            print('tmpInSent: ', tmpInSent)
#            print('tmpSent: ', tmpSent)
            result = True

    return result


def getMacthedTagSent(sA_Obj, taggedCorpus):

    inputWords = []
    inputTags = []
    
    for w in sA_Obj.inSent:
        inputWords.append(w[0])
        inputTags.append(w[1])

    for s in taggedCorpus:
        sWords = []
        sTags = []
        for w in s:
            sWords.append(w[0])
            sTags.append(w[1])
        
        if sTags == inputTags:
            tagsMatch = True
            sCopy = s.copy()

    return sCopy


def canDoMatch(sVerbs, nnxKB):

    print('Start --- canDoMatch ---')

    canDo = []
    cannotDo = []
    nnxCanDo = nnxKB["canDo"].split(',')

#    print('sVerbs: ', sVerbs)
#    print('nnxKB: ', nnxKB)
    print('nnxCanDo: ', nnxCanDo)
    nnxCanDoSet = set(nnxCanDo)
    print('nnxCanDoSet: ', nnxCanDoSet)
    print('nnxKB isAlive: ', nnxKB["isAlive"])

    if len(sVerbs) == 0:
        print('No sVerbs: ', sVerbs)
        return ['No Verb(s) Given'], ['No Verb(s) Given']
    
    for verb in sVerbs:
        print('verb: ', verb)
        print(type(verb))
        print(len(verb))
        
        if 'be' in verb: # For now a free pass to canDo
            print('be in verb')
            canDo.append(verb)
        else:
            verbSet = set(verb)
            intersect = verbSet.intersection(nnxCanDoSet)

            print('intersect:', intersect)

            if len(intersect) == 0:
                #cannotDoTmp.append(verb)
                cannotDo.append(verb)
            else:
                #canDoTmp = ', '.join(intersect)
                #print(type(canDoTmp))
                #print('canDoTmp: ', canDoTmp)
                canDo.append(verb)

    print('canDo: ', canDo)
    print('cannotDo: ', cannotDo)
    print('End --- canDoMatch ---')    
    return canDo, cannotDo


def makeGuess(subjectsCorpus):

    myGuess = 'NOT YET'
    
    return myGuess


def chkKB(sA_Obj, nnxKB, untaggedCorpus):

    # Ever evolving...
    
    print('------ start chkKB ------')

    simpCanX = []
    simpAlive = 'UNKNOWN'
    subjectsCanX = []
    subjectsAlive = []
    allVerbs = []

    if sA_Obj == None:
        return None

    # Get simp from KB
    simpKB = getSimpKB(nnxKB)

    # Get the subjects KB 
    subjectsInKB, subjectsNotInKB = getSubjectsKB(sA_Obj, nnxKB)

    # Get the objects
    objectsInKB, objectsNotInKB = getObjectsKB(sA_Obj, nnxKB)

    # Get the indiret objects
    indObjectsInKB, indObjectsNotInKB = getIndObjectsKB(sA_Obj, nnxKB)

    # Are the subjects within the corpus?
    #    What about secondary subjects?
    #    What about objects?
    subjectsCorpus = getSubjectsCorpus(sA_Obj, untaggedCorpus)

    # Has this been said before?
    said = saidBefore(sA_Obj, subjectsCorpus)
    if said:
        print('Said before: ', sA_Obj.inSent)
    else:
        print('New input: ', sA_Obj.inSent)

    # Can we make any predictions with "subjects" found in the corpus? 

    myGuess = makeGuess(subjectsCorpus)


    # Get input sentence verbs and their inflections
    print('sA_Obj.getVerbsAndTags():')
    print(sA_Obj.getVerbsAndTags())
    allVerbRecords = getVerbInflections(sA_Obj.getVerbsAndTags())
    print('allVerbRecords: ', allVerbRecords)
    for verbs in allVerbRecords:
        print(type(verbs))
        print('verbs: ', verbs)
        
        
#        allVerbs.append(verbs["inflections"])
#    print('allVerbs: ', allVerbs)


    # If imperative, can Simp do what is asked?
    if sA_Obj.sType == 'imperative':
        simpAlive = simpKB["isAlive"]
        canDo, cannotDo = canDoMatch(allVerbRecords, simpKB)
        
#        print('Simp can: ', canDo)
#        print('Simp cannot: ', cannotDo)
        simpCanX.append(simpKB["_id"])
        simpCanX.append(canDo)
        simpCanX.append(cannotDo)
#        print('simpCanX:')
#        print(simpCanX)
    else:
        print('sType not imperative, so Simp does not care...')

    # Can the subject do (canDo) what is said (subject canDo match verbs)?
#    sVerbs = sA_Obj.getVerbs()
#    sVerbsAndTags = sA_Obj.getVerbsAndTags()
    
    for subj in subjectsInKB:
        if len(subj) > 0:
#            canDo, cannotDo = canDoMatch(allVerbs, subj)
            canDo, cannotDo = canDoMatch(allVerbRecords, subj)
            subjName = subj["_id"]
            
#            print('(subjName) {} can {}'.format(subjName, canDo))
#            print('(subjName) {} cannot {}'.format(subjName, cannotDo))

            subjAlive = []
            subjAlive.append(subjName)
            subjAlive.append(subj["isAlive"])
            subjectsAlive.append(subjAlive)

            subjCanX = []
            subjCanX.append(subjName)
            subjCanX.append(canDo)
            subjCanX.append(cannotDo)
            subjectsCanX.append(subjCanX)

            

#    print('subjectsCanX:')
#    print(subjectsCanX)

    kbRes_Obj = kbResults(sA_Obj.inSent, None, None, None, subjectsInKB, subjectsNotInKB, said, simpCanX.copy(), simpAlive, subjectsCanX.copy(), subjectsAlive.copy())

#    kb_Obj.saidBefore = said
    #kb_Obj.simpCanX = simpCanX.copy()
    #kb_Obj.subjectsCanX = subjectsCanX.copy()

    print('------ end chkKB ------')
    return kbRes_Obj


if __name__ == "__main__":

    print("kbChecker.py: must call chkKB from other py file.")
        