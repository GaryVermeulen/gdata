#
# resolvePronouns.py
# Simple pronoun to noun matcher/resolver.
#
#

import pickle

# Pronoun groupings--too board and there are cross-overs
from commonConfig import subjectPronouns #, objectPronouns, possivePronouns, reflexivePronouns
#from commonConfig import demonstrativePronouns, interrogativePronouns, indefinitePronouns, relativePronouns
from commonConfig import nnx

pickleOutputFile = 'pickleJar/resolvedPronuons.p'


def loadProcessedCorpora():

    pickleFile = 'pickleJar/processedCorpora.p'

    with open(pickleFile, "rb") as f:
        processedCorpora = pickle.load(f)

    return processedCorpora


#def resolvePronouns(bookSents):
def resolvePronouns(processedCorpora):
    # Return a mapping of nouns to pronouns
    print('START: resolvePronouns...')
    

    outputCorpora = []

    for corpus in processedCorpora:

        paragraphNounQueueMax = 5
        mappedPronouns = []
    
        paragraphNounQueue = []
        epistropheSents = []

        bookName = corpus[0]
        bookSents = corpus[1]

        print('----------------------------')
        print('bookName: ', bookName)
        print('----------------------------')

        sentCount = 0
        for sentObj in bookSents:
            sentCount += 1
            sentSubjectQueue = []
            orgSent = sentObj.inputSent
            newSent = []
            #print('{} *** orgSent:'.format(bookSentCnt))
            #print(orgSent)
            #print(sentObj.taggedSentShort)
            #print('-----')
            #for taggedWord in sentObj.taggedSentShort:

            print('-----Top: ', sentCount)
            print('taggedSentLong:')
            #print(sentObj.taggedSentLong)
            for w in sentObj.taggedSentLong:
                print(w)
            print('mappedPronouns:')
            print(mappedPronouns)
            print('paragraphNounQueue:')
            print(paragraphNounQueue)

            for taggedWord in sentObj.taggedSentLong:
                #print('*** tagged word:')
                #print(taggedWord)

                #newWord = (taggedWord['word'], taggedWord['tag'])
                newWord = taggedWord
                oldWord = taggedWord

                # Collect Spacy 'dep': 'tag': 'NNP',...,'nsubj',..., 'dep_exp': 'nominal subject'
                if (taggedWord['tag'] == 'NNP') and (taggedWord['dep'] == 'nsubj'):
                    currentSent_nsubj = taggedWord
                    sentSubjectQueue.append(taggedWord)
                    
                # Pronoun found--can we replace it?
                if (taggedWord['tag'] == PRP) and (taggedWord['dep'] == 'nsubj'):
                    if len(sentSubjectQueue) > 0:
                        newWord = sentSubjectQueue.pop(0) # Blindly pop off the 1st in sent que
                        mappedSubjectQueue.append(newWord)


                """
                # End of sentence -- e.g. Two sentences were processed as one, so
                # move sentence queue items to paragraph queue if not already
                # in paragraph queue
                if taggedWord['word'] == '.': 
                    for n in sentNounQueue:
                        if n not in paragraphNounQueue:
                            paragraphNounQueue.append(n)
                    sentNounQueue = []

                    if len(paragraphNounQueue) > paragraphNounQueueMax:
                        numToPop = range(len(paragraphNounQueue) - paragraphNounQueueMax)
                        for i in numToPop:
                            tmpPopped = paragraphNounQueue.pop(0)
                            #print('  popped {} from paragraphNounQueue: {}'.format(tmpPopped, paragraphNounQueue))
                        
                # Noun found, place in sentence queue
                if taggedWord['pos'] in ['NOUN', 'PROPN']:
                    # Don't add to queue if already mapped
                    if len(mappedPronouns) > 0:
                        for mP in mappedPronouns:
                            #if mP[0][0] != taggedWord['word']:
                            if mP['word'] != taggedWord['word']:
                                #sentNounQueue.append((taggedWord['word'], taggedWord['pos'], taggedWord['tag']))
                                #sentNounQueue.append((taggedWord['word'], taggedWord['tag']))
                                sentNounQueue.append(taggedWord)
                    else:
                        #sentNounQueue.append((taggedWord['word'], taggedWord['pos'], taggedWord['tag']))
                        #sentNounQueue.append((taggedWord['word'], taggedWord['tag']))
                        sentNounQueue.append(taggedWord)
                    
                #if len(sentNounQueue) > 0:
                #    print(' sentNounQueue: ', sentNounQueue)

                #if len(paragraphNounQueue) > 0:
                #    print(' paragraphNounQueue: ', paragraphNounQueue)

                #if len(mappedPronouns) > 0:
                #    print(' mappedPronouns: ', mappedPronouns)

                # Pronoun found, now comes the fun
                alreadyMapped = False
                if taggedWord['pos'] == 'PRON':
                    #print('taggedWord: ', taggedWord)
                    # Excluding these pronouns--for now
                    if taggedWord['word'] not in ['I', 'Me', 'me', 'Mine', 'mine', 'Myself', 'myself', 'You', 'you', 'Yours', 'yours', 'Yourself', 'yourself']:
                        # Has Pronoun already been mapped?
                        if len(mappedPronouns) > 0:
                            for m in mappedPronouns:
                                #if m[1][0].lower() == taggedWord['word'].lower():
                                print('m:')
                                print(m)
                                print('taggedWord:')
                                print(taggedWord)
                                if m['word'].lower() == taggedWord['word'].lower():
                                    #print('Already mapped: ', m)
                                    alreadyMapped = True
                                    # Let's try blindly re-mapping to new pronoun...~?
                                    #newWord = (m)
                                    #newWord = (m[0])
                                    newWord = m

                                    # Drop-through, continue, break????
                                
                        if not alreadyMapped:
                            #print('if not alreadyMapped...')
                            # Simple mapping to last noun--this is just a start...
                            # First check sentNounQueue
                            if len(sentNounQueue) > 0:
                                #print('if not alreadyMapped => if len sentNounQueue')
                                # Is the noun a NNP or object/NN?
                                idx = 0
                                for n in sentNounQueue:
                                    #if n[1] == 'NNP':
                                    if n['tag'] == 'NNP':
                                        if taggedWord['word'] in subjectPronouns:
                                            nounMatch = sentNounQueue.pop(idx)
                                            #print("Noun: {} => Pronoun: {}".format(nounMatch, taggedWord['word']))
                                            #mappedPronouns.append((nounMatch, (taggedWord['word'], taggedWord['pos'], taggedWord['tag'])))
                                            mappedPronouns.append(nounMatch)
                                            newWord = nounMatch
                                            #print('newWord if: ', newWord)
                                    idx += 1
                            else:
                                #print('if not alreadyMapped => else len sentNounQueue')
                                # Check paragraphNounQueue
                                if len(paragraphNounQueue) > 0:
                                    #print('...len paragraphNouneQueue...')
                                    idx = 0
                                    for n in paragraphNounQueue:
                                        #if n[1] == 'NNP':
                                        if n['tag'] == 'NNP':
                                            if taggedWord['word'] in subjectPronouns:
                                                nounMatch = paragraphNounQueue.pop(idx)
                                                #print("Noun: {} => Pronoun: {}".format(nounMatch, taggedWord['word']))
                                                mappedPronouns.append(nounMatch)
                                                newWord = nounMatch
                                                #print('newWord else: ', newWord)
                                        idx += 1
                            alreadyMapped = False
                        #else:
                            # Already mapped and has need used once, but may be needed again...~?
        
                #print('  pNQ: ', paragraphNounQueue)
                # Clean out pNQ if already mapped
                
                if len(mappedPronouns) > 0:
                
                    for mP in mappedPronouns:
                        #print(mP)
                        if mP in paragraphNounQueue:
                            removeMe = mP
                            tmpLst = []
                            for i in paragraphNounQueue:
                                if removeMe != i:
                                    tmpLst.append(i)
                            paragraphNounQueue = tmpLst.copy()
                    #print(mappedPronouns)

                # If oldWord in subject repalce with newWord
                if oldWord != newWord:
                    if oldWord in sentObj.subject:
                        #print('Replace {} with {}'.format(oldWord, newWord))
                        #print(sentObj.subject)
                        for i in range(len(sentObj.subject)):
                            if sentObj.subject[i] == oldWord:
                                sentObj.subject[i] = newWord
                        #print(sentObj.subject)

                """
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

            print('-----Bottom')
            print('sentObj.epistropheSent:')
            print(sentObj.epistropheSent)
            print('sentObj.subject:')
            print(sentObj.subject)
            print('sentNounQueue:')
            print(sentNounQueue)
            print('mappedPronouns:')
            print(mappedPronouns)
            print('paragraphNounQueue:')
            print(paragraphNounQueue)

        newCorpus = (bookName, epistropheSents)
        outputCorpora.append(newCorpus)

    print('dumping outputCorpora to pickle...')
    with open(pickleOutputFile, "wb") as f:
        pickle.dump(outputCorpora, f)
    f.close()
    
    print('END: resolvePronouns...')
    return outputCorpora

"""
def resolvePronounsV2(bookSents):

    nouns = []

    newBookSents = []
    
    bookSentCnt = 0
    
    print('START: resolvePronounsV2')

    print(bookSents)

    for sent in bookSents:
        newSent = []
        bookSentCnt += 1
        print('{} *** orgSent:'.format(bookSentCnt))
        print(sent.inputSent)
        
        print('-----')

        for word in sent.taggedSentShort:
            newWord = {}
            print(word)

            if word['pos'] == 'PRON':
                print('pos = PRON: ', word)

                if word['word'] not in ['I', 'Me', 'me', 'Mine', 'mine', 'Myself', 'myself']:

                    if len(nouns) > 0:
                        #newWord = nouns.pop()
                        #newWord = nouns[0]
                        newWord = nouns[-1]
                        print('Replace with: ', newWord)
                    

                    
            if word['tag'] == 'NNP': # watch out for dupicates
                print('tag == NNP: ', word)
                
                nouns.append(word)

                # Remove duplicates
                tmpList = []
                for i in range(len(nouns)):
                    if nouns[i] not in nouns[i + 1:]:
                        tmpList.append(nouns[i])
                nouns = []
                nouns = tmpList.copy()

            print("De-dupped NOUNS: ")
            print(nouns)

            if len(newWord) > 0:
                newSent.append(newWord)
            else:
                newSent.append(word)

        print('newSent: ', newSent)
        newBookSents.append(newSent)

        
    print('dumping newBookSents to pickle...')
    with open(pickleOutputFile, "wb") as f:
        pickle.dump(newBookSents, f)
    f.close()
                

    print('END: resolvePronounsV2')
    return newBookSents
"""
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
