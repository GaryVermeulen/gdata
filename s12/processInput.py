#
# processInput.py
#

import sys
import pickle
import time
import commonConfig

#from commonConfig import inputSentence, Context, nnx, prpx
from commonConfig import inputSentence, nnx, prpx

from string import punctuation
#from bson.binary import Binary

from commonUtils import connectMongo
#from commonUtils import chk_nnxKB # For kb command
#from commonUtils import chkTagging
#from commonUtils import isWordKnown
#from commonUtils import getTag
#from commonUtils import expandSent # Old way
from kbChecker import getSimpKB
from expandAndTag import expandAndTag

from assimilate import assimilate

from kbEdit import modKB
#from commonConfig import Sentence, kbResults

#from scrapeWord import scrapeWord, scrapeWord2
#from scrapeWord2 import scrapeWord2
#from saveWebWord import saveWebWord
#from simpSA import sentAnalysis
#from simpSA2 import sentAnalysis2
#from kbChecker import getSimpKB, chkKB
#from processOutput import prattle


def kbCommand(nominalsKB):

    ui = ''

    nodeKey = input('Enter KB Node (key/name) to display: ')

    node = nominalsKB.find({"_id":nodeKey})

    if node == None:
        print('Could not find a node named: ', nodeKey)
    else:
        print('node: ', node)
        print('----')
        for item in node:
            print('item: ', item)
            print('item["_id"]: ', item["_id"])
            
            ui = input('Modify this doc <Y/N>? ')
            if ui in ['y', 'Y']:
                newItem = modKB(item, nominalsKB)
                q = {"_id": item["_id"]}
                v = {"$set": newItem}
                nominalsKB.update_one(q, v)
                print('Mongo updated?')
        
    return


def processUserInput():

    mdb = connectMongo()
    simpDB = mdb["simp"]
    # Semi-permanent KBs
    nominalsKB = simpDB["nominalsKB"]
    
    # Interchangeable input KBs & data
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    untaggedCorpus = simpDB["untaggedCorpus"]

#    named_tuple = time.localtime() # get struct_time
#    time_string = time.strftime("%m%d%Y_%H%M%S", named_tuple)
#    converCol = "conversationCol_" + time_string
#
#    conversationCol = simpDB[converCol] # Retain current conversation
#
    # Current conversation buffer
#    conversationLst = []
#    conversationObj = Context(0, [], [], [], [], []) # Not sure about this anymore...~?
    
    # Who am I or know thy self...
    simpKB = getSimpKB(nominalsKB)
    
    while True:
        print('-' * 10)
        uI = input('Please enter a sentence or enter <kb>: ')
        print(uI)

        if uI == '':
            print('-' * 10)
            sys.exit('Exiting; Nothing entered.')

        if uI == 'kb':
            kbCommand(nominalsKB)
            continue

        print('-' * 10)
        print('Processing user input...')
        inSentObj = inputSentence(uI, [], [])
        
        uI = uI.rstrip(punctuation)
        taggedInput = expandAndTag(uI)
        print('taggedInput: ', taggedInput)
        print('-' * 10)
        tmpSent = []
        for w in taggedInput:
            tmpSent.append({"word": w[0], "tag": w[1]})
            
        assimilate(None, tmpSent)
        

        # Dummies for for old method:
        # mismatch, multiple, unknown, baseWord = chkTagging(taggedInput, tagged_BoW)
        #mismatch = "DUMMY"
        #multiple = "DUMMY"
        #unknown  = "DUMMY"
        #baseWord = "DUMMY"

# Change processing so that we only need to read from the
# "accumulated" universal KBs

        """

        print('-' * 10)
        print('Check if Simp knows the input words...')

        for w in inSentObj.taggedSent:
#            print('Checking if {} exists in current dataset (checks all data)'.format(w))
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

        # But does known word tag match the input tag?
        print('-' * 10)
        print('Do the input sentence tags match the known data tags?')

        newData = []
        
        for d in inSentObj.data:
#            print('pI d: ', d)
#            print('-----')
            newWordData = []
            newWordData.append(d[0])
        
            for x in d:
#                print('x: ', x)
                if isinstance(x[1], bool):
#                    print('(isinstance(x[1], bool)')
                    if x[1]:
#                        print('x[1] True')
#                        print('x: ', x)
#                        print('d[0]: ', d[0])

                        tagResults = getTag(d[0], x[0])
                        newTags = []
                        newTags.append(x[0])
                        newTags.append(x[1])
#                        print('tagResults: ', tagResults)
                        if tagResults == None:
                            tagResults = []
                        for tr in tagResults:
#                            if d[0][1] != tr[1]:
#                                print('d[0][1] {} does not match tr[1] {}'.format(d[0][1], tr[1]))
#                            else:
#                                print('d[0][1] {} matches tr[1] {}'.format(d[0][1], tr[1]))
#                            print('tr[1]: ', tr[1])
                            newTags.append(tr[1])
#                        print('newTags: ', newTags)
                        newTags = tuple(newTags)
                        newWordData.append(newTags)
#                        print('---')
#                    else:
#                        print('x[1] else:')
#                    
#                else:
#                    print('else:  (isinstance(x[1], bool)')
#
#                print('newWordData: ', newWordData)

            newData.append(newWordData)        

#        print('----')
#        for d in newData:
#            print(d)
#

        print('----')
        inSentObj._newData = newData
        inSentObj.printAll()

        print('----')
        print('Conclusion of input words/tags matching data:') 
        for d in inSentObj._newData:
            word = d[0][0]
            tag  = d[0][1]
            print('for word {} with tag {}'.format(word, tag))
            for i in d:
                if tag in i:
                    print('tag in i: ', i)
                else:
                    print('tag not in i: ', i)
                
                
        
        

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


        # Add SVO info to inSentObj
        print('-' * 10)
        
        inSentObj._type = "NONE"
        inSentObj._subject = "NONE"
        inSentObj._compoundSubject = "NONE"
        inSentObj._verb = "NONE"
        inSentObj._object = "NONE"
        inSentObj._indirectObject = "NONE"
        
        inSentObj._type = newSA_Obj.type
        inSentObj._subject = newSA_Obj.subject
        inSentObj._compoundSubject = "TO DO"
        inSentObj._verb = newSA_Obj.verb
        inSentObj._object = newSA_Obj.object
        if newSA_Obj.isVar("_indirectObject"):
            inSentObj._indirectObject = newSA_Obj._indirectObject
        else:
            inSentObj._indirectObject = []
        print('inSentObj:')
        inSentObj.printAll()
        
        # Doesn't really buy us anything, so comment it out for now
        # Check KB anainst Simp, subject(s), verb(s)... (was simpGA.py)
        
        """
        """
        print('-' * 10)
        kb_Obj = chkKB(newSA_Obj, nnxKB, untaggedCorpus)

        kb_Obj.tagMismatch = mismatch
        kb_Obj.tagMultiple = multiple
        kb_Obj.tagUnknown = unknown

        print('kb_Obj: ')
        kb_Obj.printAll()

        """
        """
        # Conext checking for pronouns--which method to use?
        #
        print('-' * 20)
        print("Determine context, and append svo's to conversationObj...")
        
        conversationObj.sentNo += 1

        print('Current conversationObj:')
        conversationObj.printAll()

        print('-' * 10)

        # First build or add to conversation window object
        #
        ##subjects = newSA_Obj.getSubjectsAndTags()
        subjects = inSentObj._subject

        print('subjects: ', subjects)
        
        if len(subjects) > 0:
            if isinstance(subjects, tuple):
                conversationObj.subjects.append([subjects])
            elif isinstance(subjects, list):
                conversationObj.subjects.append(subjects)
        else:
            conversationObj.subjects.append([('No Subject', 'None')])
            print('No subject(s) error: ', subjects)
            
                    
        # compoundSubjects (indirectSubjects) ToDo
        conversationObj.compoundSubjects.append([('TODO', 'NONE')])

        # Add objects
        objects = inSentObj._object

        print('objects: ', objects)
        
        if len(objects) > 0:
            if isinstance(objects, tuple):
                conversationObj.objects.append([objects])
            elif isinstance(objects, list):
                conversationObj.objects.append(objects)
        else:
            conversationObj.objects.append([('No Object', 'None')])
            print('No object(s) error: ', objects)
        
        # Add indirectObjects
        indirectObjects = inSentObj._indirectObject

        print('indirectOjects: ', indirectObjects)
        
        if len(indirectObjects) > 0:
            if isinstance(indirectObjects, tuple):
                conversationObj.indirectObjects.append([indirectObjects])
            elif isinstance(indirectObjects, list):
                conversationObj.indirectObjects.append(indirectObjects)
        else:
            conversationObj.indirectObjects.append([('No indirectObject', 'None')])
            print('No indirectObject(s) error: ', indirectObjects)

        # Add actions (verbs)
        actions = inSentObj._verb

        print('actions: ', actions)
        
        if len(actions) > 0:
            if isinstance(actions, tuple):
                conversationObj.actions.append([actions])
            elif isinstance(actions, list):
                conversationObj.actions.append(actions)
        else:
            conversationObj.actions.append([('No actions', 'None')])
            print('No actions error: ', actions)

        print('-' * 10)
        conversationObj.printAll()

        # Can we match a prpx to a nnx?
        # Then get the correct he/she...
        #

        print('-' * 10)
        print('subjects: ', subjects)
        
        if isinstance(subjects, tuple): # Only one subject in current input sentence
            if subjects[1] in prpx:
                if len(conversationObj.subjects) > 0:
                    for conSub in conversationObj.subjects:
                        print('conSub: ', conSub)
                        for c in conSub:
                            print('c: ', c)
                            if c[1] in nnx:
                                print("For subject {} do you mean {}?".format(subjects, c))
                                
                            elif c[1] in prpx:
                                if subjects[0] != c[0]:
                                    print("Confusing subjects {} who you mean? Last subject: {}?".format(subjects, c))
                else:   
                    print('No subject context for: ', subjects)
                    
        elif isinstance(actions, list):
            for s in subjects:
                print('s in subjects: ', s)
        
        """
        """            
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

        ##conversationLst.append((time_string, newSA_Obj, kb_Obj))
        conversationLst.append((time_string,inSentObj ))

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

        """
        print('-' * 10)
        ppResults = preprocessInput(mismatch, multiple, unknown, sA_Obj, kb_Obj)

        print('Results from preprocessInput:')
        print(ppResults)
        """
#        # Respond with appropiate output
#        print('-' * 10)
#        print('SKIPPING: prattle (from processInput.py)...')
#        print('parttle retunred: ')
#        print(outSent)
#
#
    print('-' * 30)
    
    # Drop current conversation window
    converWinCol = simpDB["ConverWinCol"]
    converWinCol.drop()

    print('converWinCol dropped.')

    return 'Exit--processInput'


#
#
if __name__ == "__main__":

    print('Start processInput (__main__)...')

    processUserInput()

    print('End -- processInput (__main__)')

