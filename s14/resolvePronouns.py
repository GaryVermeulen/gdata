#
# resolvePronouns.py
#
#

import pickle

from commonConfig import subjectPronouns, objectPronouns, possivePronouns, reflexivePronouns
from commonConfig import demonstrativePronouns, interrogativePronouns, indefinitePronouns, relativePronouns


def loadProcessedCorpora():

    pickleFile = 'data/processedCorpora.p'

    with open(pickleFile, "rb") as f:
        processedCorpora = pickle.load(f)

    return processedCorpora


def resolvePronouns(processedCorpora):
    # Return a mapping of nouns to pronouns
    print('START: resolvePronouns...')
    paragraphNounQueueMax = 5
    mappedPronouns = []

    for corpus in processedCorpora:
        print(type(processedCorpora))
        print(len(processedCorpora))
        print(corpus)

        bookName = corpus[0]
        paragraphNounQueue = []
        bookSentCnt = 0
        
        print(bookName)

        for sentObj in corpus[1]:
            bookSentCnt += 1
            sentNounQueue = []
            orgSent = sentObj.inputSent
            print('{} *** orgSent:'.format(bookSentCnt))
            print(orgSent)
            for taggedSent in sentObj.taggedSent:
                #print(taggedSent)
                if taggedSent['word'] == '.': # End of sentence -- e.g. Two sentences between quoutes
                    for n in sentNounQueue:
                        if n not in paragraphNounQueue:
                            paragraphNounQueue.append(n)
                    sentNounQueue = []

                    if len(paragraphNounQueue) > paragraphNounQueueMax:
                        numToPop = range(len(paragraphNounQueue) - paragraphNounQueueMax)
                        for i in numToPop:
                            paragraphNounQueue.pop(0)
                        #print('  pNQ shorten: ', paragraphNounQueue)
                    
                if taggedSent['pos'] in ['NOUN', 'PROPN']:
                    # Don't add to quue if already mapped
                    if len(mappedPronouns) > 0:
                        for mP in mappedPronouns:
                            if mP[0][0] != taggedSent['word']:
                                sentNounQueue.append((taggedSent['word'], taggedSent['pos'], taggedSent['tag']))
                    else:
                        sentNounQueue.append((taggedSent['word'], taggedSent['pos'], taggedSent['tag']))
                    
                #if len(sentNounQueue) > 0:
                #    print(' sentNounQueue: ', sentNounQueue)
                    
                alreadyMapped = False
                if taggedSent['pos'] == 'PRON':
                    # Has Pronoun already been mapped?
                    if len(mappedPronouns) > 0:
                        for m in mappedPronouns:
                            if m[1][0].lower() == taggedSent['word'].lower():
                                print('Already mapped: ', m)
                                alreadyMapped = True
                                
                    if not alreadyMapped:
                        # Simple mapping to last noun--this just a start...
                        # First check sentNounQueue
                        if len(sentNounQueue) > 0:
                            # Is the pronoun to a NNP or object/NN?
                            idx = 0
                            for n in sentNounQueue:
                                if n[2] == 'NNP':
                                    if taggedSent['word'] in subjectPronouns:
                                        nounMatch = sentNounQueue.pop(idx)
                                        print("Noun: {} => Pronoun: {}".format(nounMatch, taggedSent['word']))
                                        mappedPronouns.append((nounMatch, (taggedSent['word'], taggedSent['pos'], taggedSent['tag'])))
                                idx += 1
                        else:
                            # Check paragraphNounQueue
                            if len(paragraphNounQueue) > 0:
                                idx = 0
                                for n in paragraphNounQueue:
                                    if n[2] == 'NNP':
                                        if taggedSent['word'] in subjectPronouns:
                                            nounMatch = paragraphNounQueue.pop(idx)
                                            print("Noun: {} => Pronoun: {}".format(nounMatch, taggedSent['word']))
                                            mappedPronouns.append((nounMatch, (taggedSent['word'], taggedSent['pos'], taggedSent['tag'])))
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
                            
            print('-----')        
            #sentObj.printAll()  ## 'pos': 'PRON'
    
    print('END: resolvePronouns...')
    return mappedPronouns

#
#
#
if __name__ == "__main__":

    print('Start:  resolvePronouns (__main__)')

    processedCorpora = loadProcessedCorpora()

    print(type(processedCorpora))
    print(len(processedCorpora))

    mappedPronouns = resolvePronouns(processedCorpora)

    for mp in mappedPronouns:
        print(mp)
    
    
    print('End: resolvePronouns (__main__)')  
