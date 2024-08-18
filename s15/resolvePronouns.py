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


def loadProcessedCorpora():

    pickleFile = 'data/processedCorpora.p'

    with open(pickleFile, "rb") as f:
        processedCorpora = pickle.load(f)

    return processedCorpora


def resolvePronouns(bookSents):
    # Return a mapping of nouns to pronouns
    print('START: resolvePronouns...')
    paragraphNounQueueMax = 5
    mappedPronouns = []
    bookSentCnt = 0
    paragraphNounQueue = []
    epistropheSents = []

    for sentObj in bookSents:
        bookSentCnt += 1
        sentNounQueue = []
        orgSent = sentObj.inputSent
        newSent = []
        print('{} *** orgSent:'.format(bookSentCnt))
        print(orgSent)
        print(sentObj.taggedSentShort)
        print('-----')
        for taggedWord in sentObj.taggedSentShort:
            print('tagged word:')
            print(taggedWord)

            newWord = (taggedWord['word'], taggedWord['tag'])
                
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
                        paragraphNounQueue.pop(0)
                    #print('  pNQ shorten: ', paragraphNounQueue)
                        
            # Noun found, place in sentence queue
            if taggedWord['pos'] in ['NOUN', 'PROPN']:
                # Don't add to queue if already mapped
                if len(mappedPronouns) > 0:
                    for mP in mappedPronouns:
                        if mP[0][0] != taggedWord['word']:
                            sentNounQueue.append((taggedWord['word'], taggedWord['pos'], taggedWord['tag']))
                else:
                    sentNounQueue.append((taggedWord['word'], taggedWord['pos'], taggedWord['tag']))
                    
            #if len(sentNounQueue) > 0:
            #    print(' sentNounQueue: ', sentNounQueue)

            # Pronoun found, now comes the fun
            alreadyMapped = False
            if taggedWord['pos'] == 'PRON':
                # Excluding these pronouns--for now
                if taggedWord['word'] not in ['I', 'Me', 'me', 'Mine', 'mine', 'Myself', 'myself', 'You', 'you', 'Yours', 'yours', 'Yourself', 'yourself']:
                    # Has Pronoun already been mapped?
                    if len(mappedPronouns) > 0:
                        for m in mappedPronouns:
                            if m[1][0].lower() == taggedWord['word'].lower():
                                print('Already mapped: ', m)
                                alreadyMapped = True
                                
                    if not alreadyMapped:
                        # Simple mapping to last noun--this is just a start...
                        # First check sentNounQueue
                        if len(sentNounQueue) > 0:
                            # Is the noun a NNP or object/NN?
                            idx = 0
                            for n in sentNounQueue:
                                if n[2] == 'NNP':
                                    if taggedWord['word'] in subjectPronouns:
                                        nounMatch = sentNounQueue.pop(idx)
                                        print("Noun: {} => Pronoun: {}".format(nounMatch, taggedWord['word']))
                                        mappedPronouns.append((nounMatch, (taggedWord['word'], taggedWord['pos'], taggedWord['tag'])))
                                        newWord = nounMatch
                                idx += 1
                        else:
                            # Check paragraphNounQueue
                            if len(paragraphNounQueue) > 0:
                                idx = 0
                                for n in paragraphNounQueue:
                                    if n[2] == 'NNP':
                                        if taggedWord['word'] in subjectPronouns:
                                            nounMatch = paragraphNounQueue.pop(idx)
                                            print("Noun: {} => Pronoun: {}".format(nounMatch, taggedWord['word']))
                                            mappedPronouns.append((nounMatch, (taggedWord['word'], taggedWord['pos'], taggedWord['tag'])))
                                            newWord = nounMatch
                                    idx += 1
                        alreadyMapped = False

            #print('  pNQ: ', paragraphNounQueue)
            # Clean out pNQ if already mapped
                
            if len(mappedPronouns) > 0:
                
                for mP in mappedPronouns:
                    #print(mP)
                    if mP[0] in paragraphNounQueue:
                        removeMe = mP[0]
                        tmpLst = []
                        for i in paragraphNounQueue:
                            if removeMe != i:
                                tmpLst.append(i)
                        paragraphNounQueue = tmpLst.copy()
                #print(mappedPronouns)

            newSent.append(newWord)                
        print('..........')
        print('newSent:')
        print(newSent)
        print('----------')
        #sentObj.printAll()  ## 'pos': 'PRON'
    
    print('END: resolvePronouns...')
    return mappedPronouns


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

        

                


    print('END: resolvePronounsV2')
    return newBookSents

#
#
#
if __name__ == "__main__":

    print('Start:  resolvePronouns (__main__)')
    print('use via import...')

#    processedCorpora = loadProcessedCorpora()
#
#    print(type(processedCorpora))
#    print(len(processedCorpora))
#
#    mappedPronouns = resolvePronouns(processedCorpora)
#
#    for mp in mappedPronouns:
#        print(mp)
    
    
    print('End: resolvePronouns (__main__)')  
