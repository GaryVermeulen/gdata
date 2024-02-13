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
def sentAnalysis3(taggedSentence):
   
    print('START: --- sentAnalysis3 ---')
    taggedInput = []
    error = []

    # Change input from dict to tuple
    for wt in taggedSentence:
        taggedInput.append((wt["word"], wt["tag"]))
        
    print('SA3: taggedInput: ')
    print(taggedInput)
    print('-----')
    
    tmpTypes = []
    tmpSubj = []
    tmpObject = []
    tmpIndirectObject = []
    # tmpInObj
    tmpVerbs = []
    tmpTag   = []
    processedSentence = []
    currentWordPosition = 0
    undetermined = True

    sent = Sentence(taggedInput, '', [], [], [])

    for inputWord in taggedInput:
        print('---')
        print(currentWordPosition)
        print(inputWord)
        word = inputWord[0] # was [0]
        tag  = inputWord[1]  # was [1]
        print('word: ', word)
        print('tag:  ', tag)
        print('processedSentence: ', processedSentence)
        
        if currentWordPosition == 0: # Not much we can with just one word
            if word in commandWords:
                sent.type = "imperative"
                
            if tag in nnx:
                sent.subject.append(inputWord)
                undetermined = False
            elif tag in prpx:
                if taggedInput[currentWordPosition + 1][1] in nnx: # My mom, My toys, ...
                    sent._PRPS = list(inputWord)
                    undetermined = False
                elif taggedInput[currentWordPosition + 1][1] in vbx: # I ran, She ran, ...
                    sent.subject.append(inputWord)
                    undetermined = False
                elif taggedInput[currentWordPosition + 1][1] == 'MD': # I could, ...
                    sent.subject.append(inputWord)
                    undetermined = False
                elif taggedInput[currentWordPosition + 1][1] == 'CC': # Me and my arrow...
                    sent.subject.append(inputWord)
                    undetermined = False
                else:    
                    print('simpSA3, prpx (currentWordPosition == 0), 2nd word else undefined: ', taggedInput[currentWordPosition + 1])
            elif tag in vbx:
                sent.verb.append(inputWord)
                undetermined = False
            elif tag in whx:
                sent._WHX = list(inputWord)
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
                    sent._MD = list(inputWord)
                    
            # Default sentence type...~?
            if len(sent.type) == 0:
                sent.type = "declarative"

            if undetermined:
                sent = setUndeterminedVar(sent, inputWord)

            print('End of 1st word:')
           
                
                    
        #elif currentWordPosition == 1:  # Secord word, but what if there are 100 words...~? :-(
                                        # Many say 14/15 to 20 should be max, but let's play...
        else:
            # Do we really need to check for every POS tag type?
            # For now we will...
            #
            """
            if tag == 'CC':
                if sent.isVar('_CC'):
                    sent._CC.append(inputWord)
                else:
                    sent._CC = list(inputWord)
            elif tag == 'CD':
                if sent.isVar('_CD'):
                    sent._CD.append(inputWord)
                else:
                    sent._CD = list(inputWord)
            elif tag == 'DT':
                if sent.isVar('_DT'):
                    sent._DT.append(inputWord)
                else:
                    sent._DT = list(inputWord)
            elif tag == 'EX':
                if sent.isVar('_EX'):
                    sent._EX.append(inputWord)
                else:
                    sent._EX = list(inputWord)
            elif tag == 'FW':
                if sent.isVar('_FW'):
                    sent._FW.append(inputWord)
                else:
                    sent._FW = list(inputWord)
            elif tag == 'IN':
                if sent.isVar('_IN'):
                    sent._IN.append(inputWord)
                else:
                    sent._IN = list(inputWord)
            elif tag == jj:
                if sent.isVar('_JJ'):
                    sent._JJ.append(inputWord)
                else:
                    sent._JJ = list(inputWord)
            elif tag == jjr:
                if sent.isVar('_JJR'):
                    sent._JJR.append(inputWord)
                else:
                    sent._JJR = list(inputWord)
            elif tag == jjs:
                if sent.isVar('_JJS'):
                    sent._JJS.append(inputWord)
                else:
                    sent._JJS = list(inputWord)
            elif tag == 'LS':
                if sent.isVar('_LS'):
                    sent._LS.append(inputWord)
                else:
                    sent._LS = list(inputWord)
            elif tag == 'MD':
                if sent.isVar('_MD'):
                    sent._MD.append(inputWord)
                else:
                    sent._MD = list(inputWord)
            elif tag in nnx:    # All nouns--trying to handle all nouns could be a mistake
            """
            if tag in nnx:
                print('nnx: ', inputWord)
                
                if len(sent.subject) == 0:
                    sent.subject.append(inputWord)
                else:
                    # Check for full name i.e. John Doe
                    if processedSentence[-1][1] == 'NNP':
                        # Where is it? Subject? object? or indirectObject?
                        if sent.subject[-1][1] == 'NNP':
                            sent.subject.append(inputWord)
                        elif sent.object[-1][1] == 'NNP':
                            sent.object.append(inputWord)
                        elif sent.isVar('_indirectObject'):
                            if sent._indirectObject[-1][1] == 'NNP':
                                sent._indirectObject.append(inputWord)
                        
                    # Is there a list? "Planes trains and boats are cool"
                    ### if the last word was a nnx or 'and' # so we need to know what has already been processed
                    if processedSentence[-1][0] == 'and':
                        subjectWords = getSubjectWords(sent)
                        if processedSentence[-2][0] in subjectWords: 
                            sent.subject.append(inputWord)
                    
                    if len(sent.object) == 0:
                        subjectWords = getSubjectWords(sent)
                
                        if word not in subjectWords:
                            sent.object.append(inputWord)
                    else:    
                        if sent.isVar('_indirectObject'):
                            sent._indirectObject.append(inputWord)
                        else:
                            sent._indirectObject = []
                            sent._indirectObject.append(inputWord)
                print('bottom of nnx:')
                sent.printAll()
            
            elif tag == 'PDT':
                if sent.isVar('_PDT'):
                    sent._PDT.append(inputWord)
                else:
                    sent._PDT = list(inputWord)
            elif tag == 'POS':
                if sent.isVar('_POS'):
                    sent._POS.append(inputWord)
                else:
                    sent._POS = list(inputWord)
            elif tag == 'PRP':
                print('PRP: ', inputWord)
                if sent.isVar('_PRP'):
                    sent._PRP.append(inputWord)
                else:
                    sent._PRP = []
                    sent._PRP.append(inputWord)
                print('End PRP: ', inputWord)
                    
            elif tag == 'PRP$':
                print('PRP$(S): ', inputWord)
                if sent.isVar('_PRPS'):
                    sent._PRPS.append(inputWord)
                else:
                    sent._PRPS = []
                    sent._PRPS.append(inputWord)
                print('End PRP$: ', inputWord)
                
            elif tag == 'RB':
                if sent.isVar('_RB'):
                    sent._RB.append(inputWord)
                else:
                    sent._RB = list(inputWord)
            elif tag == 'RBR':
                if sent.isVar('_RBR'):
                    sent._RBR.append(inputWord)
                else:
                    sent._RBR = list(inputWord)
            elif tag == 'RBS':
                if sent.isVar('_RBS'):
                    sent._RBS.append(inputWord)
                else:
                    sent._RBS = list(inputWord)
            elif tag == 'RP':
                if sent.isVar('_RP'):
                    sent._RP.append(inputWord)
                else:
                    sent._RP = list(inputWord)
            elif tag == 'SYM':
                if sent.isVar('_SYM'):
                    sent._SYM.append(inputWord)
                else:
                    sent._SYM = list(inputWord)
            elif tag == 'TO':
                if sent.isVar('_TO'):
                    sent._TO.append(inputWord)
                else:
                    sent._TO = list(inputWord)
            elif tag == 'UH':
                if sent.isVar('_UH'):
                    sent._UH.append(inputWord)
                else:
                    sent._UH = list(inputWord)
            
            elif tag in vbx:
                sent.verb.append(inputWord)
            """
            elif tag == 'WDT':
                if sent.isVar('_WDT'):
                    sent._WDT.append(inputWord)
                else:
                    sent._WDT = list(inputWord)
            elif tag == 'WP':
                if sent.isVar('_WP'):
                    sent._WP.append(inputWord)
                else:
                    sent._WP = list(inputWord)
            elif tag == 'WPS':
                if sent.isVar('_WPS'):
                    sent._WPS.append(inputWord)
                else:
                    sent._WPS = list(inputWord)
            elif tag == 'WRB':
                if sent.isVar('_WRB'):
                    sent._WRB.append(inputWord)
                else:
                    sent._WRB = list(inputWord)
            
            else:
                print('sentAnalysis2 else -- something wrong or tag not defined?')
                print('current word position: {}, current word: {}, current tag: {}'.format(currentWordPosition, word, tag))
                error.append('sentAnalysis else -- something wrong or tag not defined?')
                error.append('word position: ')
                error.append(currentWordPosition)
                error.append('inputWord: ')
                error.append(inputWord)
            """
        print('bottom of the big if:')
        sent.printAll()
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
# Old input:
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
#    tagged_uI = [('a', 'DT'), ('family', 'NN'), ('is', 'VBZ'), ('a', 'DT'), ('group', 'NN'), ('of', 'IN'), ('persons', 'NNS'), ('of', 'IN'), ('a', 'DT'), ('common', 'JJ'), ('ancestry', 'NN'), ('clan', 'NN')]

    # New input:
    tagged_uI = [{'word': 'My', 'tag': 'PRP$'}, {'word': 'name', 'tag': 'NN'}, {'word': 'is', 'tag': 'VBZ'}, {'word': 'Allie', 'tag': 'NNP'}, {'word': 'Kay', 'tag': 'NNP'}, {'word': 'and', 'tag': 'CC'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'would', 'tag': 'MD'}, {'word': 'like', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'tell', 'tag': 'VB'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'about', 'tag': 'IN'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'first', 'tag': 'JJ'}, {'word': 'pet', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'However', 'tag': 'RB'}, {'word': ',', 'tag': ','}, {'word': 'before', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'can', 'tag': 'MD'}, {'word': ',', 'tag': ','}, {'word': 'you', 'tag': 'PRP'}, {'word': 'have', 'tag': 'VBP'}, {'word': 'to', 'tag': 'TO'}, {'word': 'understand', 'tag': 'VB'}, {'word': 'that', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'a', 'tag': 'DT'}, {'word': 'little', 'tag': 'RB'}, {'word': 'older', 'tag': 'JJR'}, {'word': 'than', 'tag': 'IN'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'are', 'tag': 'VBP'}, {'word': 'and', 'tag': 'CC'}, {'word': 'have', 'tag': 'VB'}, {'word': 'a', 'tag': 'DT'}, {'word': 'family', 'tag': 'NN'}, {'word': 'of', 'tag': 'IN'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'own', 'tag': 'JJ'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'Oh', 'tag': 'UH'}, {'word': '!', 'tag': '.'}]
    #tagged_uI = [{'word': 'Do', 'tag': 'VB'}, {'word': 'not', 'tag': 'RB'}, {'word': 'worry', 'tag': 'VB'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'not', 'tag': 'RB'}, {'word': 'going', 'tag': 'VBG'}, {'word': 'to', 'tag': 'TO'}, {'word': 'talk', 'tag': 'VB'}, {'word': 'to', 'tag': 'IN'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'like', 'tag': 'IN'}, {'word': 'a', 'tag': 'DT'}, {'word': 'big', 'tag': 'JJ'}, {'word': 'person', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'going', 'tag': 'VBG'}, {'word': 'to', 'tag': 'TO'}, {'word': 'let', 'tag': 'VB'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'imagination', 'tag': 'NN'}, {'word': 'take', 'tag': 'VB'}, {'word': 'me', 'tag': 'PRP'}, {'word': 'back', 'tag': 'RB'}, {'word': 'in', 'tag': 'IN'}, {'word': 'time', 'tag': 'NN'}, {'word': 'to', 'tag': 'IN'}, {'word': 'when', 'tag': 'WRB'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'was', 'tag': 'VBD'}, {'word': '7', 'tag': 'CD'}, {'word': 'years', 'tag': 'NNS'}, {'word': 'old', 'tag': 'JJ'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'The', 'tag': 'DT'}, {'word': 'best', 'tag': 'JJS'}, {'word': 'part', 'tag': 'NN'}, {'word': 'is', 'tag': 'VBZ'}, {'word': 'that', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'do', 'tag': 'VBP'}, {'word': 'not', 'tag': 'RB'}, {'word': 'have', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'try', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'remember', 'tag': 'VB'}, {'word': 'everything', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    

    newSA_Obj, error2 = sentAnalysis3(tagged_uI)

    print('---')

    if len(error2) > 0:
        for e in error2:
            print(e)

    newSA_Obj.printAll()
 
 
    print('\nEND: --- simpSA2 main ---')    
