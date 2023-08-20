#
# processInput.py
#

import sys
import spacy
import pickle

from commonUtils import connectMongo
from commonUtils import chkTagging
from commonUtils import chk_nnxKB
from commonUtils import chkCorpus
from commonConfig import simp
from commonConfig import kbResults

from simpSA import sentAnalysis
#from simpGA import chkGrammar # evolved into kbChecker
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

    return sA_Obj

def kbCommand(nnxKB):

    nodeKey = input('Enter KB Node (key/name) to display: ')

    node = nnxKB.find({"_id":nodeKey})

    if node == None:
        print('Could not find a node named: ', nodeKey)
    else:
        print(node)
        for item in node:
            print(item)
    
    chkKB = chk_nnxKB(nodeKey, nnxKB)
    if len(chkKB) > 0:
        print('-' * 5)
        print(chkKB)
        print(chkKB["_id"])
        print(chkKB["similar"])
        print(chkKB["tag"])
        print(chkKB["canDo"])
        print(chkKB["superclass"])
    
    return


def preprocessInput(mismatch, multiple, unknown, sA_Obj, simpKB, subjectCorpus, kbResults):

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

    # Attempt to distill something meaningful from what we have
    print('-' * 10)
    print('Sentence Object:')
    sA_Obj.printAll()

    print('-' * 10)
    print('KB restults object')
    kbResults.printAll()

    # Do we know (in KB) about all the subjects?
    
    print('---   End preprocessInput   ---')

    return 'preprocessInput output'


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
            sys.exit('Nothing entered.')

        if uI == 'kb':
            kbCommand(nnxKB)
            continue

        print('-' * 10)

        doc = nlp(uI)

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

#        print('unkWords: ', unkWords)

        # Basic sentence analysis
        print('-' * 10)
        print('Checking basic sentence analysis')
        sA_Obj = sentenceAnalysis(taggedInput)    
        sA_Obj.printAll()

        # save sA_Obj pickle for debug and testing
        print('-' * 10)
        print('Saving sentence analysis object:')
        f = open('pickles/sA_Obj.pkl', 'wb')
        pickle.dump(sA_Obj, f)
        f.close()
        print('Aunt Bee saved sA_Obj.pkl')

        # KB check
        print('-' * 10)
        # Retrieve Simp KB
        simpKB = chk_nnxKB(simp, nnxKB)
        print('-' * 5)
        print(simpKB)
#        print(simpKB["_id"])
#        print(simpKB["similar"])
#        print(simpKB["tag"])
#        print(simpKB["canDo"])
#        print(simpKB["superclass"])
        
        print('-' * 10)
        # Subject(s) KB check--are the subjects in the KB?
        subjectsInKB = []
        subjectsNotInKB = []
        
        if len(sA_Obj.sSubj) == 0:
            print('Something is wrong: No subject returned.')
        else:
            print('Checking KB for subject(s):', sA_Obj.sSubj)

            if isinstance(sA_Obj.sSubj, tuple):     # Just one subkect
                print('Processing single subject.')
                subjectKB = chk_nnxKB(sA_Obj.sSubj[0], nnxKB)
                print('subjectKB: ', subjectKB)

                if len(subjectKB) > 0:
                    subjectsInKB.append(subjectKB)
                else:
                    subjectsNotInKB.append(sA_Obj.sSubj[0])
            
            elif isinstance(sA_Obj.sSubj, list):    # multiple subjects
                print('Processing multiple subjects.')
                for sub in sA_Obj.sSubj:
                    subjectKB = chk_nnxKB(sub[0], nnxKB)
                    print('subjectKB: ', subjectKB)

                    if len(subjectKB) > 0:
                        subjectsInKB.append(subjectKB)
                    else:
                        subjectsNotInKB.append(sub[0])
    
            else:
                print('Unexpected subject type encountered: ', sA_Obj.sSubj[0])

        print('subjectsInKB: ', subjectsInKB)
        print('subjectsNotInKB: ', subjectsNotInKB)

        kb_Obj = kbResults(sA_Obj.inSent, subjectsInKB, subjectsNotInKB, False, [], [])

        # Check corpus for subject
        print('-' * 10)
        print('Checking corpus for: ', sA_Obj.getSubjects())
        subjectCorpus = chkCorpus(sA_Obj.getSubjects(), untaggedCorpus)
        print('chkCorpus returned:')
        print(subjectCorpus)

        # Check KB anainst Simp, subject(s), verb(s)... (was simpGA.py)
        print('-' * 10)
        kb_Obj = chkKB(sA_Obj, kb_Obj, subjectCorpus, subjectsInKB, simpKB)

        print('Results from chkKB which currently are KB matches:')
        #print(kbResults)
        kb_Obj.printAll()

        print('-' * 10)
        ppResults = preprocessInput(mismatch, multiple, unknown, sA_Obj, simpKB, subjectCorpus, kb_Obj)

        print('Results from preprocessInput:')
        print(ppResults)

        # Respond with appropiate output
        print('-' * 10)
        print('prattle (from processInput.py)...')
        outSent = prattle(sA_Obj)
        print('parttle retunred: ')
        print(outSent)

    return 'Exit.'


#
#
if __name__ == "__main__":

    print('Processing processInput (__main__)...')

    processUserInput()

