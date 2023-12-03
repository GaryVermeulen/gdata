#
# processInput.py
#

import sys
#import spacy
import pickle
import time
import commonConfig

from commonConfig import inputSentence, Context, nnx, prpx

from string import punctuation
#from bson.binary import Binary

from commonUtils import connectMongo
from commonUtils import chkTagging
from commonUtils import isWordKnown
from commonUtils import getTag
from commonUtils import getInflectionTag
from commonUtils import getInflections
#from commonUtils import expandSent # Old way
from expandAndTag import expandAndTag

#from commonConfig import Sentence, kbResults

#from scrapeWord import scrapeWord, scrapeWord2
from scrapeWord2 import scrapeWord2
from saveWebWord import saveWebWord
#from simpSA import sentAnalysis
from simpSA2 import sentAnalysis2
from kbChecker import getSimpKB, chkKB
from processOutput import prattle

#nlp = spacy.load("en_core_web_lg") # lg has best accuracy
#nlp = spacy.load("en_core_web_sm") # 


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


def processUserInput():

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    untaggedCorpus = simpDB["untaggedCorpus"]
    conversationLst = []
    conversationObj = Context(0, [], [], [], [], [])
    # Who am I or know thy self...
    simpKB = getSimpKB(nnxKB)
    
    while True:
        print('-' * 10)
        uI = input('Please enter a sentence or enter <kb>: ')
        print(uI)

        if uI == '':
            print('-' * 10)
            sys.exit('Exiting; Nothing entered.')

        if uI == 'kb':
            kbCommand(nnxKB)
            continue

        print('-' * 10)
        print('Processing user input...')
        inSentObj = inputSentence(uI, [], [])
        
        uI = uI.rstrip(punctuation)
        taggedInput = expandAndTag(uI)

        tmpLst = []
        for wt in taggedInput:
            if wt[1] not in ['NNP', 'NNPS']:
                wt = (wt[0].lower(), wt[1])
            tmpLst.append(wt)
        
        inSentObj.taggedSent = tmpLst
        print('Expanded and tagged input:')
        print(tmpLst)
        inSentObj.printAll()

        # Dummies for for old method:
        # mismatch, multiple, unknown, baseWord = chkTagging(taggedInput, tagged_BoW)
        mismatch = "DUMMY"
        multiple = "DUMMY"
        unknown  = "DUMMY"
        baseWord = "DUMMY"

        print('-' * 10)
        print('Check if Simp knows the input words...')

        for w in inSentObj.taggedSent:
            print('Checking if {} exists in current dataset (checks all data)'.format(w))
            isWordKnownRes,inSentObj = isWordKnown(w, inSentObj)
            if isWordKnownRes:
                print('"{}" is known.'.format(w[0]))
                #inSentObj.printAll()
 
            else:
                print('"{}" is completely unknown.'.format(w[0]))
                print('Seacrhing/scaping web for unkown word: ', w)

                wordDefs = scrapeWord2(w)

                if len(wordDefs) > 0:
                    print('wordDefs:')
                    for wd in wordDefs:
                        print(wd)
                        if w[1] == wd['tag']:
                            print('Word ({}) and new word ({}) match'.format(w, wd))
                        else:
                            print('Word ({}) and new word ({}) do not match'.format(w, wd))
                    results = saveWebWord(wordDefs)
                else:
                    print('Scraping was unable to find word: ', w)
                
            print('---')
        print('inSentObj:')
        inSentObj.printAll()

        # But does know word tag match the input tag?
        print('-' * 10)
        print('Do the input sentence tags match the known data tags?')
        
        for d in inSentObj.data:
            print('pI d: ', d)
        
            for x in d:
                if isinstance(x[1], bool):
                    if x[1]:
                        print('x: ', x)
                        print('d[0]: ', d[0])

                        tagResults = getTag(d[0], x[0])
                        print('---')
        
                
        

        # New sentence analysis
        print('-' * 10)
        print('New sentence analysis:')
        #newSA_Obj, error2 = sentAnalysis2(inSentObj.taggedSent)
        newSA_Obj, error2 = sentAnalysis2(inSentObj)
        print('...')
        print('newSA_Obj:')
        newSA_Obj.printAll()

        if len(error2) > 0:
            print('New sentence analysis returned an error:')
            for e in error2:
                print(e)

            print('Ignoring input sentence')
            continue
        else:
            print('New sentence analysis did not return any errors.')

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
                print('s in subjects: ', s)
                if s[1] in prpx:
                    if len(conversationObj.subjects) > 0:
                        for cs in conversationObj.subjects:
                            if cs[1] in nnx:
                                print("For subject {} do you mean {}?".format(s, cs))
                            elif cs[1] in prpx:
                                print("Confusing subjects {} who you mean? Last subject: {}?".format(s, cs))
                        conversationObj.subjects.append(s)                    
                    else:   
                        print('No subject context for: ', s)
                        conversationObj.subjects.append(s)    
                else:
                    print('{} is the subject'.format(s))
                    conversationObj.subjects.append(s)
        else:
            conversationObj.subjects.append((('No Subject', 'None')))
            print('No subject(s) error: ', subjects)

        # compoundSubjects ToDo
        conversationObj.compoundSubjects.append((('TODO', 'NONE')))
        
        objects  = newSA_Obj.getObjectsAndTags()
        print('objects: ', objects)
        if objects != None:  # TODO: tagging errors: ex: work,VB | work,NN
            for o in objects:
                print('o in object: ', o)
                if o[1] in prpx:
                    if len(conversationObj.objects) > 0:
                        for co in conversationObj.objects:
                            print("For object {} do you mean {}?".format(co, o))
                            conversationObj.objects.append(o)
                    else:
                        print('No object context for: ', o)
                        conversationObj.objects.append(o)
                else:
                    print('{} is the object'.format(o))
                    conversationObj.objects.append(o)
        else:
            conversationObj.objects.append((('No Object', 'None')))
            print('No object(s) error: ', objects)

        if newSA_Obj.isVar('_indirectObject'):
            if isinstance(newSA_Obj._indirectObject, tuple):
                conversationObj.indirectObjects.append(list(newSA_Obj._indirectObject))
                
            elif isinstance(newSA_Obj._indirectObject, list):
                tmpLst = []
                for indirectObjectTuple in newSA_Obj._indirectObject:
                    print('indirectObjectTuple: ', indirectObjectTuple)
                    tmpLst.append(indirectObjectTuple)
                conversationObj.indirectObjects.append(tmpLst)
        else:
            print('No _indirectObject var found.')
            conversationObj.indirectObjects.append((('No Indirect Object', 'None')))
            
        actions = newSA_Obj.getVerbsAndTags()
        if len(actions) > 0:
            #tmpLst = []
            for a in actions:
                print('a in actions: ', a)
                conversationObj.actions.append(a)
                #tmpLst.append(a)
            #conversationObj.actions.append(tmpLst)
        else:
            print('No actions/verbs error: ', actions) 
            conversationObj.actions.append((('No actions/verbs', 'None')))
            
        print('-' * 10)                
        conversationObj.printAll()
        

        print("Saving conversation to conversationLst...")
        
        named_tuple = time.localtime() # get struct_time
        #print(named_tuple)
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
            #print('c: ', c)
            #print('-' * 5)
            for i in c:
                #print('i type: ', type(i))
                #print('i: ', i)
                if isinstance(i, str):
                    print('Time: ', i)
                elif isinstance(i, commonConfig.Sentence):
                    print('Sentence Obj:')
                    i.printAll()
                elif isinstance(i, commonConfig.kbResults):
                    print('kbResults Obj:')
                    i.printAll()
                else:
                    print('*** Do not know what i is: ', i)


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

