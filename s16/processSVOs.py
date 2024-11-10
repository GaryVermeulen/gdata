# processSVOs.py
#
# Supplement to Spacy; Find missing SVOs, and
# check for consistency.


import pickle
import copy 
#from collections import Counter
#from findSVO import findSVO
from commonConfig import Sentence, nnx, prpx, vbx
#from resolvePronouns import resolvePronouns


pickleInputFile = 'pickleJar/tagged.p'
pickleFileOut = 'pickleJar/processedSVO.p'

# Gender pronouns
male = ['He', 'he', 'Him', 'him', 'His', 'his', 'Himself', 'himself']
female = ['She', 'she', 'Her', 'her', 'Hers', 'hers', 'Herself', 'herself']

def loadPickleData():

    with open(pickleInputFile, 'rb') as fp:
        corpus = pickle.load(fp)
    fp.close()

    return corpus


def resolvePronouns(processedCorpora):
    # Return a mapping of nouns to pronouns
    #print('START: resolvePronouns...')
    
    outputCorpora = []

    for corpus in processedCorpora:

        paragraphSubjectQueueMax = 5

        narratorName = None
    
        sentSubjectQueue = []
        paragraphSubjectQueue = []
        mappedSubjectQueue = []
        epistropheSents = []

        bookName = corpus[0]
        bookSents = corpus[1]

        #print('----------------------------')
        #print('bookName: ', bookName)
        #print('----------------------------')

        sentCount = 0
        for sentObj in bookSents:
            sentCount += 1
            # Added last setnences to paragraph queue
            for s in sentSubjectQueue:
                paragraphSubjectQueue.append(s)
                
            # Trim paragraphSubjectQueue if exceeds paragraphSubjectQueueMax
            if len(paragraphSubjectQueue) > paragraphSubjectQueueMax:
                        numToPop = range(len(paragraphSubjectQueue) - paragraphSubjectQueueMax)
                        for i in numToPop:
                            tmpPopped = paragraphSubjectQueue.pop(0)
                        #print("REMOVED {} from paragraphSubjectQueue...".format(numToPop))
            # Starting new sentence            
            sentSubjectQueue = []
            orgSent = sentObj.inputSent
            newSent = []
            #print('{} *** orgSent:'.format(bookSentCnt))
            #print(orgSent)
            #print(sentObj.taggedSentShort)
            #print('-----')
            #for taggedWord in sentObj.taggedSentShort:

            #print('+++++++++++++++++-----> Top: ', sentCount)
            #print("narratorName: ", narratorName)
            #print('taggedSentLong:')
            #print(sentObj.taggedSentLong)
            #for w in sentObj.taggedSentLong:
            #    print(w)
            #print('sentSubjectQueue:')
            #print(sentSubjectQueue)
            #print('---')
            #print('paragraphSubjectQueue:')
            #print(paragraphSubjectQueue)
            #print('---')
            #print('mappedSubjectQueue:')
            #print(mappedSubjectQueue)
            #print('---')

            for taggedWord in sentObj.taggedSentLong:
                #print('*** tagged word:')
                #print(taggedWord)

                #newWord = (taggedWord['word'], taggedWord['tag'])
                newWord = taggedWord
                oldWord = taggedWord

                # Add to subject queue: Spacy 'dep': 'tag': 'NNP',...,'nsubj',..., 'dep_exp': 'nominal subject'
                if ((taggedWord['tag'] == 'NNP') and (taggedWord['dep'] == 'nsubj')) or ((taggedWord['tag'] == 'NNP') and (taggedWord['hdep'] == 'nsubj')):
                    currentSent_nsubj = taggedWord
                    sentSubjectQueue.append((sentCount, taggedWord))
                    #print("Added taggedWord to sentSubjectQueue:")
                    #print(sentSubjectQueue)
                    
                    
                # Pronoun found--can we replace it with a noun?
                if ((taggedWord['tag'] == 'PRP')  and (taggedWord['dep'] == 'nsubj')) or ((taggedWord['tag'] == 'PRP') and (taggedWord['dep'] == 'dobj')):
                    #print('pronoun found:')
                    #print(taggedWord)

                    # Cheap "I" handeler and set narrator's name
                    if taggedWord['word'] == 'I':
                        # {'word': 'I', 'lemma': 'I', 'pos': 'PRON', 'tag': 'PRP', 'is_stop': True, 'dep': 'nsubj', 'hdep': 'ROOT', 'dep_exp': 'nominal subject'}
                        newWord = {'word': '[I, narrator]', 'lemma': 'narrator', 'pos': 'NOUN', 'tag': 'NN', 'is_stop': False, 'dep': 'nsubj', 'hdep': 'ROOT', 'dep_exp': 'nominal subject'}
                        newSent.append(newWord)
                        if narratorName == None:
                            # Check for narrator's name within this sentence
                            # e.g. "I am Bob...", "my name is Mary...", etc.
                            narratorName = setNarratorName(sentObj.taggedSentLong)
                        #print("The narrator's name is: ", narratorName)
                        continue

                    
                    if len(sentSubjectQueue) > 0:
                        # Has it been mapped previously?
                        if len(mappedSubjectQueue) > 0:
                            # Do pronouns match?
                            index = 0
                            found = False
                            for mappedItem in mappedSubjectQueue:
                                #print("mappedItem: ", mappedItem)
                                #print("top mappedItem[0]: ", mappedItem[0])
                                if (mappedItem[2]["word"] == taggedWord["word"]) or mappedItem[2]["lemma"] == taggedWord["lemma"]:
                                    #print("top mappedItem[3]:")
                                    #print(mappedItem[3])
                                    newWord = mappedItem[3]
                                    #print(">>> REPLACE: ", taggedWord)
                                    #print(">>> REPLACE WITH mappedItem: ", newWord)
                                    found = True
                                    idx = 0
                                    for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                        if sentSub == taggedWord:
                                            sentObj.subject.pop(idx)
                                            sentObj.subject.append(newWord)
                                        idx += 1
                                    trash = sentSubjectQueue.pop(index) # Eventhough we already mapped item, clean up sentSubjectQueue
                                index += 1
                            if not found:
                                # Queue hopefully is clean for a blind pop
                                popped = sentSubjectQueue.pop(0) # Blindly pop off the 1st in sent que
                                #print('blind pop: ', popped)
                                newWord = popped[1]

                                gender = setGender(taggedWord, newWord)
                            
                                mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                                #print("Added blind popped word to mappedSubjectQueue:")
                                #print(mappedSubjectQueue)
                                #print(">>> REPLACE: ", taggedWord)
                                #print(">>> REPLACE WITH queueItem: ", newWord)
                                idx = 0
                                for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                    if sentSub == taggedWord:
                                        sentObj.subject.pop(idx)
                                        sentObj.subject.append(newWord)
                                    idx += 1
                        else:
                            #for item in sentSubjectQueue:
                            #    print("else (NO CODE) - item: ", item)
                            
                            gender = setGender(taggedWord, newWord)
                            
                            mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                            #print("Added popped word to mappedSubjectQueue:")
                            #print(mappedSubjectQueue)
                            #print(">>> REPLACE: ", taggedWord)
                            #print(">>> REPLACE WITH: ", newWord)
                            idx = 0
                            for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                if sentSub == taggedWord:
                                    sentObj.subject.pop(idx)
                                    sentObj.subject.append(newWord)
                                idx += 1
                    else:
                        # First check current paragraph queue
                        if len(paragraphSubjectQueue) > 0:
                            popped = paragraphSubjectQueue.pop(0) # Blind pop...
                            newWord = popped[1]

                            gender = setGender(taggedWord, newWord)
                            
                            mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                            #print("Added popped word to mappedSubjectQueue:")
                            #print(mappedSubjectQueue)
                            #print(">>> REPLACE: ", taggedWord)
                            #print(">>> REPLACE WITH queueItem: ", newWord)
                            idx = 0
                            for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                if sentSub == taggedWord:
                                    sentObj.subject.pop(idx)
                                    sentObj.subject.append(newWord)
                                idx += 1
                        else:
                            # Check if was already mapped
                            if len(mappedSubjectQueue) > 0:
                                # Do pronouns match?
                                for mappedItem in mappedSubjectQueue:
                                    #print("mappedItem: ", mappedItem)
                                    #print("bottom mappedItem[0]: ", mappedItem[0])
                                    if (mappedItem[2]["word"] == taggedWord["word"]) or mappedItem[2]["lemma"] == taggedWord["lemma"]:
                                        #print("bottom mappedItem[3]:")
                                        #print(mappedItem[3])
                                        newWord = mappedItem[3]
                                        #print(">>> REPLACE: ", taggedWord)
                                        #print(">>> REPLACE WITH mappedItem: ", newWord)
                                        idx = 0
                                        for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                            if sentSub == taggedWord:
                                                sentObj.subject.pop(idx)
                                                sentObj.subject.append(newWord)
                                            idx += 1

                # Try to catch PRP$
                elif (taggedWord['tag'] == 'PRP$'):
                    #print("PRP$ caught")
                    
                    if len(sentSubjectQueue) > 0:
                        # Has it been mapped previously?
                        if len(mappedSubjectQueue) > 0:
                            # Do pronouns match?
                            index = 0
                            found = False
                            for mappedItem in mappedSubjectQueue:
                                #print("PRP$ mappedItem: ", mappedItem)
                                #print("PRP$ top mappedItem[0]: ", mappedItem[0])
                                if (mappedItem[2]["word"] == taggedWord["word"]) or mappedItem[2]["lemma"] == taggedWord["lemma"]:
                                    #print("PRP$ top mappedItem[3]:")
                                    #print(mappedItem[3])
                                    newWord = mappedItem[3]
                                    #print("PRP$ >>> REPLACE: ", taggedWord)
                                    #print("PRP$ >>> REPLACE WITH mappedItem: ", newWord)
                                    found = True
                                    idx = 0
                                    for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                        if sentSub == taggedWord:
                                            sentObj.subject.pop(idx)
                                            sentObj.subject.append(newWord)
                                        idx += 1
                                    trash = sentSubjectQueue.pop(index) # Eventhough we already mapped item, clean up sentSubjectQueue
                                index += 1
                            if not found:
                                # Queue hopefully is clean for a blind pop
                                popped = sentSubjectQueue.pop(0) # Blindly pop off the 1st in sent que
                                #print('PRP$ blind pop: ', popped)
                                newWord = popped[1]

                                gender = setGender(taggedWord, newWord)
                            
                                mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                                #print("PRP$ Added blind popped word to mappedSubjectQueue:")
                                #print(mappedSubjectQueue)
                                #print("PRP$ >>> REPLACE: ", taggedWord)
                                #print("PRP$ >>> REPLACE WITH queueItem: ", newWord)
                                idx = 0
                                for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                    if sentSub == taggedWord:
                                        sentObj.subject.pop(idx)
                                        sentObj.subject.append(newWord)
                                    idx += 1

                        else:
                            #for item in sentSubjectQueue:
                            #    print("PRP$ else - item: ", item)
                            
                            gender = setGender(taggedWord, newWord)
                            
                            mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                            #print("PRP$ Added popped word to mappedSubjectQueue:")
                            #print(mappedSubjectQueue)
                            #print("PRP$ >>> REPLACE: ", taggedWord)
                            #print("PRP$ >>> REPLACE WITH: ", newWord)
                            idx = 0
                            for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                if sentSub == taggedWord:
                                    sentObj.subject.pop(idx)
                                    sentObj.subject.append(newWord)
                                idx += 1
                    else:
                        # First check current paragraph queue
                        if len(paragraphSubjectQueue) > 0:
                            popped = paragraphSubjectQueue.pop(0) # Blind pop...
                            newWord = popped[1]

                            gender = setGender(taggedWord, newWord)
                            
                            mappedSubjectQueue.append((sentCount, gender, taggedWord, newWord))
                            #print("PRP$ Added popped word to mappedSubjectQueue:")
                            #print(mappedSubjectQueue)
                            #print("PRP$ >>> REPLACE: ", taggedWord)
                            #print("PRP$ >>> REPLACE WITH queueItem: ", newWord)
                            idx = 0
                            for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                if sentSub == taggedWord:
                                    sentObj.subject.pop(idx)
                                    sentObj.subject.append(newWord)
                                idx += 1
                        else:
                            # Check if was already mapped
                            if len(mappedSubjectQueue) > 0:
                                # Do pronouns match?
                                # But for PRP$ the word nor the lemma will match!!!!
                                for mappedItem in mappedSubjectQueue:
                                    #print("PRP$ mappedItem: ", mappedItem)
                                    #print("PRP$ bottom mappedItem[0]: ", mappedItem[0])
                                    #print("PRP$ bottom mappedItem[2]: ", mappedItem[2])
                                    
                                    #if (mappedItem[2]["word"] == taggedWord["word"]) or mappedItem[2]["lemma"] == taggedWord["lemma"]:
                                    if genderMatch(taggedWord['word'], mappedItem[2]['word']): 
                                        #print("PRP$ GM bottom mappedItem[3]:")
                                        #print(mappedItem[3])
                                        newWord = mappedItem[3]
                                        #print("PRP$ GM >>> REPLACE: ", taggedWord)
                                        #print("PRP$ GM >>> REPLACE WITH mappedItem: ", newWord)
                                        idx = 0
                                        for sentSub in sentObj.subject: # Repalce existing subject pronoun with noun
                                            if sentSub == taggedWord:
                                                sentObj.subject.pop(idx)
                                                sentObj.subject.append(newWord)
                                            idx += 1
                
                newSent.append(newWord)
            #print('..........')
            #print('newSent:')
            #print(newSent)
            #print('----------')
            sentObj.epistropheSent = newSent

            # Remove duplicate subjects
            tmpSubject = []
            for s in sentObj.subject:
                if s not in tmpSubject:
                    tmpSubject.append(s)

            
            epistropheSents.append(sentObj)

            #print('----------> Bottom')
            #print('sentObj.epistropheSent:')
            #print(sentObj.epistropheSent)
            #for w in sentObj.epistropheSent:
            #    print(w)
            #print('sentObj.subject:')
            #print(sentObj.subject)
            #print('sentSubjectQueue:')
            #print(sentSubjectQueue)
            #print('mappedSubjectQueue:')
            #print(mappedSubjectQueue)
            
        newCorpus = (bookName, epistropheSents)
        outputCorpora.append(newCorpus)

    #print('dumping outputCorpora to pickle...')
#    with open(pickleOutputFile, "wb") as f:
#        pickle.dump(outputCorpora, f)
#    f.close()
    
    #print('END: resolvePronouns...')
    return outputCorpora


def setNarratorName(taggedSent):
    # e.g. "I am Bob...", "my name is Mary...", etc.
    #print('start setNarratorName')
    #print('taggedSent: ', taggedSent)
    index = 0;
    for word in taggedSent:
        #print('word: ', word)
        if word['word'] == 'I':
            #print('Found I')
            #print("taggedSent[index + 1]['word']: ", taggedSent[index + 1]['word'])
            if taggedSent[index + 1]['word'] == 'am':
                #print('Found am')
                #print("taggedSent[index + 2]['tag']: ", taggedSent[index + 2]['tag'])
                if taggedSent[index + 2]['tag'] == 'NNP':
                    #print('Found NNP')
                    #print('Setting narratorName to: ')
                    #print(taggedSent[index + 2])
                    return taggedSent[index + 2]
        index += 1
                
    #print('end setNarratorName returning None')
    return None


def setGender(taggedWord, newWord):

    if taggedWord["word"] in male:
        return 'M'
    elif taggedWord["word"] in female:
        return 'F'

    return 'X'


def genderMatch(taggedWord, mappedItem):

    if (taggedWord in male) and (mappedItem in male):
        return True
    elif (taggedWord in female) and (mappedItem in female):
        return True

    return False


def findSVO(sentObj, method):
   
#    print('START: --- findSVO (per word) ---')
    #orgSentObj.printAll()
    #print('-----')

    processedSentence = []
    currentWordPosition = 0

    SUBJECT_DEPS = ["nsubj", "nsubjpass", "csubj", "agent", "expl"]
    OBJECT_DEPS = ["dobj", "dative", "attr", "oprd"]

    if method in ['s', 'S']:
#        print("...Using spaCy method...")
        for inputWord in sentObj.epistropheSent:
            # Per Spacy is this a subject?
            #
            if inputWord['tag'] in nnx or inputWord['tag'] in prpx:
                if (inputWord["dep"] in SUBJECT_DEPS) or (inputWord["hdep"] in SUBJECT_DEPS):
                    if inputWord not in sentObj.subject:
                        sentObj.subject.append(inputWord)
                    processedSentence.append(inputWord)
                    currentWordPosition += 1

                    #spacyProcessed.append(("Subject", inputWord))

                    continue

            # Per Spacy is this a object?
            #
            if inputWord['tag'] in nnx:
                if (inputWord["dep"] in OBJECT_DEPS) or (inputWord["hdep"] in OBJECT_DEPS):
                    if inputWord not in sentObj.object:
                        sentObj.object.append(inputWord)
                    processedSentence.append(inputWord)
                    currentWordPosition += 1

                    #spacyProcessed.append(("Object", inputWord))

                    continue

            # Grab the verbs
            #
            if inputWord["pos"] == "VERB":
                sentObj.verb.append(inputWord)
                processedSentence.append(inputWord)
                currentWordPosition += 1

                #spacyProcessed.append(("Verb", inputWord))

                continue

            #spacyNotProcessed.append(inputWord)

        
            currentWordPosition += 1
            processedSentence.append(inputWord)
    else:
        # Homemade...
#        print("...Using Homemade method...")
        
        for inputWord in sentObj.epistropheSent:
            tag = inputWord['tag']
            
            if tag in nnx:

                # Typically first noun is the subject...
                #
                if len(sentObj.subject) == 0:
                    sentObj.subject = []
                    sentObj.subject.append(inputWord)
                    currentWordPosition += 1
                    processedSentence.append(inputWord)

                    #homemadeProcessed.append(("nnx subject", inputWord))

                    continue # ???
            
                # Check for full name i.e. John Doe
                #print("sentObj.inputSent: ", sentObj.inputSent)
                #print("inputWord: ", inputWord)
                #print('processedSentence: ', processedSentence)
                #print('[-1]: ', processedSentence[-1])
                if processedSentence[-1]['tag'] == 'NNP':
                    # Where is it? Subject? object? or indirectObject?
                    # Using strict SVO:
                    if len(sentObj.verb) == 0:
                        sentObj.subject.append(inputWord)
                    else:
                        if len(sentObj.verb) == 0:
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
                if (len(sentObj.verb) > 0) and (len(sentObj.object) == 0):
                    sentObj.object = []
                    sentObj.object.append(inputWord)
                elif len(sentObj.verb) == 0:
                    sentObj.subject.append(inputWord)
                else:
                    # ?
                    if processedSentence[-1]['tag'] != 'NNP': # Check for John Doe?
                        sentObj.object.append(inputWord)

                #homemadeProcessed.append(("nnx Subject or Object", inputWord))        
                #print("END if tag in nnx") 
            
            elif tag in prpx:
                if (len(sentObj.verb) ==0) and (len(sentObj.subject) == 0):
                    sentObj.subject = []
                    sentObj.subject.append(inputWord)
                
                elif (len(sentObj.verb) == 0) and (len(sentObj.subject) > 0):
                    sentObj.subject.append(inputWord)
                
                elif (len(sentObj.verb) > 0) and (len(sentObj.object) == 0):

                    # Filter out: "He did his..."
                    if (len(sentObj.subject) > 0):
                        #print('sentObj.subject: ', sentObj.subject)
                        #print('len(sentObj.subject): ', len(sentObj.subject))
                        #print('sentObj.subject != None): ', sentObj.subject != None)
                        if sentObj.subject[0]['tag'] in prpx:
#                   print('prpx found in subject--is there a subject possesive match?')
                            if pronounMatch(sentObj.subject[0], inputWord):
#                               print('pronoun match!')
                                sentObj.subject.append(inputWord) # Just to record it
                            else:
#                               print('no pronoun match...')
                                # This my not be the best...~?
                                sentObj.object = []
                                sentObj.object.append(inputWord)
                
                elif (len(sentObj.verb) > 0) and (len(sentObj.object) > 0):
                                    
                    sentObj.object.append(inputWord) 
                    
                if sentObj.isVar('_PRPX'):
                    sentObj._PRPX.append(inputWord)
                else:
                    sentObj._PRPX = []
                    sentObj._PRPX.append(inputWord)

                #homemadeProcessed.append(("prpx", inputWord))
                    
            elif tag in vbx:
                if (len(sentObj.verb) == 0):
                    sentObj.verb = []
                sentObj.verb.append(inputWord)

                #homemadeProcessed.append(("vbx", inputWord))
            
            elif tag == 'WDT':
                if sentObj.isVar('_WDT'):
                    sentObj._WDT.append(inputWord)
                else:
                    sentObj._WDT = []
                    sentObj._WDT.append(inputWord)

                #homemadeProcessed.append(("WDT", inputWord))
                    
            elif tag == 'WP':
                if sentObj.isVar('_WP'):
                    sentObj._WP.append(inputWord)
                else:
                    sentObj._WP = []
                    sentObj._WP.append(inputWord)

                #homemadeProcessed.append(("WP", inputWord))
                    
            elif tag == 'WPS':
                if sentObj.isVar('_WPS'):
                    sentObj._WPS.append(inputWord)
                else:
                    sentObj._WPS = []
                    sentObj._WPS.append(inputWord)

                #homemadeProcessed.append(("WPS", inputWord))
            
            elif tag == 'WRB':
                if sentObj.isVar('_WRB'):
                    sentObj._WRB.append(inputWord)
                else:
                    sentObj._WRB = []
                    sentObj._WRB.append(inputWord)

                #homemadeProcessed.append(("WRB", inputWord))
            #else:
            #    print('ELSE: unknown tag? inputWord: ', inputWord)

        
            # Tracking what we have processed thus far--for look back checking
            currentWordPosition += 1
    
            processedSentence.append(inputWord)
        
#            
#        
#    if processedSentence[-1]['word'] == "?":
#        newSentObj.type = "interrogative"
#    elif processedSentence[-1]['word'] == "!":
#        if processedSentence[0]['tag'] in vbx: # Usally begins with a verb
#            sentObj.type = "imperative"
#        else:
#            sentObj.type = "exclamative"
#    else:
#        if processedSentence[0]['tag'] in vbx: # Usally begins with a verb
#            sentObj.type = "imperative"
#        else:
#            sentObj.type = "declarative"
#
#    #print("sentObj:")
#    #sentObj.printAll()
#    
#    print('END: --- findSVO ---')
    
    return sentObj



def processNNXs(inputWord, newSentObj, processedSentence, currentWordPosition):

    #print("START processNNXs...")
    #print('inputWord: ', inputWord)
    #print('newSentObj:')
    #newSentObj.printAll()
    #print('processedSentence: ', processedSentence)
    #print('currentWordPosition: ', currentWordPosition)
    
    if newSentObj.subject == None:
        newSentObj.subject = []
        newSentObj.subject.append(inputWord)
        currentWordPosition += 1
        processedSentence.append(inputWord)
        #print('newSentObj.subject == None')
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

    #print("END processNNXs...") 
    return newSentObj


def getSubjectWords(sent):
    # Return a list of just the subject(s) words (no tags)
    subWords = []
    subs = sent.subject

    if subs != None:
        for s in subs:
            subWords.append(s['word'])

    return subWords


def getObjectWords(sent):
    # Return a list of just the subject(s) words (no tags)
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
            #print('sentence #: ', tmpCnt)
            #print('s (.inputSent) in bookText (findSVOs):')
            #print(s.inputSent)
            #print('.....')
            # method: s = spacy
            method = 'x'
            svoObj = findSVO(s, method)
            #print('after findSVO:')
            #svoObj.printAll()
            #print('...............')
            objArr.append(svoObj)
            
        newCorpora.append((bookName, objArr))

    return newCorpora


def processCorpus(corpus):

    # Resolve pronouns--Much work needed!
    resolvedCorpus = resolvePronouns(corpus)

    # Find Subject-Verb-Objects
    processedCorpusSVO = findSVOs(resolvedCorpus)


    return processedCorpusSVO




#
#
#
if __name__ == "__main__":

    print("START: processSVOs...")

    spacyProcessed = []
    spacyNotProcessed = []
    homemadeProcessed = []
    homemadeNotProcesed = []

    corpus = loadPickleData()

    # Resolve pronouns--Much work needed!
    #resolvedCorpora = resolvePronouns(corpus)
    """
    print(len(resolvedCorpora))
    print(type(resolvedCorpora))

    for c in resolvedCorpora:
        cnt = 0
        print("Book Name: ", c[0])
        for s in c[1]:
            cnt += 1
            print('--- {} ---'.format(cnt))
            s.printAll()
    """
    # Find Subject-Verb-Objects
    #processedCorporaSVO = findSVOs(resolvedCorpora)
    """
    print(len(processedCorporaSVO))
    print(type(processedCorporaSVO))

    for c in processedCorporaSVO:
        cnt = 0
        print("Book Name: ", c[0])
        for s in c[1]:
            cnt += 1
            print('--- {} ---'.format(cnt))
            s.printAll()
    """
    pCorpusSVO = processCorpus(corpus)

    print(len(pCorpusSVO))
    print(type(pCorpusSVO))

    for c in pCorpusSVO:
        cnt = 0
        print("Book Name: ", c[0])
        """
        for s in c[1]:
            cnt += 1
            print('--- {} ---'.format(cnt))
            s.printAll()
        """



#    print('------------------ spacy processed')
#    for i in spacyProcessed:
#        print(i)
#
#    print('------------------ spacy not processed')
#    for i in spacyNotProcessed:
#        print(i)

    #print('------------------ homemade')
    #for i in homemadeProcessed:
    #    print(i)

    
    # Save processedCorporaSVO
    #with open(pickleFileOut, "wb") as f:
    #    pickle.dump(processedCorporaSVO, f)
    #f.close()
    

    print("END: processSVOs.")
