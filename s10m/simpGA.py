#
# simpGA.py
#
#   Grammar analysis of current corpus
#


from commonConfig import verbose
from commonConfig import Sentence

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

    canDo = []
    cannotDo = []
    nnxCanDo = nnxKB["canDo"].split(',')

#    print('sVerbs: ', sVerbs)
#    print('nnxKB: ', nnxKB)
#    print('nnxCanDo: ', nnxCanDo)
    nnxCanDoSet = set(nnxCanDo)
#    print('nnxCanDoSet: ', nnxCanDoSet)

    if len(sVerbs) == 0:
        print('No sVerbs: ', sVerbs)
        return ['No Verb(s) Given'], ['No Verb(s) Given']
    
    for verb in sVerbs:
#        print('verb: ', verb)

        verbSet = set(verb)
        intersect = verbSet.intersection(nnxCanDoSet)

        canDoTmp = []
        cannotDoTmp = []

        if len(intersect) == 0:
            cannotDoTmp.append(verb)
            cannotDo.append(cannotDoTmp)
        else:
            canDoTmp = list(intersect)
            canDo.append(canDoTmp)
        
    return canDo, cannotDo


def chkGrammar(sA_Obj, subjectCorpus, subjectsKB, simpKB):

    # Ever evolving...
    
    print('------ start chkGrammar ------')

    if sA_Obj == None:
        return None

    # Has this been said before?
    if saidBefore(sA_Obj, subjectCorpus):
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
    else:
        print('Not imperative')

    # Can the subject do (canDo) what is said (subject canDo match verbs)?
    sVerbs = sA_Obj.getVerbs()
#    print('sVerbs: ', sVerbs)

    sVerbsAndTags = sA_Obj.getVerbsAndTags()
#    print('sVerbsAndTags: ', sVerbsAndTags)
  
#    print('subjectsKB type: ', type(subjectsKB))
#    print('subjectsKB: ', subjectsKB)
    
    for subj in subjectsKB:
#        print('---')
        if len(subj) > 0:
            #print('subj: ', subj)
            #subjCanDo = set(subj["canDo"].split(','))
            #print('subjCanDo: ', subjCanDo)

            canDo, cannotDo = canDoMatch(allVerbs, subj)

            """
            intersect = subjCanDo.intersection(sVerbs)
            print('intersect: ', intersect)
            """
            subjName = subj["_id"]
            
            print('(subjName) {} can {}'.format(subjName, canDo))
            print('(subjName) {} cannot {}'.format(subjName, cannotDo))
        

    print('------ end chkGrammar ------')
    return 'nope'


if __name__ == "__main__":

    print("simpGA.py: must call chkGrammar from other py file.")
        
