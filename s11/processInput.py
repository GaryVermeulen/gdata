#
# processInput.py
#

import sys
#import spacy
import pickle
import time
import commonConfig

from commonConfig import Context, nnx, prpx

from string import punctuation
#from bson.binary import Binary

from commonUtils import connectMongo
from commonUtils import chkTagging
from commonUtils import isWordKnown
from commonUtils import getInflectionTag
from commonUtils import getInflections
#from commonUtils import expandSent # Old way
from expandAndTag import expandAndTag

#from commonConfig import Sentence, kbResults


#from simpSA import sentAnalysis
from simpSA2 import sentAnalysis2
from kbChecker import chkKB
from processOutput import prattle

#nlp = spacy.load("en_core_web_lg") # lg has best accuracy
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
    conversationLst = []
    conversationObj = Context(0, [], [], [], [], [])
    
    while True:
        print('-' * 10)
        uI = input('Please enter a sentence or enter <kb>: ')
        print(uI)

        if uI == '':
            print('-' * 10)
            #res = input('Retain conversation <Y/n>? ')
            #if res in ['Y', 'y', 'Yes', 'yes']:
            #    print('Conversation kept.')
            #else:
            #    conversation = simpDB["conversation"]
            #    conversation.drop()
            #    print('Conversation dropped.')

            sys.exit('Exiting; Nothing entered.')

        if uI == 'kb':
            kbCommand(nnxKB)
            continue

        print('-' * 10)
        print('Preprocess user input...')
        # Old way
        #eUI_List = expandSent(uI)
        #eUI_Str = ' '.join(eUI_List)
        # New way
        # Remove punctuation from end
        uI = uI.rstrip(punctuation)
        print('rstrip: ', uI)
        taggedInput = expandAndTag(uI)

        print('expanded and tagged input:')
        print(taggedInput)

        # Check tagged uI aginst taggedBoW for conflicts
        # There's also tagging errors, ex: returns: ('work', 'VB') instead of: ('work', 'NN')
        # Yet another can of worms!
        print('-' * 10)
        print('Checking tags...')

        mismatch, multiple, unknown, baseWord = chkTagging(taggedInput, tagged_BoW)

        print('chkTagging results:')
        print('Mismatch: ', mismatch)
        print('Multiple: ', multiple)
        print('Unknown: ', unknown)
        print('baseWord: ', baseWord)
        print('-' * 10)

        # Since the above is unwieldy let's break it up into smaller singular functions
        for w in taggedInput:
            print('Checking if {} exists in current dataset (checks all data)'.format(w))
            isWordKnownRes = isWordKnown(w, tagged_BoW)
            if isWordKnownRes:
                print('{} is known.'.format(w[0]))
            else:
                print('{} is completely unknown.'.format(w[0]))
            print('---')

        # New sentence analysis
        print('-' * 10)
        print('New sentence analysis')
        newSA_Obj, error2 = sentAnalysis2(taggedInput)
        print('...')
        newSA_Obj.printAll()

        if len(error2) > 0:
            print('New sentence analysis returned an error:')
            for e in error2:
                print(e)

            print('Ignoring input sentence')
            continue

        # Check KB anainst Simp, subject(s), verb(s)... (was simpGA.py)
        print('-' * 10)
        kb_Obj = chkKB(newSA_Obj, nnxKB, untaggedCorpus)

        kb_Obj.tagMismatch = mismatch
        kb_Obj.tagMultiple = multiple
        kb_Obj.tagUnknown = unknown

        print('kb_Obj: ')
        kb_Obj.printAll()

        # Conext checking for pronouns--which method to use?
        print('-' * 20)
        print("Determine context, and append svo's to conversationObj...")
        
        conversationObj.sentNo += 1



        
        subjects = newSA_Obj.getSubjectsAndTags()
        if len(subjects) > 0:
            for s in subjects:
                if s[1] in prpx:
                    if len(conversationObj.subjects) > 0:
                        for cs in conversationObj.subjects:
                            if cs[1] in nnx:
                                print("For subject {} do you mean {}?".format(s, cs))
                    else:
                        print('No subject context for: ', s)
                else:
                    print('{} is the subject'.format(s))

                conversationObj.subjects.append(list(s))
        else:
            print('No subject(s) error: ', subjects)

        # compoundSubjects ToDo
        conversationObj.compoundSubjects.append('TODO')
        
        objects  = newSA_Obj.getObjectsAndTags()
        print('objects: ', objects)
        if objects != None:  # TODO: tagging errors: ex: work,VB | work,NN
            for o in objects:
                if o[1] in prpx:
                    if len(conversationObj.objects) > 0:
                        for co in conversationObj.objects:
                            print("For object {} do you mean {}?".format(co, o))
                    else:
                        print('No object context for: ', o)
                else:
                    print('{} is the object'.format(o))
                
                conversationObj.objects.append(list(o))
        else:
            print('No object(s) error: ', objects)

        if newSA_Obj.isVar('_indirectObject'):
            if isinstance(newSA_Obj._indirectObject, tuple):
                conversationObj.indirectObjects.append(list(newSA_Obj._indirectObject))
                
            elif isinstance(newSA_Obj._indirectObject, list):
                tmpLst = []
                for indirectObjectTuple in newSA_Obj._indirectObject:
                    tmpLst.append(indirectObjectTuple)
                conversationObj.indirectObjects.append(tmpLst)
        else:
            print('No _indirectObject var found.')
            
        actions = newSA_Obj.getVerbsAndTags()
        if len(actions) > 0:
            tmpLst = []
            for a in actions:
                tmpLst.append(a)
            conversationObj.actions.append(tmpLst)
        else:
            print('No actions/verbs error: ', actions) 
        
        print('-' * 10)                
        conversationObj.printAll()
        

        print("Saving conversation to conversationLst...")
        
        named_tuple = time.localtime() # get struct_time
        print(named_tuple)
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

        print(time_string)

        conversationLst.append((time_string, newSA_Obj, kb_Obj))

        print('-' * 10)
        print('There are {} sentences in the current conversastionLst.'.format(len(conversationLst)))

        #if len(conversationLst) == 1:
        #@    conversationObj = Context([], [], [], [], [])

        print('-' * 10)
        print('len conversationLst: ', len(conversationLst))
        for c in conversationLst:
            print('c: ', c)
            print('-' * 5)
            for i in c:
                print('i type: ', type(i))
                print('i: ', i)
                if isinstance(i, str):
                    print('Time: ', i)
                elif isinstance(i, commonConfig.Sentence):
                    print('Sentence Obj:')
                    i.printAll()
                elif isinstance(i, commonConfig.kbResults):
                    print('kbResults Obj:')
                    i.printAll()
                else:
                    print('do not know what i is: ', i)


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


        print('-' * 30)

    return 'Exit--processInput'


#
#
if __name__ == "__main__":

    print('Start processInput (__main__)...')

    processUserInput()

    print('End -- processInput (__main__)')

