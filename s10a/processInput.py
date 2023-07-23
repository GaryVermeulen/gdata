#
# processInput.py
#

import pickle
import sys
import spacy

from commonUtils import *
from simpConfig import *
from processKB import *
from simpSA import *
from simpGA import chkGrammar
from checkKB import chkKB
#from processOutput import prattle

nlp = spacy.load("en_core_web_lg") # lg has best accuracy
#nlp = spacy.load("en_core_web_sm") # 


def sentenceAnalysis(tagged_uI, kbTree):

    print('------ start sentenceAnalysis ------')

    sA_Obj, error = sentAnalysis(tagged_uI, kbTree)

    if len(error) > 0:
        print('*** sentAnalysis returned possible errors:')
        for e in error:
            print(e)

    print('------ end sentenceAnalysis ------')

    return sA_Obj

def kbCommand(kbTree):

    nodeKey = input('Enter KB Node (key/name) to display: ')

    node = kbTree.find_node(kbTree.root, nodeKey)

    if node == None:
        print('Could not find a node named: ', nodeKey)
    else:
        print('key:      ', node.key)
        print('parent:   ', node.parentNode)
        print('similar:  ', node.similar)
        print('tag:      ', node.tag)
        print('canDo:    ', node.canDo)
        print('children: ', node.children)
        for c in node.children:
            print(c)
    
    return

def processUserInput():

    taggedCorpus = loadPickle('taggedCorpusSents')
    taggedBoW = loadPickle('taggedBoW')
    allInflections = loadPickle('inflections')
    kbTree = loadPickle('kbTree')

    while True:
        print('-' * 5)
        uI = input('Please enter a sentence or enter <kb>: ')
        print(uI)

        if uI == '':
            sys.exit('Nothing entered.')

        if uI == 'kb':
            kbCommand(kbTree)
            continue

        print('-' * 5)

        doc = nlp(uI)

        taggedInput = []
        for token in doc:
            tmpToken = ((str(token.text)), (str(token.tag_)))
            taggedInput.append(tmpToken)

        print('Spacy tagged input:')
        print(taggedInput)

        print('-' * 5)
        print('Checking KB for simp...')
        simpCanDo = kbTree.get_canDo(kbTree.root, simp)
        simpCanDo = simpCanDo.split(',')
        print('simpCanDo: ', simpCanDo)

        print('-' * 10)

        sA_Obj = sentenceAnalysis(taggedInput, kbTree)    
        sA_Obj.printAll()

        print('-' * 10)
        # save sA_Obj pickle
        print('Saving sentence analysis object:')
        savePickle('sA_Obj', sA_Obj)

        print('-' * 10)

        if sA_Obj.sSubj == '':
            print('Something is wrong: No subject returned.')
        else:
            print('Checking KB for sentence subject:', sA_Obj.sSubj[0])
            sentSubjectCanDo = kbTree.get_canDo(kbTree.root, sA_Obj.sSubj[0])
            if sentSubjectCanDo == None:
                print('{} retunred None from KB.'.format(sA_Obj.sSubj[0]))
            else:
                sentSubjectCanDo = sentSubjectCanDo.split(',')
                print('sentSubjectCanDo: ', sentSubjectCanDo)

        print('-' * 10)

        grammarResults = chkGrammar(sA_Obj, taggedCorpus)

        print('Results from chkGrammar:')
        print(grammarResults)
        
        print('-' * 10)
        print('Check KB...')

        kbNodes = chkKB(sA_Obj, kbTree)

        for node in kbNodes:
            print('---')
            print('key:      ', node.key)
            
            print('parent:   ', node.parentNode)
            print('similar:  ', node.similar)
            print('tag:      ', node.tag)
            print('canDo:    ', node.canDo)
            print('childern: ', node.children)
            for c in node.children:
                print(c)
            

        print('-' * 10)
        print('prattle (from processInput.py)...')
        print('Not yet...')
        #outSent = prattle(sA_Obj)
        #print('from processInput.py; outSent:')
        #print(outSent)

    return 'Exit.'


#
#
if __name__ == "__main__":

    print('Processing processInput (__main__)...')

    processUserInput()

