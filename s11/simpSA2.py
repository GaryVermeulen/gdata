#
# simpSA2.py
#
#   Sentence analysis--attempt to determine SVO
#   The orginal simpSA is a nightmare, so trying
#   something different...
#


from commonConfig import *


def setUndeterminedVar(sent, inputWord):

    word   = inputWord[0]
    tag    = inputWord[1]
    tmpTag = []

    if tag == 'CC':
        if sent.isVar('_CC'):
            tmpTag.append(sent._CC)
            tmpTag.append(inputWord)
            sent._CC = tmpTag
        else:
            sent._CC = inputWord
    elif tag == 'CD':
        if sent.isVar('_CD'):
            tmpTag.append(sent._CD)
            tmpTag.append(inputWord)
            sent._CD = tmpTag
        else:
            sent._CD = inputWord
    elif tag == 'DT':
        if sent.isVar('_DT'):
            tmpTag.append(sent._DT)
            tmpTag.append(inputWord)
            sent._DT = tmpTag
        else:
            sent._DT = inputWord
    elif tag == 'EX':
        if sent.isVar('_EX'):
            tmpTag.append(sent._EX)
            tmpTag.append(inputWord)
            sent._EX = tmpTag
        else:
            sent._EX = inputWord
    elif tag == 'FW':
        if sent.isVar('_FW'):
            tmpTag.append(sent._FW)
            tmpTag.append(inputWord)
            sent._FW = tmpTag
        else:
            sent._FW = inputWord
    elif tag == 'IN':
        if sent.isVar('_IN'):
            tmpTag.append(sent._IN)
            tmpTag.append(inputWord)
            sent._IN = tmpTag
        else:
            sent._IN = inputWord
    elif tag == jj:
        if sent.isVar('_JJ'):
            tmpTag.append(sent._JJ)
            tmpTag.append(inputWord)
            sent._JJ = tmpTag
        else:
            sent._JJ = inputWord
    elif tag == jjr:
        if sent.isVar('_JJR'):
            tmpTag.append(sent._JJR)
            tmpTag.append(inputWord)
            sent._JJR = tmpTag
        else:
            sent._JJR = inputWord
    elif tag == jjs:
        if sent.isVar('_JJS'):
            tmpTag.append(sent._JJS)
            tmpTag.append(inputWord)
            sent._JJS = tmpTag
        else:
            sent._JJS = inputWord
    elif tag == 'LS':
        if sent.isVar('_LS'):
            tmpTag.append(sent._LS)
            tmpTag.append(inputWord)
            sent._LS = tmpTag
        else:
            sent._LS = inputWord
    elif tag == 'MD':
        if sent.isVar('_MD'):
            tmpTag.append(sent._MD)
            tmpTag.append(inputWord)
            sent._MD = tmpTag
        else:
            sent._MD = inputWord
    elif tag == nn:
        if sent.isVar('_NN'):
            tmpTag.append(sent._NN)
            tmpTag.append(inputWord)
            sent._NN = tmpTag
        else:
            sent._NN = inputWord
    elif tag == nnp:
        if sent.isVar('_NNP'):
            tmpTag.append(sent._NNP)
            tmpTag.append(inputWord)
            sent._NNP = tmpTag
        else:
            sent._NNP = inputWord
    elif tag == nns:
        if sent.isVar('_NNS'):
            tmpTag.append(sent._NNS)
            tmpTag.append(inputWord)
            sent._NNS = tmpTag
        else:
            sent._NNS = inputWord
    elif tag == nnps:
        if sent.isVar('_NNPS'):
            tmpTag.append(sent._NNPS)
            tmpTag.append(inputWord)
            sent._NNPS = tmpTag
        else:
            sent._NNPS = inputWord
    elif tag == 'PDT':
        if sent.isVar('_PDT'):
            tmpTag.append(sent._PDT)
            tmpTag.append(inputWord)
            sent._PDT = tmpTag
        else:
            sent._PDT = inputWord
    elif tag == 'POS':
        if sent.isVar('_POS'):
            tmpTag.append(sent._POS)
            tmpTag.append(inputWord)
            sent._POS = tmpTag
        else:
            sent._POS = inputWord
    elif tag == prp:
        if sent.isVar('_PRP'):
            tmpTag.append(sent._PRP)
            tmpTag.append(inputWord)
            sent._PRP = tmpTag
        else:
            sent._PRP = inputWord
    elif tag == prps:
        if sent.isVar('_PRPS'):
            tmpTag.append(sent._PRPS)
            tmpTag.append(inputWord)
            sent._PRPS = tmpTag
        else:
            sent._PRPS = inputWord
    elif tag == 'RB':
        if sent.isVar('_RB'):
            tmpTag.append(sent._RB)
            tmpTag.append(inputWord)
            sent._RB = tmpTag
        else:
            sent._RB = inputWord
    elif tag == 'RBR':
        if sent.isVar('_RBR'):
            tmpTag.append(sent._RBR)
            tmpTag.append(inputWord)
            sent._RBR = tmpTag
        else:
            sent._RBR = inputWord
    elif tag == 'RBS':
        if sent.isVar('_RBS'):
            tmpTag.append(sent._RBS)
            tmpTag.append(inputWord)
            sent._RBS = tmpTag
        else:
            sent._RBS = inputWord
    elif tag == 'RP':
        if sent.isVar('_RP'):
            tmpTag.append(sent._RP)
            tmpTag.append(inputWord)
            sent._RP = tmpTag
        else:
            sent._RP = inputWord
    elif tag == 'SYM':
        if sent.isVar('_SYM'):
            tmpTag.append(sent._SYM)
            tmpTag.append(inputWord)
            sent._SYM = tmpTag
        else:
            sent._SYM = inputWord
    elif tag == 'TO':
        if sent.isVar('_TO'):
            tmpTag.append(sent._TO)
            tmpTag.append(inputWord)
            sent._TO = tmpTag
        else:
            sent._TO = inputWord
    elif tag == 'UH':
        if sent.isVar('_UH'):
            tmpTag.append(sent._UH)
            tmpTag.append(inputWord)
            sent._UH = tmpTag
        else:
            sent._UH = inputWord
    elif tag == vb:
        if sent.isVar('_VB'):
            tmpTag.append(sent._VB)
            tmpTag.append(inputWord)
            sent._VB = tmpTag
        else:
            sent._VB = inputWord
    elif tag == vbd:
        if sent.isVar('_VBD'):
            tmpTag.append(sent._VBD)
            tmpTag.append(inputWord)
            sent._VBD = tmpTag
        else:
            sent._VBD = inputWord
    elif tag == vbg:
        if sent.isVar('_VBG'):
            tmpTag.append(sent._VBG)
            tmpTag.append(inputWord)
            sent._VBG = tmpTag
        else:
            sent._VBG = inputWord
    elif tag == vbn:
        if sent.isVar('_VBN'):
            tmpTag.append(sent._VBN)
            tmpTag.append(inputWord)
            sent._VBN = tmpTag
        else:
            sent._VBN = inputWord
    elif tag == vbp:
        if sent.isVar('_VBP'):
            tmpTag.append(sent._VBP)
            tmpTag.append(inputWord)
            sent._VBP = tmpTag
        else:
            sent._VBP = inputWord
    elif tag == vbz:
        if sent.isVar('_VBZ'):
            tmpTag.append(sent._VBZ)
            tmpTag.append(inputWord)
            sent._VBZ = tmpTag
        else:
            sent._VBZ = inputWord
    elif tag == 'WDT':
        if sent.isVar('_WDT'):
            tmpTag.append(sent._WDT)
            tmpTag.append(inputWord)
            sent._WDT = tmpTag
        else:
            sent._WDT = inputWord
    elif tag == 'WP':
        if sent.isVar('_WP'):
            tmpTag.append(sent._WP)
            tmpTag.append(inputWord)
            sent._WP = tmpTag
        else:
            sent._WP = inputWord
    elif tag == 'WPS':
        if sent.isVar('_WPS'):
            tmpTag.append(sent._WPS)
            tmpTag.append(inputWord)
            sent._WPS = tmpTag
        else:
            sent._WPS = inputWord
    elif tag == 'WRB':
        if sent.isVar('_WRB'):
            tmpTag.append(sent._WRB)
            tmpTag.append(inputWord)
            sent._WRB = tmpTag
        else:
            sent._WRB = inputWord
    else:
        if sent.isVar('_UNK'):
            tmpTag.append(sent._UNK)
            tmpTag.append(inputWord)
            sent._UNK = tmpTag
        else:
            sent._UNK = inputWord

    return sent


def getSubjectWords(sent):
    # Just return a list of just the subject(s) words (no tags)
    subWords = []
    subs = sent.subject
    
    if isinstance(subs, tuple):
        subWords.append(subs[0])
    elif isinstance(subs, list):
        for s in subs:
            subWords.append(s[0])

    return subWords
    



# Attempt to analyze the input sentence
####################################################
def sentAnalysis2(taggedInput):
   
    print('START: --- sentAnalysis2 ---')
    error = []
    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''

    tmpTypes = []
    tmpSubj = []
    tmpIndirectObject = []
    tmpVerbs = []
    tmpTag   = []

    processedSentence = []

    currentWordPosition = 0

    undetermined = True

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj)

    print(taggedInput)
    for inputWord in taggedInput:
        print(currentWordPosition)
        print(inputWord)
        word = inputWord[0]
        tag  = inputWord[1]
        print('word: ', word)
        print('tag:  ', tag)
        print('processedSentence: ', processedSentence)
        
        
        if currentWordPosition == 0: # Not much we can with just one word
            if word in commandWords:
                sent.type = "imperative"
                
            if tag in nnx:
                sent.subject = inputWord
                undetermined = False
            elif tag in prpx:
                sent.subject = inputWord
                undetermined = False
            elif tag in vbx:
                sent.verb = inputWord
                undetermined = False
            elif tag in whx:
                sent._WHX = inputWord
                if len(sent.type) == 0:
                    sent.type = "interrogative"
                else:   
                    sent.type = sent.type + ', interrogative' # An imperative interrogation?
                
            # "can" is not a whx, so a funky exception?
            if word in ['Can', 'can']:
                if len(sent.type) == 0:
                    sent.type = "interrogative"
                else:
                    sent.type = sent.type + ', interrogative' # An imperative interrogation?
                    
                if tag == 'MD': # Do we really need to check for MD or can we assume MD...~?
                    sent._MD = inputWord
                    
            # Default sentence type...~?
            if len(sent.type) == 0:
                sent.type = "declarative"

            if undetermined:
                sent = setUndeterminedVar(sent, inputWord)
                
                    
        #elif currentWordPosition == 1:  # Secord word, but what if there are 100 words...~? :-(
                                        # Many say 14/15 to 20 should be max, but let's play...
        else:
            # Do we really need to check for every POS tag type?
            # For now we will...
            #
            if tag == 'CC':
                if sent.isVar('_CC'):
                    tmpTag.append(sent._CC)
                    tmpTag.append(inputWord)
                    sent._CC = tmpTag
                else:
                    sent._CC = inputWord
            elif tag == 'CD':
                if sent.isVar('_CD'):
                    tmpTag.append(sent._CD)
                    tmpTag.append(inputWord)
                    sent._CD = tmpTag
                else:
                    sent._CD = inputWord
            elif tag == 'DT':
                if sent.isVar('_DT'):
                    tmpTag.append(sent._DT)
                    tmpTag.append(inputWord)
                    sent._DT = tmpTag
                else:
                    sent._DT = inputWord
            elif tag == 'EX':
                if sent.isVar('_EX'):
                    tmpTag.append(sent._EX)
                    tmpTag.append(inputWord)
                    sent._EX = tmpTag
                else:
                    sent._EX = inputWord
            elif tag == 'FW':
                if sent.isVar('_FW'):
                    tmpTag.append(sent._FW)
                    tmpTag.append(inputWord)
                    sent._FW = tmpTag
                else:
                    sent._FW = inputWord
            elif tag == 'IN':
                if sent.isVar('_IN'):
                    tmpTag.append(sent._IN)
                    tmpTag.append(inputWord)
                    sent._IN = tmpTag
                else:
                    sent._IN = inputWord
            elif tag == jj:
                if sent.isVar('_JJ'):
                    tmpTag.append(sent._JJ)
                    tmpTag.append(inputWord)
                    sent._JJ = tmpTag
                else:
                    sent._JJ = inputWord
            elif tag == jjr:
                if sent.isVar('_JJR'):
                    tmpTag.append(sent._JJR)
                    tmpTag.append(inputWord)
                    sent._JJR = tmpTag
                else:
                    sent._JJR = inputWord
            elif tag == jjs:
                if sent.isVar('_JJS'):
                    tmpTag.append(sent._JJS)
                    tmpTag.append(inputWord)
                    sent._JJS = tmpTag
                else:
                    sent._JJS = inputWord
            elif tag == 'LS':
                if sent.isVar('_LS'):
                    tmpTag.append(sent._LS)
                    tmpTag.append(inputWord)
                    sent._LS = tmpTag
                else:
                    sent._LS = inputWord
            elif tag == 'MD':
                if sent.isVar('_MD'):
                    tmpTag.append(sent._MD)
                    tmpTag.append(inputWord)
                    sent._MD = tmpTag
                else:
                    sent._MD = inputWord
            elif tag in nnx:    # All nouns
                if len(sent.subject) == 0:
                    sent.subject = inputWord
                else:
                    # Is there a list? "Planes trains and boats are cool"
                    ### if the last word was a nnx or 'and' # so we need to know what has already been processed
                    if processedSentence[-1][0] == 'and':
                        subjectWords = getSubjectWords(sent)
                        if processedSentence[-2][0] in subjectWords: 
                            tmpSubj.append(sent.subject)
                            sent.subject = tmpSubj
                            sent.subject.append(inputWord)
                    
                    if len(sent.object) == 0:
                        subjectWords = getSubjectWords(sent)
                        if word not in subjectWords:
                            sent.object = inputWord
                    else:
                        if sent.isVar('_indirectObject'):
                            tmpIndirectObject.append(sent._indirectObject)
                            sent._indirectObject = tmpIndirectObject
                            sent._indirectObject.append(inputWord)
                        else:
                            sent._indirectObject = inputWord
            elif tag == 'PDT':
                if sent.isVar('_PDT'):
                    tmpTag.append(sent._PDT)
                    tmpTag.append(inputWord)
                    sent._PDT = tmpTag
                else:
                    sent._PDT = inputWord
            elif tag == 'POS':
                if sent.isVar('_POS'):
                    tmpTag.append(sent._POS)
                    tmpTag.append(inputWord)
                    sent._POS = tmpTag
                else:
                    sent._POS = inputWord
            elif tag in prpx:
                if len(sent.subject) == 0:
                    sent.subject = inputWord
                else:
                    if len(sent.object) == 0:
                        sent.object = inputWord
                    else:
                        if sent.isVar('_indirectObject'):
                            tmpIndirectObject.append(sent._indirectObject)
                            sent._indirectObject = tmpInObj
                            sent._indirectObject.append(inputWord)
                        else:
                            sent._indirectObject = inputWord
            elif tag == 'RB':
                if sent.isVar('_RB'):
                    tmpTag.append(sent._RB)
                    tmpTag.append(inputWord)
                    sent._RB = tmpTag
                else:
                    sent._RB = inputWord
            elif tag == 'RBR':
                if sent.isVar('_RBR'):
                    tmpTag.append(sent._RBR)
                    tmpTag.append(inputWord)
                    sent._RBR = tmpTag
                else:
                    sent._RBR = inputWord
            elif tag == 'RBS':
                if sent.isVar('_RBS'):
                    tmpTag.append(sent._RBS)
                    tmpTag.append(inputWord)
                    sent._RBS = tmpTag
                else:
                    sent._RBS = inputWord
            elif tag == 'RP':
                if sent.isVar('_RP'):
                    tmpTag.append(sent._RP)
                    tmpTag.append(inputWord)
                    sent._RP = tmpTag
                else:
                    sent._RP = inputWord
            elif tag == 'SYM':
                if sent.isVar('_SYM'):
                    tmpTag.append(sent._SYM)
                    tmpTag.append(inputWord)
                    sent._SYM = tmpTag
                else:
                    sent._SYM = inputWord
            elif tag == 'TO':
                if sent.isVar('_TO'):
                    tmpTag.append(sent._TO)
                    tmpTag.append(inputWord)
                    sent._TO = tmpTag
                else:
                    sent._TO = inputWord
            elif tag == 'UH':
                if sent.isVar('_UH'):
                    tmpTag.append(sent._UH)
                    tmpTag.append(inputWord)
                    sent._UH = tmpTag
                else:
                    sent._UH = inputWord
            elif tag in vbx:
                if len(sent.verb) == 0:
                    sent.verb = inputWord
                else:
                    if isinstance(sent.verb, tuple):
                        tmpVerbs.append(sent.verb)
                    elif isinstance(sent.verb, list):
                        for v in sent.verb:
                            tmpVerbs.append(v)

                    tmpVerbs.append(inputWord)
                    sent.verb = tmpVerbs
            elif tag == 'WDT':
                if sent.isVar('_WDT'):
                    tmpTag.append(sent._WDT)
                    tmpTag.append(inputWord)
                    sent._WDT = tmpTag
                else:
                    sent._WDT = inputWord
            elif tag == 'WP':
                if sent.isVar('_WP'):
                    tmpTag.append(sent._WP)
                    tmpTag.append(inputWord)
                    sent._WP = tmpTag
                else:
                    sent._WP = inputWord
            elif tag == 'WPS':
                if sent.isVar('_WPS'):
                    tmpTag.append(sent._WPS)
                    tmpTag.append(inputWord)
                    sent._WPS = tmpTag
                else:
                    sent._WPS = inputWord
            elif tag == 'WRB':
                if sent.isVar('_WRB'):
                    tmpTag.append(sent._WRB)
                    tmpTag.append(inputWord)
                    sent._WRB = tmpTag
                else:
                    sent._WRB = inputWord
            else:
                print('sentAnalysis2 else -- something wrong or tag not defined?')
                print('current word position: {}, current word: {}, current tag: {}'.format(currentWordPosition, word, tag))
                error.append('sentAnalysis else -- something wrong or tag not defined?')
                error.append('word position: ')
                error.append(currentWordPosition)
                error.append('inputWord: ')
                error.append(inputWord)
        
        currentWordPosition += 1
        # Reset/clear tmp var's
        tmpTypes = []
        tmpSubj = []
        tmpIndirectObject = []
        tmpVerbs = []
        tmpTag   = []

        processedSentence.append(inputWord) # Tracking what we have processed for back-tracking/checking
    
    print('END: --- sentAnalysis2 ---')
    return sent, error



if __name__ == "__main__":

    print('START: --- simpSA2 main ---')

#    tagged_uI = [('see', 'VBP'), ('Hammy', 'NNP')]

#    tagged_uI = [('i', 'PRP'), ('am', 'VBP')]

#    tagged_uI = [('can', 'MD'), ('you', 'PRP'), ('eat', 'VB'), ('a', 'DT'), ('bus', 'NN')]


#    tagged_uI = [('see', 'VBP'), ('Hammy', 'NNP'), ('run', 'VB')]
#    tagged_uI = [('see', 'VBP'), ('Hammy', 'NNP'), ('run', 'VB'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN')]
#    tagged_uI = [('Bob', 'NNP'), ('was', 'VBD'), ('happy', 'JJ')]
#    tagged_uI = [('Bob', 'NNP'), ('saw', 'VBD'), ('Pookie', 'NNP')]
#    tagged_uI = [('Bob', 'NNP'), ('walked', 'VBD'), ('Pookie', 'NNP'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN')]
#    tagged_uI = [('Bob', 'NNP'), ('walked', 'VBD'), ('Pookie', 'NNP'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('with', 'IN'), ('Hammy', 'NNP')]
#    tagged_uI = [('Bob', 'NNP'), ('and', 'CC'), ('Mary', 'NNP'), ('walked', 'VBD'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('with', 'IN'), ('Pookie', 'NNP')]


#    tagged_uI = [('Bob', 'NNP'), ('is', 'VBZ'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('with', 'IN'), ('Pookie', 'NNP'), ('and', 'CC'), ('Hammy', 'NNP')]

#    tagged_uI = [('two', 'CD'), ('persons', 'NNS'), ('per', 'IN'), ('campus', 'NN'), ('were', 'VBD'), ('given', 'VBN'), ('workshop', 'NN'), ('training', 'NN')]

#    tagged_uI = [('what', 'WDT'), ('book', 'NN'), ('are', 'VBP'), ('you', 'PRP'), ('reading', 'VBG')]
#    tagged_uI = [('where', 'WRB'), ('have', 'VBP'), ('you', 'PRP'), ('been', 'VBN')]
#    tagged_uI = [('who', 'WP'), ('can', 'MD'), ('help', 'VB'), ('me', 'PRP')]

#!!    tagged_uI = [('Where', 'WRB'), ('do', 'VBP'), ('we', 'PRP'), ('go', 'VB'), ('from', 'IN'), ('here', 'RB')] # Watch for tagging errors
#should be:
#    tagged_uI = [('Where', 'WRB'), ('do', 'VBP'), ('we', 'PRP'), ('go', 'VB'), ('from', 'IN'), ('here', 'NN')]

#    tagged_uI = [('they', 'PRP'), ('went', 'VBD'), ('to', 'IN'), ('the', 'DT'), ('park', 'NN')]

#    tagged_uI = [('stop', 'VB'), ('what', 'WP'), ('you', 'PRP'), ('are', 'VBP'), ('doing', 'VBG')]

#    tagged_uI = [('here', 'RB'), ('we', 'PRP'), ('go', 'VBP'), ('again', 'RB')]

#    tagged_uI = [('a', 'DT'), ('family', 'NN'), ('is', 'VBZ'), ('a', 'DT'), ('group', 'NN'), ('of', 'IN'), ('persons', 'NNS')]

    tagged_uI = [('a', 'DT'), ('family', 'NN'), ('is', 'VBZ'), ('a', 'DT'), ('group', 'NN'), ('of', 'IN'), ('persons', 'NNS'), ('of', 'IN'), ('a', 'DT'), ('common', 'JJ'), ('ancestry', 'NN'), ('clan', 'NN')]
    

    newSA_Obj, error2 = sentAnalysis2(tagged_uI)

    print('---')

    if len(error2) > 0:
        for e in error2:
            print(e)

    newSA_Obj.printAll()
 
 
    print('\nEND: --- simpSA2 main ---')    
