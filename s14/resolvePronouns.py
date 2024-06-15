#
# resolvePronouns.py
#
#

import pickle




def loadProcessedCorpora():

    pickleFile = 'data/processedCorpora.p'

    with open(pickleFile, "rb") as f:
        processedCorpora = pickle.load(f)

    return processedCorpora


def resolvePronouns(processedCorpora):
    # Return a mapping of nouns to pronouns
    print('START: resolvePronouns...')
    nounQueueMax = 5
    mappedPronouns = []

    for corpus in processedCorpora:
        print(type(processedCorpora))
        print(len(processedCorpora))
        print(corpus)

        bookName = corpus[0]
        nounQueue = []
        
        print(bookName)

        for sentObj in corpus[1]:
            sentNounQueue = []
            orgSent = sentObj.inputSent
            print('orgSent:')
            print(orgSent)
            for taggedSent in sentObj.taggedSent:
                print(taggedSent)
                if taggedSent['pos'] in ['NOUN', 'PROPN']:
                    sentNounQueue.append(taggedSent['word'])
                    if len(nounQueue) < nounQueueMax:
                        nounQueue.append(taggedSent['word'])
                    else:
                        nounQueue.pop()
                        nounQueue.append(taggedSent['word'])
                print(nounQueue)
                print(sentNounQueue)
                if taggedSent['pos'] == 'PRON':
                    print(taggedSent['word'])
                    # Simple mapping to last noun--this just a start...
                    if taggedSent['word'] in ['he', 'she', 'it', 'they']:
                        if len(sentNounQueue) > 0:
                            print("Noun: {} => Pronoun: {}".format(sentNounQueue.pop(), taggedSent['word']))
                    
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

    notSure = resolvePronouns(processedCorpora)

    print(notSure)
    
    
    print('End: resolvePronouns (__main__)')  
