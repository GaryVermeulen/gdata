#
# findSVO.py
#
#   Determine Subject, Verb, Objects of simple senteneces.
#   This follows strict SVO, and fails if the input
#   is other than SVO (EX: SOV or VSO).
#

import sys

#from commonConfig import *
from commonConfig import Sentence, nnx, prpx, vbx

import pickle
pickleFileIn = 'data/processedCorpora.p'
pickleFileOut = 'data/objArr.p'

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


def getObjectWords(sent):
    # Just return a list of just the subject(s) words (no tags)
    objWords = []
    objs = sent.object
    
    if isinstance(objs, tuple):
        objWords.append(objs[0])
    elif isinstance(objs, list):
        for s in objs:
            objWords.append(s[0])

    return objWords

    
def findSVO(taggedSentence):
   
#    print('START: --- findSVO ---')

    processedSentence = []
    currentWordPosition = 0

    sent = Sentence(taggedSentence, '', [], [], [])

    for inputWord in taggedSentence:
        word = inputWord[0]
        tag  = inputWord[1]

        if tag in nnx:
            if len(sent.subject) == 0:
                sent.subject.append(inputWord)
                currentWordPosition += 1
                processedSentence.append(inputWord)
                continue
            else:
                # Check for full name i.e. John Doe
                if processedSentence[-1][1] == 'NNP':
                    # Where is it? Subject? object? or indirectObject?
                    # Using strict SVO:
                    if len(sent.verb) == 0: 
                        sent.subject.append(inputWord)
                    else:
                        sent.object.append(inputWord)
                    currentWordPosition += 1
                    processedSentence.append(inputWord)
                    continue
  
                # Is there a list? "Planes trains and boats are cool"
                if processedSentence[-1][0] == 'and':
                    subjectWords = getSubjectWords(sent)
                    objectWords = getObjectWords(sent)
                    if processedSentence[-2][0] in subjectWords: 
                        sent.subject.append(inputWord)
                    elif processedSentence[-2][0] in objectWords:
                        sent.object.append(inputWord)
                    currentWordPosition += 1
                    processedSentence.append(inputWord)
                    continue
                            
                # Default 
                if len(sent.verb) > 0 and len(sent.object) == 0:
                    sent.object.append(inputWord)
                elif len(sent.verb) == 0:
                    sent.subject.append(inputWord)
                else:
                    # ?
                    if processedSentence[-1][1] != 'NNP': # Check for John Doe
                        if sent.isVar('_indirectObject'):
                            sent._indirectObject.append(inputWord)
                        else:
                            sent._indirectObject = []
                            sent._indirectObject.append(inputWord)

        elif tag in prpx:
            if len(sent.verb) == 0 and len(sent.subject) == 0:
                sent.subject.append(inputWord)
            elif len(sent.verb) == 0 and len(sent.subject) > 0:
                sent.subject.append(inputWord)
            elif len(sent.verb) > 0 and len(sent.object) == 0:
                sent.object.append(inputWord)
            elif len(sent.verb) > 0 and len(sent.object) > 0:
                if sent.isVar('_indirectObject'):
                    sent._indirectObject.append(inputWord)
                else:
                    sent._indirectObject = []
                    sent._indirectObject.append(inputWord)
                    
            if sent.isVar('_PRPX'):
                sent._PRPX.append(inputWord)
            else:
                sent._PRPX = []
                sent._PRPX.append(inputWord)
                    
        elif tag in vbx:
            sent.verb.append(inputWord)
            
        elif tag == 'WDT':
            if sent.isVar('_WDT'):
                sent._WDT.append(inputWord)
            else:
                sent._WDT = []
                sent._WDT.append(inputWord)
                    
        elif tag == 'WP':
            if sent.isVar('_WP'):
                sent._WP.append(inputWord)
            else:
                sent._WP = []
                sent._WP.append(inputWord)
                    
        elif tag == 'WPS':
            if sent.isVar('_WPS'):
                sent._WPS.append(inputWord)
            else:
                sent._WPS = []
                sent._WPS.append(inputWord)
                    
        elif tag == 'WRB':
            if sent.isVar('_WRB'):
                sent._WRB.append(inputWord)
            else:
                sent._WRB = []
                sent._WRB.append(inputWord)
        #else:
        #    print('ELSE: unknown tag? inputWord: ', inputWord)

#        print(processedSentence)
            
         # Tracking what we have processed for look back checking
        currentWordPosition += 1
        processedSentence.append(inputWord)
            

    if processedSentence[-1][0] == "?":
        sent.type = "interrogative"
    elif processedSentence[-1][0] == "!":
        if processedSentence[0][1] in vbx: # Usally begins with a verb
            sent.type = "imperative"
        else:
            sent.type = "exclamative"
    else:
        if processedSentence[0][1] in vbx: # Usally begins with a verb
            sent.type = "imperative"
        else:
            sent.type = "declarative"
        
    #print('END: processedSentence:')
    #print(processedSentence)
    
    return sent



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
        for c in corpus:
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
                print(s)
                print('---------')
                svoObj = findSVO(s)
                svoObj.printAll()
                print('---------')
                print('Save to an array...')
                objArr.append(svoObj)
                if tmpCnt > 10:
                    print("Only processing {} sentences...".format(tmpCnt))
                    exitNow = True
                    break
            if exitNow:
                break
            
    print('*********')
    print('Check objArr...')
    print('len objArr: ', len(objArr))
    print('type objArr: ', type(objArr))
    objCnt = 0
    for obj in objArr:
        objCnt += 1
        print('---: ', objCnt)
        obj.printAll()

        
    print('*********')
    print('dump objArr to pickle...')
    pickle.dump(objArr, open(pickleFileOut, "wb" ) )

        
                    #sys.exit("TEMP EXIT")

#    svoObj = findSVO(tagged_uI)



    print('---')
   
#    svoObj.printAll()
 
 
    print('\nEND: --- findSVO main ---')    
