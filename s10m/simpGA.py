#
# simpGA.py
#
#   Grammar analysis of current corpus
#

#from nltk.tag import pos_tag
#from nltk.tokenize import word_tokenize

#from commonUtils import loadPickle


from commonConfig import verbose
from commonConfig import Sentence

from commonUtils import connectMongo
from commonUtils import getInflectionTag
from commonUtils import getInflections



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
            print('tmpInSent: ', tmpInSent)
            print('tmpSent: ', tmpSent)
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


def canDoMatch(sVerb, simpKB):

    canDo = []
    cannotDo = []
    simpCanDo = simpKB["canDo"].split(',')

    print('sVerb: ', sVerb)
    print('Simp canDo: ', simpCanDo)

    if sVerb == '':
        print('No sVerb: ', sVerb)
        return ['No Verb Given'], ['No Verb Given']
    
    for verb in sVerb:
        if verb in simpCanDo:
            canDo.append(verb)
        else:
            cannotDo.append(verb)

    return canDo, cannotDo


def chkGrammar(sA_Obj, subjectCorpus, subjectsKB, simpKB):

    # Not sure about this idea anymore???

    
    
    
    print('------ start chkGrammar ------')

    if sA_Obj == None:
        return None

    # Has this been said before?
    if saidBefore(sA_Obj, subjectCorpus):
        print('{} Was said before'.format(sA_Obj.inSent))
    else:
        print('New input: ', sA_Obj.inSent)

    # Get input sentence verbs
    ##sVerbs = getVerbs

    # If imperative, can Simp do what is asked?
    if sA_Obj.sType == 'imperative':
        canDo, cannotDo = canDoMatch(sA_Obj.getVerbs(), simpKB)
        
        print('Simp can: ', canDo)
        print('Simp cannot: ', cannotDo)
    else:
        print('Not imperative')

    # Can the subject do (canDo) what is said (subject canDo match verbs)?
    sVerbs = sA_Obj.getVerbs()
    print('sVerbs: ', sVerbs)

    sVerbsAndTags = sA_Obj.getVerbsAndTags()
    print('sVerbsAndTags: ', sVerbsAndTags)
  
    print(type(subjectsKB))
    for subj in subjectsKB:
        print(subj)
        subjCanDo = set(subj["canDo"].split(','))
        print(subjCanDo)
        intersect = subjCanDo.intersection(sVerbs)
        print(intersect)
        subjName = subj["_id"]
        print('{} can {}'.format(subjName, intersect))
        

  
        
    """
    if len(subjectCanDo) == 0:
        print('No subjectCanDo?!: ', subjectCanDo)
    else:
        if isinstance(sA_Obj.sVerb, tuple):
            print('tuple found')
            sVerbSet.add(sA_Obj.sVerb[0])
            print(sVerbSet)

            sVerbTag = getInflectionTag(sA_Obj.sVerb[1])
            inflections = getInflections(sA_Obj.sVerb[0], sVerbTag)
            print('inflections: ', inflections)

            sVerbSet = set(inflections[0])
            
            
        elif isinstance(sA_Obj.sVerb, list):
            print('list found')
            tmpLst = []
            for v in sA_Obj.sVerb:
                tmpLst.append(v[0])
            sVerbSet.add(tmpLst)
            print(sVerbSet)
        else:
            print('expecting tuple or list, but found: ', sA_Obj.sVerb)

        if len(sVerbSet) > 0:
            subjectCanDoSet = set(subjectCanDo)
            print('subjectCanDoSet: ', subjectCanDoSet)
            intersect = subjectCanDoSet.intersection(sVerbSet)
            if len(intersect) > 0:
                print('Yes, subject {} can {}'.format(sA_Obj.sSubj, intersect))
            else:
                print('No, subject {} cannot {}'.format(sA_Obj.sSubj, intersect))
        else:
            print('len(sVerbSet) == 0 ?', sVerbSet)
    """    
        

    print('------ end chkGrammar ------')
    return 'nope'


if __name__ == "__main__":

    print("simpGA.py: must call chkGrammar from other py file.")
        
