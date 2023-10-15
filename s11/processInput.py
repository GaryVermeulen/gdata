#
# processInput.py
#

import sys
import spacy
import pickle

from commonUtils import connectMongo
from commonUtils import chkTagging
from commonUtils import getInflectionTag
from commonUtils import getInflections
from commonUtils import expandSent

#from commonConfig import commandWords


from simpSA import sentAnalysis
from simpSA2 import sentAnalysis2
from kbChecker import chkKB
from processOutput import prattle

nlp = spacy.load("en_core_web_lg") # lg has best accuracy
#nlp = spacy.load("en_core_web_sm") # 


def sentenceAnalysis(tagged_uI):

    print('------ start sentenceAnalysis ------')

    sA_Obj, error = sentAnalysis(tagged_uI)

    if len(error) > 0:
        print('*** sentAnalysis returned possible errors:')
        for e in error:
            print(e)

    print('------ end sentenceAnalysis ------')

    return sA_Obj, error

def kbCommand(nnxKB):

    nodeKey = input('Enter KB Node (key/name) to display: ')

    node = nnxKB.find({"_id":nodeKey})

    if node == None:
        print('Could not find a node named: ', nodeKey)
    else:
        print(node)
        for item in node:
            print(item)
    
    chkKB_Results = chk_nnxKB(nodeKey, nnxKB)
    if len(chkKB_Results) > 0:
        print('-' * 5)
        print(chkKB_Results)
        print(chkKB_Results["_id"])
        print(chkKB_Results["similar"])
        print(chkKB_Results["tag"])
        print(chkKB_Results["isAlive"])
        print(chkKB_Results["canDo"])
        print(chkKB_Results["superclass"])
    
    return


def preprocessInput(mismatch, multiple, unknown, sA_Obj, kb_Obj):

    print('---   Start preprocessInput   ---')
    # Process tagging issues
    if len(mismatch) > 0:
        print('Tagging issue -- mismatch: ', mismatch)
    else:
        print('No missmatched tags')

    if len(multiple) > 0:
        print('Tagging issue -- multiple: ', multiple)
    else:
        print('No multiple tags found')

    if len(unknown) > 0:
        print('Tagging issue -- unknown: ', unknown)
    else:
        print('No unknown tags')

#    results = processTaggingIssues(mismatch, multiple, unknown, sA_Obj)
#
#    print('processTaggingIssues; returned: ', results)

    # Attempt to distill something meaningful from what we have
    print('-' * 10)
    print('Sentence Object:')
    sA_Obj.printAll()

    print('-' * 10)
    print('KB object')
    kb_Obj.printAll()

    # Do we know (in KB) about all the subjects?
    
    print('---   End preprocessInput   ---')

    return 'preprocessInput output'


def processTaggingIssues(mismatch, multiple, unknown, sA_Obj):

    if len(mismatch) > 0:
        print('Tagging issue -- mismatch: ', mismatch)
    


    return 'processTaggingIssues results'


def processUserInput():

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    untaggedCorpus = simpDB["untaggedCorpus"]
    
    while True:
        print('-' * 10)
        uI = input('Please enter a sentence or enter <kb>: ')
        print(uI)

        if uI == '':
            print('-' * 10)
            res = input('Retain conversation <Y/n>? ')
            if res in ['Y', 'y', 'Yes', 'yes']:
                print('Conversation kept.')
            else:
                conversation = simpDB["conversation"]
                conversation.drop()
                print('Conversation dropped.')

            sys.exit('Exiting; Nothing entered.')

        if uI == 'kb':
            kbCommand(nnxKB)
            continue

        print('-' * 10)
        print('Preprocess user input...')

        eUI_List = expandSent(uI)
        eUI_Str = ' '.join(eUI_List)

        print('eUI_Str: ', eUI_Str)

        print('-' * 10)

        doc = nlp(eUI_Str)

        taggedInput = []
        for token in doc:
            tmpToken = ((str(token.text)), (str(token.tag_)))
            taggedInput.append(tmpToken)

        print('Spacy tagged input:')
        print(taggedInput)

        # Check tagged uI aginst taggedBoW for conflicts
        print('-' * 10)
        print('Checking tags...')

        mismatch, multiple, unknown = chkTagging(taggedInput, tagged_BoW)

        print('chkTagging results:')
        print('Mismatch: ', mismatch)
        print('Multiple: ', multiple)
        print('Unknown: ', unknown)

        if len(unknown) > 0:
            unkWords = []
            for u in unknown:
                unkWords.append(u[0])

        # Original sentence analysis
        print('-' * 10)
        print('Checking basic sentence analysis')
        sA_Obj, error = sentenceAnalysis(taggedInput)    
        sA_Obj.printAll()
        if len(error) > 0:
            print('Sentence analysis returned an error:')
            for e in error:
                print(e)

            print('Ignoring input sentence')
            continue

        # New sentence analysis
        print('-' * 10)
        print('New sentence analysis')
        newSA_Obj, error2 = sentAnalysis2(taggedInput)    
        newSA_Obj.printAll()
        if len(error2) > 0:
            print('New sentence analysis returned an error:')
            for e in error2:
                print(e)

            print('Ignoring input sentence')
            continue

        # save sA_Obj pickle for debug and testing
        #print('-' * 10)
        #print('Saving sentence analysis object:')
        #f = open('pickles/sA_Obj.pkl', 'wb')
        #pickle.dump(sA_Obj, f)
        #f.close()
        #print('Aunt Bee saved sA_Obj.pkl')

        # Check KB anainst Simp, subject(s), verb(s)... (was simpGA.py)
        print('-' * 10)
        kb_Obj = chkKB(sA_Obj, nnxKB, untaggedCorpus)

        kb_Obj.tagMismatch = mismatch
        kb_Obj.tagMultiple = multiple
        kb_Obj.tagUnknown = unknown

        print('kb_Obj: ')
        kb_Obj.printAll()

        """
        print('-' * 10)
        ppResults = preprocessInput(mismatch, multiple, unknown, sA_Obj, kb_Obj)

        print('Results from preprocessInput:')
        print(ppResults)
        """
        # Respond with appropiate output
        print('-' * 10)
        print('SKIPPING: prattle (from processInput.py)...')
#        print('parttle retunred: ')
#        print(outSent)


        

    return 'Exit.'


#
#
if __name__ == "__main__":

    print('Processing processInput (__main__)...')

    processUserInput()

