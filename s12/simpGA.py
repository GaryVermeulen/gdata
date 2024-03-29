#
# simpGA.py
#
#   Grammar analysis of current corpus
# This evolved into a KB checker and doesn't really do any
# Grammar analysis, so saved as kbChecker.py
#


from commonConfig import verbose
from commonConfig import Sentence
from commonConfig import kbResults

from commonUtils import connectMongo
from commonUtils import getInflectionTag
from commonUtils import getInflections


def getVerbInflections(verbsAndTags):

    inflections = []
#    print('getVerbInflections: ', verbsAndTags)

    for verb in verbsAndTags:
        v = verb[0]
        t = verb[1]

        tag = getInflectionTag(t)

        inflections.append(getInflections(v, tag))

#        print('inflections: ', inflections)

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
            print('MATCH')
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

    print('sVerbs: ', sVerbs)
    print('nnxKB: ', nnxKB)
    print('nnxCanDo: ', nnxCanDo)
    nnxCanDoSet = set(nnxCanDo)
    print('nnxCanDoSet: ', nnxCanDoSet)

    if len(sVerbs) == 0:
        print('No sVerbs: ', sVerbs)
        return ['No Verb(s) Given'], ['No Verb(s) Given']
    
    for verb in sVerbs:
        print('verb: ', verb)

        verbSet = set(verb)
        intersect = verbSet.intersection(nnxCanDoSet)

        print(type(intersect))
        print(intersect)

        canDoTmp = []
        cannotDoTmp = []

        if len(intersect) == 0:
            #cannotDoTmp.append(verb)
            cannotDo.append(verb)
        else:
            #canDoTmp = ', '.join(intersect)
            #print(type(canDoTmp))
            #print('canDoTmp: ', canDoTmp)
            canDo.append(verb)

    print(canDo)
    print(cannotDo)
    print('End --- canDoMatch ---')    
    return canDo, cannotDo


def chkGrammar(sA_Obj, subjectCorpus, subjectsKB, simpKB):

    # Ever evolving...
    
    print('------ start chkGrammar ------')

    simpCanX = []
    subjectsCanX = []

    if sA_Obj == None:
        return None

    # Has this been said before?
    #if saidBefore(sA_Obj, subjectCorpus):
    said = saidBefore(sA_Obj, subjectCorpus)
    if said:
        print('Said before: ', sA_Obj.inSent)
    else:
        print('New input: ', sA_Obj.inSent)

    # Get input sentence verbs and their inflections
    allVerbs = getVerbInflections(sA_Obj.getVerbsAndTags())
    print('allVerbs: ', allVerbs)

    # If imperative, can Simp do what is asked?
    if sA_Obj.sType == 'imperative':
        canDo, cannotDo = canDoMatch(allVerbs, simpKB)
        
        print('Simp can: ', canDo)
        print('Simp cannot: ', cannotDo)
        simpCanX.append(simpKB["_id"])
        simpCanX.append(canDo)
        simpCanX.append(cannotDo)
        print('simpCanX:')
        print(simpCanX)
    else:
        print('Not imperative')

    # Can the subject do (canDo) what is said (subject canDo match verbs)?
    sVerbs = sA_Obj.getVerbs()
    sVerbsAndTags = sA_Obj.getVerbsAndTags()
    
    for subj in subjectsKB:
        if len(subj) > 0:
            canDo, cannotDo = canDoMatch(allVerbs, subj)
            subjName = subj["_id"]
            
            print('(subjName) {} can {}'.format(subjName, canDo))
            print('(subjName) {} cannot {}'.format(subjName, cannotDo))

            subjCanX = []
            subjCanX.append(subjName)
            subjCanX.append(canDo)
            subjCanX.append(cannotDo)
            subjectsCanX.append(subjCanX)

    print('subjectsCanX:')
    print(subjectsCanX)

    kbRes_Obj = kbResults(sA_Obj.inSent, said, simpCanX, subjectsCanX)

    print('------ end chkGrammar ------')
    return kbRes_Obj


if __name__ == "__main__":

    print("simpGA.py: must call chkGrammar from other py file.")
        
