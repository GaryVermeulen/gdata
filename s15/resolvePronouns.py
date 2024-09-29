#
# resolvePronouns.py
# Simple pronoun to noun (NNP) matcher/resolver.
#
#

import pickle

# Pronoun groupings--too board and there are cross-overs
#from commonConfig import subjectPronouns #, objectPronouns, possivePronouns, reflexivePronouns
#from commonConfig import demonstrativePronouns, interrogativePronouns, indefinitePronouns, relativePronouns
from commonConfig import nnx
from commonConfig import male, female 

pickleOutputFile = 'pickleJar/resolvedPronuons.p' # For standalone runs to debug


# For standalone run to debug
def loadProcessedCorpora():

    pickleFile = 'pickleJar/taggedCorpora.p'

    with open(pickleFile, "rb") as f:
        processedCorpora = pickle.load(f)

    return processedCorpora


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


#def resolvePronouns(bookSents):
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
    with open(pickleOutputFile, "wb") as f:
        pickle.dump(outputCorpora, f)
    f.close()
    
    #print('END: resolvePronouns...')
    return outputCorpora

#
#
#
if __name__ == "__main__":

    print('Start:  resolvePronouns (__main__)')
    print('use via import...')

    processedCorpora = loadProcessedCorpora()
#
    print(type(processedCorpora))
    print(len(processedCorpora))
#
    mappedPronouns = resolvePronouns(processedCorpora)
#
    """
    for mp in mappedPronouns:
        print(mp)
        print('bookName: ', mp[0])
        sentCount = 0
        for s in mp[1]:
            sentCount += 1
            print(sentCount)
            s.printAll()
            print('-----')
    """
    
    print('End: resolvePronouns (__main__)')  
