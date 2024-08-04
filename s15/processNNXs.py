# processNNXs.py
#
# Breaking down the SVO rules...
#

def processNNXs(inputWord, newSentObj, processedSentence, currentWordPosition):
    
    if newSentObj.subject == None:
        newSentObj.subject = []
        newSentObj.subject.append(inputWord)
        currentWordPosition += 1
        processedSentence.append(inputWord)
        #continue
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
            sent.subject.append(inputWord)
        elif processedSentence[-2]['word'] in objectWords:
            sent.object.append(inputWord)
                        
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
                    
    return newSentObj
