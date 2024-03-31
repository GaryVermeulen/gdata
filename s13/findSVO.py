#
# findSVO.py
#
#   Determine Subject, Verb, Objects of sentenece.
#


from commonConfig import *



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
    

def findSVO(taggedSentence):
   
#    print('START: --- findSVO ---')
    taggedInput = []
    error = []

    # Change input from dict to tuple
    for wt in taggedSentence:
        taggedInput.append((wt["word"], wt["tag"]))
        
#    print('findSVO: taggedInput: ')
#    print(taggedInput)
#    print('-----')
    
    processedSentence = []
    currentWordPosition = 0

    sent = Sentence(taggedInput, '', [], [], [])

    for inputWord in taggedInput:
#        print('---')
#        print(currentWordPosition)
#        print(inputWord)
        word = inputWord[0] # was [0]
        tag  = inputWord[1]  # was [1]
#        print('word: ', word)
#        print('tag:  ', tag)
#        print('processedSentence: ', processedSentence)
        
        if currentWordPosition == 0: # Not much we can with just one word
            if word in commandWords:
                sent.type = "imperative"
                
            if tag in nnx:
                sent.subject.append(inputWord)

            elif tag in prpx:
                
                if taggedInput[currentWordPosition + 1][1] in vbx: # I ran, She ran, ...
                    sent.subject.append(inputWord)

                elif taggedInput[currentWordPosition + 1][1] == 'MD': # I could, ...
                    sent.subject.append(inputWord)

                elif taggedInput[currentWordPosition + 1][1] == 'CC': # Me and my arrow...
                    sent.subject.append(inputWord)

                else:    
                    print('findSVO, prpx (currentWordPosition == 0), 2nd word else undefined: ', taggedInput[currentWordPosition + 1])
                    
            elif tag in vbx:
                sent.verb.append(inputWord)

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
                           
            # Default sentence type...~?
            if len(sent.type) == 0:
                sent.type = "declarative"

#            print('End of 1st word:')
                                    
        else:
            # Do we really need to check for every POS tag type?
            # Only checking nnx, vbx, whx
            #
            if tag in nnx:
#                print('nnx: ', inputWord)
                
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
                        if processedSentence[-1][1] != 'NNP': # Check for John Doe
                            if sent.isVar('_indirectObject'):
                                sent._indirectObject.append(inputWord)
                            else:
                                sent._indirectObject = []
                                sent._indirectObject.append(inputWord)
#                print('bottom of nnx:')
#                sent.printAll()
                        
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
            
#        print('bottom of the big if:')
#        sent.printAll()
        currentWordPosition += 1

        processedSentence.append(inputWord) # Tracking what we have processed for back-tracking/checking
    
#    print('END: --- findSVO ---')
    return sent, error



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
    tagged_uI = [{'word': 'The', 'tag': 'DT'}, {'word': 'best', 'tag': 'JJS'}, {'word': 'part', 'tag': 'NN'}, {'word': 'is', 'tag': 'VBZ'}, {'word': 'that', 'tag': 'IN'}, {'word': 'I', 'tag': 'PRP'}, {'word': 'do', 'tag': 'VBP'}, {'word': 'not', 'tag': 'RB'}, {'word': 'have', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'try', 'tag': 'VB'}, {'word': 'to', 'tag': 'TO'}, {'word': 'remember', 'tag': 'VB'}, {'word': 'everything', 'tag': 'NN'}, {'word': '.', 'tag': '.'}]
    

    svoObj, error2 = findSVO(tagged_uI)

    print('---')

    if len(error2) > 0:
        for e in error2:
            print(e)

    svoObj.printAll()
 
 
    print('\nEND: --- findSVO main ---')    
