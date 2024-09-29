# processSVOs.py
#
# Supplement to Space; Find missing SVOs, and
# check for consistency.


import pickle
import copy 
#from collections import Counter
#from findSVO import findSVO
from commonConfig import Sentence, nnx, prpx, vbx
from resolvePronouns import resolvePronouns


pickleInputFile = 'pickleJar/taggedCorpora.p'
pickleFileOut = 'pickleJar/processedCorporaSVO.p'

def loadPickleData():

    with open(pickleInputFile, 'rb') as fp:
        corpora = pickle.load(fp)
#        print('Aunt Bee loaded corpora pickle.')
    fp.close()

    return corpora


def findSVO(sentObj):
   
    print('START: --- findSVO ---')
    #orgSentObj.printAll()
    #print('-----')

    global spacyProcessed
    global homemadeProcessed

    processedSentence = []
    currentWordPosition = 0

    SUBJECT_DEPS = ["nsubj", "nsubjpass", "csubj", "agent", "expl"]
    OBJECT_DEPS = ["dobj", "dative", "attr", "oprd"]

    #sent = Sentence(taggedSentence, '', [], [], [])
    ##newSentObj = Sentence(orgSentObj.inputSentence, orgSentObj.taggedSentenceShort, orgSentObj.taggedSentLong, orgSentObj.epistropheSent, )
    # WHY? newSentObj = copy.deepcopy(orgSentObj)   

    for inputWord in sentObj.epistropheSent:
        
        word = inputWord['word']
        tag  = inputWord['tag']


        # Per Spacy is this a subject?
        #if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
        if (inputWord["dep"] in SUBJECT_DEPS) or (inputWord["hdep"] in SUBJECT_DEPS):
            sentObj.subject.append(inputWord)
            processedSentence.append(inputWord)
            currentWordPosition += 1

            spacyProcessed.append(("Subject", inputWord))

            continue # For now...

        # Grab the verbs
        #if token.pos_ == "VERB":
        if inputWord["pos"] == "VERB":
            sentObj.verb.append(inputWord)
            processedSentence.append(inputWord)
            currentWordPosition += 1

            spacyProcessed.append(("Verb", inputWord))

            continue

        # Per Spacy is this a object?
        #if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
        if (inputWord["dep"] in OBJECT_DEPS) or (inputWord["hdep"] in OBJECT_DEPS):
            sentObj.object.append(inputWord)
            processedSentence.append(inputWord)
            currentWordPosition += 1

            spacyProcessed.append(("Object", inputWord))

            continue
              

        # Homemade mess...
        #
        
        if tag in nnx:

            print("if tag in nnx")
            
            if (sentObj.subject == None) or (len(sentObj.subject) == 0):
                sentObj.subject = []
                sentObj.subject.append(inputWord)
                currentWordPosition += 1
                processedSentence.append(inputWord)

                homemadeProcessed.append(("nnx subject", inputWord))

                continue # ???
            
            # Check for full name i.e. John Doe
            print("sentObj.inputSent: ", sentObj.inputSent)
            print("inputWord: ", inputWord)
            print('processedSentence: ', processedSentence)
            print('[-1]: ', processedSentence[-1])
            if processedSentence[-1]['tag'] == 'NNP':
                # Where is it? Subject? object? or indirectObject?
                # Using strict SVO:
                if sentObj.verb == None:
                    sentObj.subject.append(inputWord)
                else:
                    if sentObj.object == None:
                        sentObj.object = []
                    sentObj.object.append(inputWord)
                currentWordPosition += 1
                processedSentence.append(inputWord)
                
            # Is there a list? "Planes trains and boats are cool"
            # What if: "Planes, trains, and boats..."????
            if processedSentence[-1]['word'] == 'and':
                subjectWords = getSubjectWords(sentObj)
                objectWords = getObjectWords(sentObj)
                    
                if processedSentence[-2]['word'] in subjectWords: 
                    sentObj.subject.append(inputWord)
                elif processedSentence[-2]['word'] in objectWords:
                    sentObj.object.append(inputWord)
                        
                currentWordPosition += 1
                processedSentence.append(inputWord)
                           
            # Default 
            if (sentObj.verb != None) and (sentObj.object == None):
                sentObj.object = []
                sentObj.object.append(inputWord)
            elif sentObj.verb == None:
                sentObj.subject.append(inputWord)
            else:
                # ?
                if processedSentence[-1]['tag'] != 'NNP': # Check for John Doe?
                    sentObj.object.append(inputWord)

            homemadeProcessed.append(("nnx Subject or Object", inputWord))        
            print("END if tag in nnx") 
            
        elif tag in prpx:
            if (sentObj.verb == None) and (sentObj.subject == None):
                sentObj.subject = []
                sentObj.subject.append(inputWord)
                
            elif (sentObj.verb == None) and (sentObj.subject != None):
                sentObj.subject.append(inputWord)
                
            elif (sentObj.verb != None) and (sentObj.object == None):

                # Filter out: "He did his..."
                if sentObj.subject != None:
                    if sentObj.subject[0]['tag'] in prpx:
#                 print('prpx found in subject--is there a subject possesive match?')
                        if pronounMatch(sentObj.subject[0], inputWord):
#                           print('pronoun match!')
                            sentObj.subject.append(inputWord) # Just to record it
                        else:
#                            print('no pronoun match...')
                            # This my not be the best...~?
                            sentObj.object = []
                            sentObj.object.append(inputWord)
                
            elif (sentObj.verb != None) and (sentObj.object != None):
                                    
                sentObj.object.append(inputWord) 
                    
            if sentObj.isVar('_PRPX'):
                sentObj._PRPX.append(inputWord)
            else:
                sentObj._PRPX = []
                sentObj._PRPX.append(inputWord)

            homemadeProcessed.append(("prpx", inputWord))
                    
        elif tag in vbx:
            if sentObj.verb == None:
                sentObj.verb = []
            sentObj.verb.append(inputWord)

            homemadeProcessed.append(("vbx", inputWord))
            
        elif tag == 'WDT':
            if sentObj.isVar('_WDT'):
                sentObj._WDT.append(inputWord)
            else:
                sentObj._WDT = []
                sentObj._WDT.append(inputWord)

            homemadeProcessed.append(("WDT", inputWord))
                    
        elif tag == 'WP':
            if sentObj.isVar('_WP'):
                sentObj._WP.append(inputWord)
            else:
                sentObj._WP = []
                sentObj._WP.append(inputWord)

            homemadeProcessed.append(("WP", inputWord))
                    
        elif tag == 'WPS':
            if sentObj.isVar('_WPS'):
                sentObj._WPS.append(inputWord)
            else:
                sentObj._WPS = []
                sentObj._WPS.append(inputWord)

            homemadeProcessed.append(("WPS", inputWord))
            
        elif tag == 'WRB':
            if sentObj.isVar('_WRB'):
                sentObj._WRB.append(inputWord)
            else:
                sentObj._WRB = []
                sentObj._WRB.append(inputWord)

            homemadeProcessed.append(("WRB", inputWord))
        #else:
        #    print('ELSE: unknown tag? inputWord: ', inputWord)

#        print(processedSentence)
            
         # Tracking what we have processed for look back checking
        currentWordPosition += 1
        processedSentence.append(inputWord)
            

    if processedSentence[-1]['word'] == "?":
        newSentObj.type = "interrogative"
    elif processedSentence[-1]['word'] == "!":
        if processedSentence[0]['tag'] in vbx: # Usally begins with a verb
            sentObj.type = "imperative"
        else:
            sentObj.type = "exclamative"
    else:
        if processedSentence[0]['tag'] in vbx: # Usally begins with a verb
            sentObj.type = "imperative"
        else:
            sentObj.type = "declarative"

    #print("sentObj:")
    #sentObj.printAll()
    
    print('END: --- findSVO ---')
    
    return sentObj



def processNNXs(inputWord, newSentObj, processedSentence, currentWordPosition):

    print("START processNNXs...")
    print('inputWord: ', inputWord)
    print('newSentObj:')
    newSentObj.printAll()
    print('processedSentence: ', processedSentence)
    print('currentWordPosition: ', currentWordPosition)
    
    if newSentObj.subject == None:
        newSentObj.subject = []
        newSentObj.subject.append(inputWord)
        currentWordPosition += 1
        processedSentence.append(inputWord)
        print('newSentObj.subject == None')
        return newSentObj
    
    # Check for full name i.e. John Doe
#    print('[-1]: ', processedSentence[-1])
    if processedSentence[-1]['tag'] == 'NNP':
        # Where is it? Subject? object? or indirectObject?
        # Using strict SVO:
        if newSentObj.verb == None:
            newSentObj.subject.append(inputWord)
        else:
            if newSentObj.object == None:
                newSentObj.object = []
            newSentObj.object.append(inputWord)
        currentWordPosition += 1
        processedSentence.append(inputWord)
        #continue
        return newSentObj
  
    # Is there a list? "Planes trains and boats are cool"
    # What if: "Planes, trains, and boats..."????
    if processedSentence[-1]['word'] == 'and':
        subjectWords = getSubjectWords(newSentObj)
        objectWords = getObjectWords(newSentObj)
                    
        if processedSentence[-2]['word'] in subjectWords: 
            newSentObj.subject.append(inputWord)
        elif processedSentence[-2]['word'] in objectWords:
            newSentObj.object.append(inputWord)
                        
        currentWordPosition += 1
        processedSentence.append(inputWord)
        #continue
        return newSentObj
                           
    # Default 
    if (newSentObj.verb != None) and (newSentObj.object == None):
        newSentObj.object = []
        newSentObj.object.append(inputWord)
    elif newSentObj.verb == None:
        newSentObj.subject.append(inputWord)
    else:
        # ?
        if processedSentence[-1]['tag'] != 'NNP': # Check for John Doe?
            newSentObj.object.append(inputWord)
                        
            # Not worrying about direct or indirect objects
            #
            #if newSentObj.isVar('_indirectObject'):
            #    newSentObj._indirectObject.append(inputWord)
            #else:
            #    newSentObj._indirectObject = []
            #    newSentObj._indirectObject.append(inputWord)

    print("END processNNXs...") 
    return newSentObj




def getSubjectWords(sent):

    # Just return a list of just the subject(s) words (no tags)
    subWords = []
    subs = sent.subject

    if subs != None:
        for s in subs:
            subWords.append(s['word'])

    return subWords


def getObjectWords(sent):

    # Just return a list of just the subject(s) words (no tags)
    objWords = []
    objs = sent.object

    if objs != None:
        for s in objs:
            objWords.append(s['word'])

    return objWords



def pronounMatch(pronoun, inputWord):

    # Check subject pronoun to possessive pronoun ex: he/his, she/hers

#    print('pronoun: ', pronoun)
#    print('inputWord: ', inputWord)

    if (pronoun['word'] in ['He', 'he']) and (inputWord['word'] in ['his']):
        return True
    elif (pronoun['word'] in ['She', 'she']) and (inputWord['word'] in ['hers']):
        return True

    return False



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
            svoObj = findSVO(s)
            objArr.append(svoObj)
            
        newCorpora.append((bookName, objArr))

    return newCorpora




#
#
#
if __name__ == "__main__":

    print("Start: processSVOs...")

    spacyProcessed = []
    homemadeProcessed = []

    corpora = loadPickleData()

    # Resolve pronouns
    resolvedCorpora = resolvePronouns(corpora)

    # Find Subject-Verb-Objects
    processedCorporaSVO = findSVOs(resolvedCorpora)

    print('------------------ spacy')
    for i in spacyProcessed:
        print(i)

    print('------------------ homemade')
    for i in homemadeProcessed:
        print(i)

    
    # Save processedCorporaSVO
    with open(pickleFileOut, "wb") as f:
        pickle.dump(processedCorporaSVO, f)
    f.close()
    

    print("Completed: processSVOs.")
