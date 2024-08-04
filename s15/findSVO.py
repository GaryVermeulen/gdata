#
# findSVO.py
#
#   Determine Subject, Verb, Objects of simple senteneces.
#   This follows strict SVO, and fails if the input
#   is other than SVO (EX: SOV or VSO).
#

import sys

from processNNXs import processNNXs

#from commonConfig import *
from commonConfig import Sentence, nnx, prpx, vbx

import pickle
pickleFileIn = 'data/processedCorpora.p'
pickleFileOut = 'data/foundSVO.p'

def getSubjectWords(sent):

    # Just return a list of just the subject(s) words (no tags)
    subWords = []
    subs = sent.subject
    
    for s in subs:
        subWords.append(s['word'])

    return subWords


def getObjectWords(sent):

    # Just return a list of just the subject(s) words (no tags)
    objWords = []
    objs = sent.object
    
    for s in objs:
        objWords.append(s['word'])

    return objWords

    
def findSVO(inputSentence, taggedSentence):
   
#    print('START: --- findSVO ---')
#
#    print('inputSentence type: ', type(inputSentence))
#    print('inputSentence:')
#    print(inputSentence)
#
#    print('taggedSentence type: ', type(taggedSentence))
#    print('taggedSentence:')
#    print(taggedSentence)

    # Let's count the number of nouns and pronouns for sanity check later...
    nnxLst = []
    for w in taggedSentence:
        if (w['tag'] in nnx) or (w['tag'] in prpx):
#            print('nnx or prpx found: ', w)
            nnxLst.append(w)

    processedSentence = []
    currentWordPosition = 0

    #sent = Sentence(taggedSentence, '', [], [], [])
    newSentObj = Sentence(inputSentence, taggedSentence)

    for inputWord in taggedSentence:
        
        word = inputWord['word']
        tag  = inputWord['tag']

#        print('inputWord: ', inputWord)
#
#        print('word: ', word)
#        print('tag: ', tag)
#
#        print('processedSentence:')
#        print(processedSentence)

        if tag in nnx:

            newSentObj = processNNXs(inputWord, newSentObj, processedSentence, currentWordPosition)
            
#            if newSentObj.subject == None:
#                newSentObj.subject = []
#                newSentObj.subject.append(inputWord)
#                currentWordPosition += 1
#                processedSentence.append(inputWord)
#                continue
#            
#            # Check for full name i.e. John Doe
#            print('[-1]: ', processedSentence[-1])
#            if processedSentence[-1]['tag'] == 'NNP':
#                # Where is it? Subject? object? or indirectObject?
#                # Using strict SVO:
#                if newSentObj.verb == None:
#                    newSentObj.subject.append(inputWord)
#                else:
#                    if newSentObj.object == None:
#                        newSentObj.object = []
#                    newSentObj.object.append(inputWord)
#                currentWordPosition += 1
#                processedSentence.append(inputWord)
#                continue
#  
#            # Is there a list? "Planes trains and boats are cool"
#            # What if: "Planes, trains, and boats..."????
#            if processedSentence[-1]['word'] == 'and':
#                subjectWords = getSubjectWords(newSentObj)
#                objectWords = getObjectWords(newSentObj)
#                    
#                if processedSentence[-2]['word'] in subjectWords: 
#                    sent.subject.append(inputWord)
#                elif processedSentence[-2]['word'] in objectWords:
#                    sent.object.append(inputWord)
#                        
#                currentWordPosition += 1
#                processedSentence.append(inputWord)
#                continue
#                            
#            # Default 
#            if (newSentObj.verb != None) and (newSentObj.object == None):
#                newSentObj.object = []
#                newSentObj.object.append(inputWord)
#            elif newSentObj.verb == None:
#                newSentObj.subject.append(inputWord)
#            else:
#                # ?
#                if processedSentence[-1]['tag'] != 'NNP': # Check for John Doe?
#                    newSentObj.object.append(inputWord)
#                        
#                    # Not worrying about direct or indirect objects
#                    #
#                    #if newSentObj.isVar('_indirectObject'):
#                    #    newSentObj._indirectObject.append(inputWord)
#                    #else:
#                    #    newSentObj._indirectObject = []
#                    #    newSentObj._indirectObject.append(inputWord)
#
        elif tag in prpx:
            if (newSentObj.verb == None) and (newSentObj.subject == None):
                newSentObj.subject = []
                newSentObj.subject.append(inputWord)
                
            elif (newSentObj.verb == None) and (newSentObj.subject != None):
                newSentObj.subject.append(inputWord)
                
            elif (newSentObj.verb != None) and (newSentObj.object == None):

                # Filter out: "He did his..."
                if newSentObj.subject[0]['tag'] in prpx:
#                    print('prpx found in subject--is there a subject possesive match?')
                    if pronounMatch(newSentObj.subject[0], inputWord):
#                        print('pronoun match!')
                        newSentObj.subject.append(inputWord) # Just to record it
                    else:
#                        print('no pronoun match...')
                        # This my not be the best...~?
                        newSentObj.object = []
                        newSentObj.object.append(inputWord)
                
            elif (newSentObj.verb != None) and (newSentObj.object != None):
                
                    
                newSentObj.object.append(inputWord) 

                # For now not worring about direct or indirect objects
                #
                #if newSentObj.isVar('_indirectObject'):
                #    newSentObj._indirectObject.append(inputWord)
                #else:
                #    newSentObj._indirectObject = []
                #    newSentObj._indirectObject.append(inputWord)
                    
            if newSentObj.isVar('_PRPX'):
                newSentObj._PRPX.append(inputWord)
            else:
                newSentObj._PRPX = []
                newSentObj._PRPX.append(inputWord)
                    
        elif tag in vbx:
            if newSentObj.verb == None:
                newSentObj.verb = []
            newSentObj.verb.append(inputWord)
            
        elif tag == 'WDT':
            if newSentObj.isVar('_WDT'):
                newSentObj._WDT.append(inputWord)
            else:
                newSentObj._WDT = []
                newSentObj._WDT.append(inputWord)
                    
        elif tag == 'WP':
            if newSentObj.isVar('_WP'):
                newSentObj._WP.append(inputWord)
            else:
                newSentObj._WP = []
                newSentObj._WP.append(inputWord)
                    
        elif tag == 'WPS':
            if newSentObj.isVar('_WPS'):
                newSentObj._WPS.append(inputWord)
            else:
                newSentObj._WPS = []
                newSentObj._WPS.append(inputWord)
                    
        elif tag == 'WRB':
            if newSentObj.isVar('_WRB'):
                newSentObj._WRB.append(inputWord)
            else:
                newSentObj._WRB = []
                newSentObj._WRB.append(inputWord)
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
            newSentObj.type = "imperative"
        else:
            newSentObj.type = "exclamative"
    else:
        if processedSentence[0]['tag'] in vbx: # Usally begins with a verb
            newSentObj.type = "imperative"
        else:
            newSentObj.type = "declarative"

    # Were all the nnx's matched up?
        
    #print('END: processedSentence:')
    #print(processedSentence)
    
    return newSentObj


def pronounMatch(pronoun, inputWord):

    # Check subject pronoun to possessive pronoun ex: he/his, she/hers

#    print('pronoun: ', pronoun)
#    print('inputWord: ', inputWord)

    if (pronoun['word'] in ['He', 'he']) and (inputWord['word'] in ['his']):
        return True
    elif (pronoun['word'] in ['She', 'she']) and (inputWord['word'] in ['hers']):
        return True

    return False



if __name__ == "__main__":

    print('START: --- findSVO main ---')
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
    #tagged_uI = [{'word': 'My', 'tag': 'PRP$'}, {'word': 'name', 'tag': 'NN'}, {'word': 'is', 'tag': 'VBZ'}, {'word': 'Allie', 'tag': 'NNP'}, {'word': 'Kay', 'tag': 'NNP'}, {'word': 'and', 'tag': 'CC'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'would', 'tag': 'MD'}, {'word': 'like', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'tell', 'tag': 'VB'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'about', 'tag': 'IN'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'first', 'tag': 'JJ'}, {'word': 'pet', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'However', 'tag': 'RB'}, {'word': ',', 'tag': ','}, {'word': 'before', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'can', 'tag': 'MD'}, {'word': ',', 'tag': ','}, {'word': 'you', 'tag': 'PRP'}, {'word': 'have', 'tag': 'VBP'}, {'word': 'to', 'tag': 'TO'}, {'word': 'understand', 'tag': 'VB'}, {'word': 'that', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'a', 'tag': 'DT'}, {'word': 'little', 'tag': 'RB'}, {'word': 'older', 'tag': 'JJR'}, {'word': 'than', 'tag': 'IN'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'are', 'tag': 'VBP'}, {'word': 'and', 'tag': 'CC'}, {'word': 'have', 'tag': 'VB'}, {'word': 'a', 'tag': 'DT'}, {'word': 'family', 'tag': 'NN'}, {'word': 'of', 'tag': 'IN'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'own', 'tag': 'JJ'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'Oh', 'tag': 'UH'}, {'word': '!', 'tag': '.'}]
    #tagged_uI = [{'word': 'Do', 'tag': 'VB'}, {'word': 'not', 'tag': 'RB'}, {'word': 'worry', 'tag': 'VB'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'not', 'tag': 'RB'}, {'word': 'going', 'tag': 'VBG'}, {'word': 'to', 'tag': 'TO'}, {'word': 'talk', 'tag': 'VB'}, {'word': 'to', 'tag': 'IN'}, {'word': 'you', 'tag': 'PRP'}, {'word': 'like', 'tag': 'IN'}, {'word': 'a', 'tag': 'DT'}, {'word': 'big', 'tag': 'JJ'}, {'word': 'person', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'I', 'tag': 'PRP'}, {'word': 'am', 'tag': 'VBP'}, {'word': 'going', 'tag': 'VBG'}, {'word': 'to', 'tag': 'TO'}, {'word': 'let', 'tag': 'VB'}, {'word': 'my', 'tag': 'PRP$'}, {'word': 'imagination', 'tag': 'NN'}, {'word': 'take', 'tag': 'VB'}, {'word': 'me', 'tag': 'PRP'}, {'word': 'back', 'tag': 'RB'}, {'word': 'in', 'tag': 'IN'}, {'word': 'time', 'tag': 'NN'}, {'word': 'to', 'tag': 'IN'}, {'word': 'when', 'tag': 'WRB'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'was', 'tag': 'VBD'}, {'word': '7', 'tag': 'CD'}, {'word': 'years', 'tag': 'NNS'}, {'word': 'old', 'tag': 'JJ'}, {'word': '.', 'tag': '.'}]
    #tagged_uI = [{'word': 'The', 'tag': 'DT'}, {'word': 'best', 'tag': 'JJS'}, {'word': 'part', 'tag': 'NN'}, {'word': 'is', 'tag': 'VBZ'}, {'word': 'that', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'do', 'tag': 'VBP'}, {'word': 'not', 'tag': 'RB'}, {'word': 'have', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'try', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'remember', 'tag': 'VB'}, {'word': 'everything', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]

    expandedCorpora = pickle.load( open(pickleFileIn, "rb" ) )

    print('len expandedCorpora: ', len(expandedCorpora))
    print('type expandedCorpora: ', type(expandedCorpora))

    
    objArr = []
    exitNow = False

    for corpus in expandedCorpora:
        print('len of corpus: ', len(corpus))
        
        bookName = corpus[0]
        bookText = corpus[1]
            
        print('bookName: ', bookName)
        print('bookText: ')
        print(type(bookText))
        print(len(bookText))
        tmpCnt = 0
        for s in bookText:
            tmpCnt += 1
            print('=========: ', tmpCnt)
            #s.printAll()
            #print('---------')
            svoObj = findSVO(s.inputSent, s.taggedSent)
            print('..... svoObj:')
            svoObj.printAll()
            print('---------')
            print('Save to an array...')
            objArr.append(svoObj)
            #if tmpCnt > 10:
            #    print("Only processing {} sentences...".format(tmpCnt))
            #    exitNow = True
            #    break
            #if exitNow:
            #    break
            
    print('*********')
    print('Check objArr...')
    print('len objArr: ', len(objArr))
    print('type objArr: ', type(objArr))
    #objCnt = 0
    #for obj in objArr:
    #    objCnt += 1
    #    print('---: ', objCnt)
    #    obj.printAll()
    #
    #print('objCnt: ', objCnt)
    print('*********')
    print('dump objArr to pickle...')
    pickle.dump(objArr, open(pickleFileOut, "wb" ) )

        
                    #sys.exit("TEMP EXIT")

#    svoObj = findSVO(tagged_uI)



    print('---')
   
#    svoObj.printAll()
 
 
    print('\nEND: --- findSVO main ---')    
