#
# simpSA.py
#
#   Sentence analysis--attempt to determine SVO
#   This version takes a tagged input sentence instead of
#   a CFG tree
#
""" Notes:

    declarative sentence (statement)
    interrogative sentence (question)
    imperative sentence (command)
    exclamative sentence (exclamation)\
    

    Per Wordy.com

        Subject–Verb
        Subject–Verb–Object
        Subject–Verb–Adjective
        Subject–Verb–Adverb
        Subject–Verb–Noun


    Per english.com:
    
        1.) A sentence is a group of words that has a complete thought, meaning or idea.
        2.) Every English sentence starts with a Subject followed by a Verb.
        3.) Every English sentence must have a verb.
        4.) A Subject tells who or what the sentence is about.
        5.) The Verb is the action word that tells what someone or something does.
        6.) Add -s to most verbs to tell about one person, place or a thing. e.g One bird stops.
        7.) The words (am, is, are) are verbs called (to-be) They tell about now. e.g. I am six. Kip is little
        8.) Use AM to tell about yourself. Use IS to tell about one person, thing, place. Use ARE to tell about more than one.
        9.) A noun names a person, animal, place or a thing.
        10.) A sentence always starts with a capital letter and ends with an ending mark.


    Per waldenu.edu:
    
    Simple sentences:
        A simple sentence is an independent clause with no conjunction or dependent clause.
        
    Compound sentences:
        A compound sentence is two independent clauses joined by a conjunction (e.g., and, but, or, for, nor, yet, so).
        
    Complex sentences:
        A complex sentence contains one independent clause and at least one dependent clause. The clauses in a complex
        sentence are combined with conjunctions and subordinators, terms that help the dependent clauses relate to the
        independent clause. Subordinators can refer to the subject (who, which), the sequence/time (since, while), or the
        causal elements (because, if) of the independent clause.
        
    Compound-complex sentences:
        A compound-complex sentence contains multiple independent clauses and at least one dependent clause. These
        sentences will contain both conjunctions and subordinators.

    
"""

from commonConfig import *

        
def processNPP(wordPosition, sent):

    tmpInObj = []
    tmpSubj = []
    """
    if verbose: 
        print('taggedInput to processNNP:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """ 
    if wordPosition == 1:
        sent.sType = 'declarative'

        if sent.sSubj == '':
            sent.sSubj =  sent.inSent[0] # taggedInput[0]                        
    else:
        if sent.sType == '':
            sent.sType = 'declarative'

        if sent.sVerb != '':
            if sent.sSubj == '':
                sent.sSubj = sent.inSent[wordPosition - 1] #    taggedInput[wordPosition - 1]
            else:
                if sent.sObj == '':
                    sent.sObj = sent.inSent[wordPosition - 1] #    taggedInput[wordPosition - 1]
                else:
                    if sent.sInObj == '':
                        sent.sInObj = sent.inSent[wordPosition - 1] #    taggedInput[wordPosition - 1]
                    else:
                        tmpInObj.append(sent.sObj)
                        sent.sInObj = tmpInObj
                        sent.sInObj.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
        else:
            if sent.sCC != '':
                tmpSubj.append(sent.sSubj)
                sent.sSubj = tmpSubj
                sent.sSubj.append(sent.inSent[wordPosition - 1]) #    taggedInput[wordPosition - 1])
                    
    return sent


def processPRP(wordPosition, sent):

    tmpInObj = []
    tmpSubj = []
    """
    if verbose: 
        print('taggedInput to processPRP:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """ 
    if wordPosition == 1:
        sent.sType = 'declarative'

        if sent.sSubj == '':
            sent.sSubj = sent.inSent[0] # taggedInput[0]                        
    else:
        if sent.sType == '':
            sent.sType = 'declarative'
            
        if sent.sSubj == '':
            sent.sSubj = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]                        
     
    return sent


def processNN(wordPosition, sent):

    tmpInObj = []
    tmpObj = []
    """
    if verbose: 
        print('taggedInput to processNN:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'declarative'

        if sent.sSubj == '':
            sent.sSubj = sent.inSent[0] # taggedInput[0]                        
    else:
        if sent.sType == '':
            sent.sType = 'declarative'

        if sent.sVerb != '':
            if sent.sSubj == '':
                sent.sSubj = sent.inSent[wordPosition - 1]
            else:
                if sent.sObj == '':
                    sent.sObj = sent.inSent[wordPosition - 1]
                else:
                    if sent.sInObj == '':
                        sent.sInObj = sent.inSent[wordPosition - 1] 
                    else:
                        tmpInObj.append(sent.sObj)
                        sent.sInObj = tmpInObj
                        sent.sInObj.append(sent.inSent[wordPosition - 1]) 
        else:
            if sent.sDet != '':
                if sent.sSubj == '':
                    sent.sSubj = sent.inSent[wordPosition - 1]

            if sent.inSent[wordPosition - 2][1] == 'DT':
                if sent.sObj == '':
                        sent.sObj = sent.inSent[wordPosition - 1]
                else:
                    tmpObj.append(sent.sObj)
                    sent.sObj = tmpInObj
                    sent.sObj.append(sent.inSent[wordPosition - 1])
            
    return sent


def processVerbs(wordPosition, sent):

    tmpVerbs = []
    """
    if verbose: 
        print('taggedInput to processVerbs:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        if sent.inSent[0][0] in commandWords:
            sent.sType = 'imperative'
        else:
            sent.sType = 'declarative'
            
        sent.sVerb = sent.inSent[0]
    else:
        if sent.sVerb == '':
            sent.sVerb = sent.inSent[wordPosition - 1]
        else:
            tmpVerbs.append(sent.sVerb)
            tmpVerbs.append(sent.inSent[wordPosition - 1])
            sent.sVerb = tmpVerbs

    return sent


def processAdj(wordPosition, sent):

    tmp = []
    """
    if verbose: 
        print('taggedInput to processAdj:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'declarative'
        sent.sAdj = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sAdj == '':
            sent.sAdj = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmp.append(sent.sAdj)
            tmp.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sAdj = tmp

    return sent


def processDT(wordPosition, sent):

    tmpDet = []
    """
    if verbose: 
        print('taggedInput to processDT:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'declarative'
        sent.sDet = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sDet == '':
            sent.sDet = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmpDet.append(sent.sDet)
            tmpDet.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sDet = tmpDet

    return sent


def processIN(wordPosition, sent):

    tmpIN = []
    """
    if verbose: 
        print('taggedInput to processIN:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'declarative'
        sent.sIN = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sIN == '':
            sent.sIN = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmpIN.append(sent.sIN)
            tmpIN.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sIN = tmpIN

    return sent


def processMD(wordPosition, sent):

    tmpMD = []
    """
    if verbose: 
        print('taggedInput to processMD:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        if sent.inSent[0][0] == 'can':
            sent.sType = 'interrogative'
        else:
            sent.sType = 'declarative'
        sent.sMD = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sMD == '':
            sent.sMD = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmpMD.append(sent.sMD)
            tmpMD.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sMD = tmpMD

    return sent


def processWDT(wordPosition, sent):

    tmpWDT = []
    """
    if verbose: 
        print('taggedInput to processWDT:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'interrogative'
        sent.sWDT = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sWDT == '':
            sent.sWDT = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmpWDT.append(sent.sMD)
            tmpWDT.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sWDT = tmpWDT

    return sent


def processCC(wordPosition, sent):

    tmpCC = []
    """
    if verbose: 
        print('taggedInput to processCC:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)
    """
    if wordPosition == 1:
        sent.sType = 'declarative?'
        sent.sCC = sent.inSent[0] # taggedInput[0]
    else:
        if sent.sCC == '':
            sent.sCC = sent.inSent[wordPosition - 1] # taggedInput[wordPosition - 1]
        else:
            tmpCC.append(sent.sCC)
            tmpCC.append(sent.inSent[wordPosition - 1]) # taggedInput[wordPosition - 1])
            sent.sCC = tmpCC

    return sent


def processRB(wordPosition, sent):

    tmpRB = []

    if wordPosition == 1:
        sent.sType = 'declarative'
        sent.sRB = sent.inSent[0]
    else:
        if sent.sRB == '':
            sent.sRB = sent.inSent[wordPosition - 1]
        else:
            tmpRB.append(sent.sRB)
            tmpRB.append(sent.inSent[wordPosition - 1])
            sent.sRB = tmpRB

    return sent



def getTag(item):

    currentWord = item[0]

    tempWords = currentWord.split(',')
    if len(tempWords) != 1:
        print(' ** tempWords len err **')
        
    currentTag = item[1]

    tempTags = currentTag.split(',')
    if len(tempTags) == 0:
        print(' ** tempTags cannot eq 0 **')
    elif len(tempTags) > 1:
        print(' ** tempTags greater then 1 -- returning first tag found **')
        currentTag = tempTags[0]        

    return currentWord, currentTag



# Attempt to analyze the input sentence
#   from just POS tags (find SVO)
####################################################
def sentAnalysis(taggedInput):
   
    print('--- sentAnalysis ---')

    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''
    sInObj = ''
    sAdj = ''
    sDet = ''
    sIN = ''
    sPP = ''
    sMD = ''
    sWDT = ''
    sCC = ''
    sRB = ''
    
    wordPosition = 0

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC, sRB)
#    print(' BEFORE:')
#    sent.printAll()
    
#    print('taggedInput to sentAnalysis:')
#    print(taggedInput)
    
    for item in taggedInput:

        wordPosition += 1

#        print('item: ', item)
#        print(len(item))
#        print(type(item))

        #currentWord, currentTag = getTag(item)
        currentWord = item[0]
        currentTag = item[1]
        
#        print('item[0]: ', item[0])
#        print('item[1]: ', item[1])

        if currentTag == 'NNP':
            sent = processNPP(wordPosition, sent)
#            print('NNP')
#            sent.printAll()
        
        elif currentTag in ['PRP', 'PRP$']:
            sent = processPRP(wordPosition, sent)
#            print('PRP...')
#            sent.printAll()

        elif currentTag in ['NN', 'NNS']:
            sent = processNN(wordPosition, sent)
#            print('NN...')
#            sent.printAll()
            
        elif currentTag in ['VB','VBD','VBG','VBN','VBP','VBZ']:
            sent = processVerbs(wordPosition, sent)
#            print('VB...')
#            sent.printAll()
            
        elif currentTag in ['JJ', 'JJR', 'JJS']:
            sent = processAdj(wordPosition, sent)
#            print('JJ...')
#            sent.printAll()
            
        elif currentTag in ['DT']:
            sent = processDT(wordPosition, sent)
#            print('DT')
#            sent.printAll()
            
        elif currentTag in ['IN']:
            sent = processIN(wordPosition, sent)
#            print('IN')
#            sent.printAll()
            
        elif currentTag in ['MD']:
            sent = processMD(wordPosition, sent)
#            print('MD')
#            sent.printAll()
            
        elif currentTag in ['CC']:
            sent = processCC(wordPosition, sent)
#            print('CC')
#            sent.printAll()

        elif currentTag in ['RB']:
            sent = processRB(wordPosition, sent)
#            print('CC')
#            sent.printAll()
          
        elif currentTag in ['WDT', 'WP', 'WRB']:
            sent = processWDT(wordPosition, sent)
#            print('WDT...')
#            sent.printAll()
        else:
            print('sentAnalysis else -- something wrong or tag not defined?')
            print('word position: {}, current word: {}, current tag: {}'.format(wordPosition, currentWord, currentTag))


    """
    if verbose: 
        print('--_-_-_-_-_-_-_-_-_-_--')
        print('Tagged Input Sentence:')
        print(taggedInput)
        print('----------------------')
        print('sType = ', sType)
        print('sSubj = ', sSubj)
        print('sVerb = ', sVerb)
        print('sObj =  ', sObj)
        print('sInObj - ', sInObj)
        print('sAdj =  ', sAdj) 
        print('sDet =  ', sDet)
        print('sIN =   ', sIN)
        print('sPP =   ', sPP)
        print('sMD =   ', sMD)
        print('sWDT =  ', sWDT)
        print('sCC =  ', sCC)
    """

    """
#        sent.inSent = inSent   # Set at init
    sent.sType  = sType
    sent.sSubj  = sSubj
    sent.sVerb  = sVerb
    sent.sObj   = sObj
    sent.sInObj = sInObj
    sent.sAdj   = sAdj
    sent.sDet   = sDet
    sent.sIN    = sIN
    sent.sPP    = sPP
    sent.sMD    = sMD
    sent.sWDT   = sWDT
    sent.sCC    = sCC
    """
    """
    if verbose:
        print('----------------------')
        print('sent.inSent: ', sent.inSent)
        print('sent.sType  = ', sent.sType)
        print('sent.sSubj  = ', sent.sSubj)
        print('sent.sVerb  = ', sent.sVerb)
        print('sent.sObj   = ', sent.sObj)
        print('sent.sInObj = ', sent.sInObj)
        print('sent.sAdj   = ', sent.sAdj)
        print('sent.sDet   = ', sent.sDet)
        print('sent.sIN    = ', sent.sIN)
        print('sent.sPP    = ', sent.sPP)
        print('sent.sMD    = ', sent.sMD)
        print('sent.sWDT   = ', sent.sWDT)
        print('sent.sCC    = ', sent.sCC)
    
    print('--- end sentAnalysis ---')
    """


    # Sanity check:
    #
    error = []
    
    if sent.sSubj == '':
        print('*Error* No subect found: ')
        error.append('No subect found')
        
    if sent.sVerb == '':
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
    tagged_uI = [['bob', 'NNP'], ['is', 'VBZ'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['pookie', 'NNP'], ['and', 'CC'], ['hammy', 'NNP']]

    sA_Obj, error = sentAnalysis(tagged_uI)

    if len(error) > 0:
        for e in error:
            print(e)

    sA_Obj.printAll()
