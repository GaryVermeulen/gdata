#
# simpSA.py
#
#   Sentence analysis--attempt to determine SVO
#   This version takes a tagged input sentence instead of
#   a CFG tree
#


from commonConfig import Sentence, validClassVars, commandWords


def processCC(wordPosition, sent):

    tmpCC = []

    if wordPosition == 1:
        sent.type = 'declarative?'
        sent._CC = sent.inputSent[0]
    else:
        if sent.isVar('_CC'):
            tmpCC.append(sent._CC)
            tmpCC.append(sent.inputSent[wordPosition - 1])
            sent._CC = tmpCC
        else:
            sent._CC = sent.inputSent[wordPosition - 1]

    return sent


def processCD(wordPosition, sent):

    tmpCD = []
    
    if sent.isVar('_CD'):
        tmpDT.append(sent._CD)
        tmpDT.append(sent.inputSent[wordPosition - 1])
        sent._CD = tmpCD
    else:
        sent._CD = sent.inputSent[wordPosition - 1]

    return sent


def processDT(wordPosition, sent):

    tmpDT = []

    if wordPosition == 1:
        sent.type = 'declarative'
        sent._DT = sent.inputSent[0]
    else:
        if sent.isVar('_DT'):
            tmpDT.append(sent._DT)
            tmpDT.append(sent.inputSent[wordPosition - 1])
            sent._DT = tmpDT
        else:
            sent._DT = sent.inputSent[wordPosition - 1]

    return sent


def processEX(wordPosition, sent):

    tmpEX = []
    
    if sent.isVar('_EX'):
        tmpEX.append(sent._EX)
        tmpEX.append(sent.inputSent[wordPosition - 1])
        sent._EX = tmpEX
    else:
        sent._EX = sent.inputSent[wordPosition - 1]

    return sent


def processFW(wordPosition, sent):

    tmpFW = []
    
    if sent.isVar('_FW'):
        tmpFW.append(sent._FW)
        tmpFW.append(sent.inputSent[wordPosition - 1])
        sent._FW = tmpFW
    else:
        sent._FW = sent.inputSent[wordPosition - 1]

    return sent


def processIN(wordPosition, sent):

    tmpIN = []

    if wordPosition == 1:
        sent.type = 'declarative'
        sent._IN = sent.inputSent[0]
    else:
        if sent.isVar('_IN'):
            tmpIN.append(sent._IN)
            tmpIN.append(sent.inputSent[wordPosition - 1])
            sent._IN = tmpIN
        else:
            sent._IN = sent.inputSent[wordPosition - 1]

    return sent


def processJJ(wordPosition, sent):

    tmpJJ = []

    if wordPosition == 1:
        sent.type = 'declarative'
        sent._JJ = sent.inputSent[0]
    else:
        if sent.isVar('_JJ'):
            tmpJJ.append(sent._JJ)
            tmpJJ.append(sent.inputSent[wordPosition - 1])
            sent._JJ = tmpJJ
        else:
            sent._JJ = sent.inputSent[wordPosition - 1]

    return sent


def processJJR(wordPosition, sent):

    tmpJJR = []

    if sent.isVar('_JJR'):
        tmpJJR.append(sent._JJR)
        tmpJJR.append(sent.inputSent[wordPosition - 1])
        sent._JJR = tmpJJR
    else:
        sent._JJR = sent.inputSent[wordPosition - 1]

    return sent


def processJJS(wordPosition, sent):

    tmpJJS = []
    
    if sent.isVar('_JJS'):
        tmpJJS.append(sent._JJS)
        tmpJJS.append(sent.inputSent[wordPosition - 1])
        sent._JJS = tmpJJS
    else:
        sent._JJS = sent.inputSent[wordPosition - 1]

    return sent


def processLS(wordPosition, sent):

    tmpLS = []
    
    if sent.isVar('_LS'):
        tmpLS.append(sent._LS)
        tmpLS.append(sent.inputSent[wordPosition - 1])
        sent._LS = tmpLS
    else:
        sent._LS = sent.inputSent[wordPosition - 1]

    return sent


def processMD(wordPosition, sent):

    # Except for the 1st word of a sentence I don't think a MD should ever be capitalized...~?

    tmpMD = []
    taggedMD = sent.inputSent[wordPosition - 1]
    word = taggedMD[0].lower()
    tag = taggedMD[1]

    if wordPosition == 1:
        if sent.inputSent[0][0] == 'can':
            sent.type = 'interrogative'
        else:
            sent.type = 'declarative'
        taggedMD = (word, tag)
        sent._MD = taggedMD
    else:
        if sent.isVar('_MD'):
            tmpMD.append(sent._MD)
            tmpMD.append(taggedMD)
            sent._MD = tmpMD
        else:
            sent._MD = taggedMD

    return sent


def processNN(wordPosition, sent):

    tmpInObj = []
    tmpObj = []
    tmpSubj = []

    if wordPosition == 1:
        sent.type = 'declarative'

        if sent.subject == '':
            sent.subject = sent.inputSent[0]
    else:
        if sent.type == '':
            sent.type = 'declarative'

        if len(sent.verb) > 0:
            if len(sent.subject) == 0:
                sent.subject = sent.inputSent[wordPosition - 1]
            else:
                if len(sent.object) == 0:
                    sent.object = sent.inputSent[wordPosition - 1]
                else:
                    print("ELSE:")
                    if sent.isVar('_indirectObject'):
                        tmpInObj.append(sent._indirectObject)
                        sent._indirectObject = tmpInObj
                        sent._indirectObject.append(sent.inputSent[wordPosition - 1])
                    else:
                        print("ADDING 1st indirectObject!?!")
                        sent._indirectObject = sent.inputSent[wordPosition - 1]
        else:
            if sent.isVar('_DT'):
                if len(sent.subject) == 0:
                    sent.subject = sent.inputSent[wordPosition - 1]
                else:
                    if sent.isVar('_CC') and wordPosition == 4:
                        tmpSubj.append(sent.subject)
                        sent.subject = tmpSubj
                        sent.subject.append(sent.inputSent[wordPosition - 1])
                    else:
                        if len(sent.object) == 0:
                            sent.object = sent.inputSent[wordPosition - 1]
                        else:
                            tmpObj.append(sent.object)
                            sent.object = tmpObj
                            sent.object.append(sent.inputSent[wordPosition - 1])
            else: # Attempt to catch "Hello Simp"
                if len(sent.subject) == 0:
                    sent.subject = sent.inputSent[wordPosition - 1]

                
            # ? Not sure wjhat I was trying to catch...~?
            #if sent.inSent[wordPosition - 2][1] == 'DT':
            #    if sent.sSubj != '':
            #        if sent.sObj == '':
            #            sent.sObj = sent.inSent[wordPosition - 1]
            #        else:
            #            tmpObj.append(sent.sObj)
            #            sent.sObj = tmpInObj
            #            sent.sObj.append(sent.inSent[wordPosition - 1])
            
    return sent


def processNNS(wordPosition, sent):

    tmpNNS = []
    tmpInObj = []

    if len(sent.subject) == 0:
        sent.subject = sent.inputSent[wordPosition - 1]
        if sent.isVar('_NNS'):
            tmpNNS.append(sent._NNS)
            tmpNNS.append(sent.inputSent[wordPosition - 1])
            sent._NNS = tmpNNS
        else:
            sent._NNS = sent.inputSent[wordPosition - 1]

    elif len(sent.object == 0):
        sent.object = sent.inputSent[wordPosition - 1]
        if sent.isVar('_NNS'):
            tmpNNS.append(sent._NNS)
            tmpNNS.append(sent.inputSent[wordPosition - 1])
            sent._NNS = tmpNNS
        else:
            sent._NNS = sent.inputSent[wordPosition - 1]
    else:
        
        if sent.isVar('_indirectObject'):
            if sent.isVar('_NNS'):
                tmpNNS.append(sent._NNS)
                tmpNNS.append(sent.inputSent[wordPosition - 1])
                sent._NNS = tmpNNS
            else:
                sent._NNS = sent.inputSent[wordPosition - 1]    
            tmpInObj.append(sent._indirectObject)
            sent._indirectObject = tmpInObj
            sent._indirectObject.append(sent.inputSent[wordPosition - 1])
        else:
            if sent.isVar('_NNS'):
                tmpNNS.append(sent._NNS)
                tmpNNS.append(sent.inputSent[wordPosition - 1])
                sent._NNS = tmpNNS
            else:
                sent._NNS = sent.inputSent[wordPosition - 1]
            print("ADDING 1st _NNS indirectObject!?!")
            sent._indirectObject = sent.inputSent[wordPosition - 1]

    return sent

        
def processNNP(wordPosition, sent):

    tmpInObj = []
    tmpSubj = []

    print('Start NNP')

    if wordPosition == 1:
        sent.type = 'declarative'

        if sent.subject == '':
            sent.subject =  sent.inputSent[0]
    else:
        if len(sent.type) == 0:
            sent.type = 'declarative'

        if len(sent.verb) > 0:
            if len(sent.subject) == 0:
                sent.subject = sent.inputSent[wordPosition - 1]
            else:
                if sent.isVar('_CC'):
                    tmpSubj.append(sent.subject)
                    sent.subject = tmpSubj
                    sent.subject.append(sent.inputSent[wordPosition - 1])
                else:
                    if len(sent.object) == 0:
                        sent.object = sent.inputSent[wordPosition - 1] #    taggedInput[wordPosition - 1]
                    else:
                        if sent.isVar('_indirectObject'):
                            tmpInObj.append(sent._indirectObject)
                            sent._indirectObject = tmpInObj
                            sent._indirectObject.append(sent.inputSent[wordPosition - 1])
                        else:
                            sent._indirectobject = sent.inputSent[wordPosition - 1]
        else:
            if sent.isVar('_CC'):
                tmpSubj.append(sent.subject)
                sent.subject = tmpSubj
                sent.subject.append(sent.inputSent[wordPosition - 1])
                return sent

            if sent.isVar('_MD'):
                tmpSubj.append(sent.subject)
                sent.subject = tmpSubj
                sent.subject.append(sent.inputSent[wordPosition - 1])
                    
    return sent


def processNNPS(wordPosition, sent):

    if wordPosition == 1:
        sent.type = 'declarative'

        if sent.subject == '':
            sent.subject =  sent.inputSent[0]                        
    else:
        if sent.type == '':
            sent.type = 'declarative'
        if sent.subject == '':
                sent.subject = sent.inputSent[wordPosition - 1]
        else:
            if sent.object == '':
                sent.object = sent.inputSent[wordPosition - 1]
            else:
                if sent.isVar('_indirectObject'):
                    tmpInObj.append(sent._indirectObject)
                    sent._indirectObject = tmpInObj
                    sent._indirectObject.append(sent.inputSent[wordPosition - 1])
                else:
                    sent._indirectObject = sent.inputSent[wordPosition - 1]
                    
    return sent


def processPDT(wordPosition, sent):

    tmpPDT = []
    
    if sent.isVar('_PDT'):
        tmpPDT.append(sent._PDT)
        tmpPDT.append(sent.inputSent[wordPosition - 1])
        sent._PDT = tmpPDT
    else:
        sent._PDT = sent.inputSent[wordPosition - 1]

    return sent


def processPOS(wordPosition, sent):

    tmpPOS = []
    
    if sent.isVar('_POS'):
        tmpPOS.append(sent._POS)
        tmpPOS.append(sent.inputSent[wordPosition - 1])
        sent._POS = tmpPOS
    else:
        sent._POS = sent.inputSent[wordPosition - 1]

    return sent


def processPRP(wordPosition, sent):

    tmpInObj = []
    tmpSubj = []

    if wordPosition == 1:
        sent.type = 'declarative'

        if sent.subject == '':
            sent.subject = sent.inputSent[0]
    else:
        if sent.type == '':
            sent.type = 'declarative'
            
        if sent.subject == '':
            sent.subject = sent.inputSent[wordPosition - 1]
     
    return sent


def processPRPS(wordPosition, sent):

    tmpPRPS = []
    
    if sent.isVar('_PRPS'):
        tmpPRPS.append(sent._PRPS)
        tmpPRPS.append(sent.inputSent[wordPosition - 1])
        sent._PRPS = tmpPRPS
    else:
        sent._PRPS = sent.inputSent[wordPosition - 1]

    return sent


def processRB(wordPosition, sent):

    tmpRB = []

    if wordPosition == 1:
        sent.type = 'declarative'
        sent._RB = sent.inputSent[0]
    else:
        if sent.isVar('_RB'):
            tmpRB.append(sent._RB)
            tmpRB.append(sent.inputSent[wordPosition - 1])
            sent._RB = tmpRB
        else:
            sent._RB = sent.inputSent[wordPosition - 1]

    return sent


def processRBR(wordPosition, sent):

    tmpRBR = []
    
    if sent.isVar('_RBR'):
        tmpRBR.append(sent._RBR)
        tmpRBR.append(sent.inputSent[wordPosition - 1])
        sent._RBR = tmpRBR
    else:
        sent._RBR = sent.inputSent[wordPosition - 1]

    return sent


def processRBS(wordPosition, sent):

    tmpRBS = []
    
    if sent.isVar('_RBS'):
        tmpRBS.append(sent._RBS)
        tmpRBS.append(sent.inputSent[wordPosition - 1])
        sent._RBS = tmpRBS
    else:
        sent._RBS = sent.inputSent[wordPosition - 1]

    return sent


def processRP(wordPosition, sent):

    tmpRP = []
    
    if sent.isVar('_RP'):
        tmpRP.append(sent._RP)
        tmpRP.append(sent.inputSent[wordPosition - 1])
        sent._RP = tmpRP
    else:
        sent._RP = sent.inputSent[wordPosition - 1]

    return sent


def processSYM(wordPosition, sent):

    tmpSYM = []
    
    if sent.isVar('_SYM'):
        tmpSYM.append(sent._SYM)
        tmpSYM.append(sent.inputSent[wordPosition - 1])
        sent._SYM = tmpSYM
    else:
        sent._SYM = sent.inputSent[wordPosition - 1]

    return sent


def processTO(wordPosition, sent):

    tmpTO = []
    
    if sent.isVar('_TO'):
        tmpTO.append(sent._TO)
        tmpTO.append(sent.inputSent[wordPosition - 1])
        sent._TO = tmpTO
    else:
        sent._TO = sent.inputSent[wordPosition - 1]

    return sent


def processUH(wordPosition, sent):

    tmpUH = []

    if wordPosition == 1:
        sent.type = 'declarative'
        sent._UH = sent.inputSent[0]
    else:
        if sent.isVar('_UH'):
            tmpUH.append(sent._UH)
            tmpUH.append(sent.inputSent[wordPosition - 1])
            sent._UH = tmpUH
        else:
            sent._UH = sent.inputSent[wordPosition - 1]

    return sent


def processVBX(wordPosition, sent): # Attempt to process all verbs

    #print('Big verb')
    tmpVerbs = []
    taggedVerb = sent.inputSent[wordPosition - 1]
    #print('taggedVerb: ', taggedVerb)
    #print('sent.verb: ', sent.verb)

    if wordPosition == 1:
        if sent.inputSent[0][0] in commandWords:
            sent.type = 'imperative'
        else:
            sent.type = 'declarative'
            
        #sent.verb = sent.inputSent[0]
        sent.verb = taggedVerb
    else:
        if sent.verb == '':
            #sent.verb = sent.inputSent[wordPosition - 1]
            sent.verb = taggedVerb
        else:
            if isinstance(sent.verb, tuple):
                tmpVerbs.append(sent.verb)
            elif isinstance(sent.verb, list):
                for vT in sent.verb:
                    tmpVerbs.append(vT)

            tmpVerbs.append(taggedVerb)
            sent.verb = tmpVerbs

    return sent


def processWDT(wordPosition, sent):

    tmpWDT = []

    if wordPosition == 1:
        sent.type = 'interrogative'
        sent._WDT = sent.inputSent[0]
    else:
        if sent.isVar('_WDT'):
            tmpWDT.append(sent._MD)
            tmpWDT.append(sent.inputSent[wordPosition - 1])
            sent._WDT = tmpWDT
        else:
            sent.sWDT = sent.inSent[wordPosition - 1]
            
    return sent


def processWP(wordPosition, sent):

    tmpWP = []
    
    if sent.isVar('_WP'):
        tmpWP.append(sent._WP)
        tmpWP.append(sent.inputSent[wordPosition - 1])
        sent._WP = tmpWP
    else:
        sent._WP = sent.inputSent[wordPosition - 1]

    return sent


def processWPS(wordPosition, sent):

    tmpWPS = []
    
    if sent.isVar('_WPS'):
        tmpWPS.append(sent._WPS)
        tmpWPS.append(sent.inputSent[wordPosition - 1])
        sent._WPS = tmpWPS
    else:
        sent._WPS = sent.inputSent[wordPosition - 1]

    return sent


def processWRB(wordPosition, sent):

    tmpWRB = []
    
    if sent.isVar('_WRB'):
        tmpWRB.append(sent._WRB)
        tmpWRB.append(sent.inputSent[wordPosition - 1])
        sent._WRB = tmpWP
    else:
        sent._WP = sent.inputSent[wordPosition - 1]

    return sent




# Attempt to analyze the input sentence
#   from just POS tags (find SVO)
####################################################
def sentAnalysis(taggedInput):
   
    print('--- sentAnalysis ---')
    error = []
    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''

    
    wordPosition = 0

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj)
    
    for item in taggedInput:

        wordPosition += 1
        currentWord = item[0]
        currentTag = item[1]

        if wordPosition == 1:    # Only keep NNPs capitalized
            if currentTag not in ['NNP']:
                currentWord = currentWord.lower()

        #print('currentWord: ', currentWord)
        #print('currentTag: ', currentTag)

        # Process part-of-speech tags from Penn Treebank Project
        #
        if currentTag in ['CC']:        # Coordinating conjunction
            sent = processCC(wordPosition, sent)

        elif currentTag in ['CD']:      # Cardinal number
            sent = processCD(wordPosition, sent)

        elif currentTag in ['DT']:      # Determiner
            sent = processDT(wordPosition, sent)

        elif currentTag in ['EX']:      # Existential there
            sent = processEX(wordPosition, sent)

        elif currentTag in ['FW']:      # Foreign word
            sent = processEX(wordPosition, sent)

        elif currentTag in ['IN']:      # Preposition or subordinating conjunction
            sent = processIN(wordPosition, sent)

        elif currentTag in ['JJ']:      # Adjective
            sent = processJJ(wordPosition, sent)

        elif currentTag in ['JJR']:     # Adjective, comparative
            sent = processJJR(wordPosition, sent)

        elif currentTag in ['JJS']:     # Adjective, superlative
            sent = processJJS(wordPosition, sent)

        elif currentTag in ['LS']:      # List item maker
            sent = processLS(wordPosition, sent)

        elif currentTag in ['MD']:      # Modal
            sent = processMD(wordPosition, sent)

        elif currentTag in ['NN']:      # Noun, singular or mass
            sent = processNN(wordPosition, sent)

        elif currentTag in ['NNS']:     # Noun, plural
            sent = processNNS(wordPosition, sent)

        elif currentTag in ['NNP']:     # Proper noun, singular
            sent = processNNP(wordPosition, sent)

        elif currentTag in ['NNPS']:    # Proper noun, plural
            sent = processNNPS(wordPosition, sent)

        elif currentTag in ['PDT']:     # Predeterminer
            sent = processPDT(wordPosition, sent)

        elif currentTag in ['POS']:     # Possessive ending
            sent = processPOS(wordPosition, sent)

        elif currentTag in ['PRP']:     # Personal pronoun
            sent = processPRP(wordPosition, sent)

        elif currentTag in ['PRP$']:    # Possessive pronoun PRP$ or PRPS
            sent = processPRPS(wordPosition, sent)

        elif currentTag in ['RB']:      # Adverb
            sent = processRB(wordPosition, sent)

        elif currentTag in ['RBR']:     # Adverb, comparative
            sent = processRBR(wordPosition, sent)

        elif currentTag in ['RBS']:     # Adverb, superlative
            sent = processRBS(wordPosition, sent)

        elif currentTag in ['RP']:      # Particle
            sent = processRP(wordPosition, sent)

        elif currentTag in ['SYM']:     # Symbol
            sent = processSYM(wordPosition, sent)

        elif currentTag in ['TO']:      # to
            sent = processTO(wordPosition, sent)

        elif currentTag in ['UH']:      # Interjection
            sent = processUH(wordPosition, sent)

        elif currentTag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:   # Process all verbs
            sent = processVBX(wordPosition, sent)
  
        #elif currentTag in ['VB']:      # Verb, base form
        #    sent = processVB(wordPosition, sent)
        #
        #elif currentTag in ['VBD']:     # Verb, past tense
        #    sent = processVBD(wordPosition, sent)
        #
        #elif currentTag in ['VBG']:     # Verb, gerund or present participle
        #    sent = processVBG(wordPosition, sent)
        #    
        #elif currentTag in ['VBN']:     # Verb, past participle
        #    sent = processVBN(wordPosition, sent)
        #
        #elif currentTag in ['VBP']:     # Verb, non-3rd person singular present
        #    sent = processVBP(wordPosition, sent)
        #    
        #elif currentTag in ['VBZ']:     # Verb, 3rd person singular present
        #    sent = processVBZ(wordPosition, sent)
        
        elif currentTag in ['WDT']:     # Wh-determiner
            sent = processWDT(wordPosition, sent)

        elif currentTag in ['WP']:      # Wh-pronoun
            sent = processWP(wordPosition, sent)

        elif currentTag in ['WPS']:     # Possessive wh-pronoun WP$
            sent = processWPS(wordPosition, sent)

        elif currentTag in ['WRB']:     # Wh-adverb
            sent = processWRB(wordPosition, sent)

        else:
            print('sentAnalysis else -- something wrong or tag not defined?')
            print('word position: {}, current word: {}, current tag: {}'.format(wordPosition, currentWord, currentTag))
            error.append('sentAnalysis else -- something wrong or tag not defined?')
            error.append('word position: ')
            error.append(wordPosition)
            error.append('word position: ')
            error.append('current word: ')
            error.append(currentWord)
            error.append('current tag: ')
            error.append(currentTag)

    # Sanity check:
    #
    if sent.subject == '':
        print('*Error* No subect found: ')
        error.append('No subect found')
        
    if sent.verb == '':
        print('*Error* No verb found: ')
        error.append('No verb found')
    
    return sent, error
# End sentAnalysis



if __name__ == "__main__":

    kbTree = None

#    tagged_uI = [['see', 'VBP'], ['hammy', 'NNP'], ['run', 'VB']]
#    tagged_uI = [['see', 'VBP'], ['hammy', 'NNP'], ['run', 'VB'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN']]
#    tagged_uI = [['bob', 'NNP'], ['was', 'VBD'], ['happy', 'JJ']]
#    tagged_uI = [['bob', 'NNP'], ['saw', 'VBD'], ['pookie', 'NNP']]
#    tagged_uI = [['bob', 'NNP'], ['walked', 'VBD'], ['pookie', 'NNP'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['hammy', 'NNP']]
#    tagged_uI = [['bob', 'NNP'], ['and', 'CC'], ['mary', 'NNP'], ['walked', 'VBD'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['pookie', 'NNP']]

    tagged_uI = [('Bob', 'NNP'), ('is', 'VBZ'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('with', 'IN'), ('Pookie', 'NNP'), ('and', 'CC'), ('Hammy', 'NNP')]

    sA_Obj, error = sentAnalysis(tagged_uI)

    if len(error) > 0:
        for e in error:
            print(e)

    sA_Obj.printAll()
 
 
    
