#
# simpMods.py
#
"""
 buildCFG()
 Contruct a simple CFG file using the the example from the NLTK Book
 Input:  simpLex.txt
 Input format: 'word', 'N, V, P, or Det', 'optional short description'
 
 File: simp.cfg
 Output foramt: S -> NP VP
                VP -> V NP | V NP PP
                PP -> P NP
                NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
                N -> "man" | "dog" | "cat" | "telescope" | "park"
                V -> "saw" | "ate" | "walked"
                P -> "in" | "on" | "by" | "with"
                Det -> "a" | "an" | "the" | "my"

 Symbol    Meaning 	            Example
 ------    ------                  ----------------
 S 	   sentence                the man walked
 NP 	   noun phrase             a dog
 VP 	   verb phrase             saw a park
 PP 	   prepositional phrase    with a telescope
 Det 	   determiner              the
 N 	   noun                    dog
 V 	   verb                    walked
 P 	   preposition             in                

 File: simp3.cfg
 Output foramt: S -> NP VP | VP | AUX NP VP
                NP -> ProN | PropN | Det Nom
                Nom -> N Nom | N
                ProN -> "me" | "I" | "you" | "it"
                PropN -> "John" | "Mary" | "Bob" | "Pookie" | "Pete" | "Jane" | "Sam"
                N -> "cat" | "man" | "dog" | "telescope" | "park" | "duck" | "bus"
                VP -> V | V NP | V NP PP | V PP
                V -> "saw" | "ate" | "walked" | "ran" | "fly"
                PP -> Prep NP
                Prep -> "in" | "on" | "by" | "with" | "at"
                Det -> "a" | "an" | "the" | "my" | "some"
                AUX -> "can" | "could" | "might" | "will"
                
 
"""


import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
import re

# Our own module
#import modGrammar

# Pyke implementation
#
##import contextlib
##import sys
##import time


# CFG file
#
##fCFG = 'simp.cfg'
##fCFG = 'simp3.cfg'
fCFG = '/home/gary/src/simpleton/simpPTPoS.cfg'

#
# Lexicon
#
fLex = 'simpLex.txt'

#
# KBs
#
fKBcan = 'simpKBcan.txt'
fKBis = 'simpKBis.txt'


###
def getNouns():

    nouns = []

    with open(fCFG, 'r') as fin:
        
        while (line := fin.readline().rstrip()):

            line = line.replace("-", '')
            line = line.replace(" ", '')

            line = line.split(">")

            if line[0] == 'NN':
                s = line[1].split('|')
                       
    fin.close()

    return(s)

# getNouns

###
def getNames():

    names = []

    with open(fCFG, 'r') as fin:
        
        while (line := fin.readline().rstrip()):

            line = line.replace("-", '')
            line = line.replace(" ", '')

            line = line.split(">")

            if line[0] == 'NNP':
                s = line[1].split('|')
                       
    fin.close()
    
    return(s)

# End getNames()

###
def getIsA():

    isAList = []
    
    with open(fKBis, 'r') as fis:
        
        while (line := fis.readline().rstrip()):
            
            line = line.split(":")
            isAList.append(line)

    fis.close()

    return(isAList)
    
# End getIsA

###
def getCanDo():
    
    canDoList = []
    
    with open(fKBcan, 'r') as fcan:
        
        while (line := fcan.readline().rstrip()):
            
            line = line.split(":")
            canDoList.append(line)

    fcan.close()

    return(canDoList)

# End getCanDo()

###
def buildCFG():
    
#    lex = []
#    rules = []
#
#    with open(fLex, 'r') as fin:
#        
#        while (line := fin.readline().rstrip()):
#            
#            lex.append(line)
#
#    fin.close()
#
#    fout = open(fCFG, 'w')
#
#    # Currently only adding words
#    #
#    S = 'S -> NP VP'
#    VP = 'VP -> V NP | V NP PP'
#    PP = 'PP -> P NP'
#    NP = ''
#    N = ''
#    V = ''
#    P = ''
#    Det = ''
#
#    for l in lex:
#        ll = l.split(',')
#        
#        if ll[1] == 'NP':
#            if len(NP) == 0:
#                NP = 'NP -> ' + '\"' + str(ll[0]) + '\"'
#            else:
#                NP = NP + ' | \"' + str(ll[0]) + '\"'
#        elif ll[1] == 'N':
#            if len(N) == 0:
#                N = 'N -> ' + '\"' + str(ll[0]) + '\"'
#            else:
#                N = N + ' | \"' + str(ll[0]) + '\"'
#        elif ll[1] == 'V':
#            if len(V) == 0:
#                V = 'V -> ' + '\"' + str(ll[0]) + '\"'
#            else:
#                V = V + ' | \"' + str(ll[0]) + '\"'
#        elif ll[1] == 'P':
#            if len(P) == 0:
#                P = 'P -> ' + '\"' + str(ll[0]) + '\"'
#            else:
#                P = P + ' | \"' + str(ll[0]) + '\"'
#        elif ll[1] == 'Det':
#            if len(Det) == 0:
#                Det = 'Det -> ' + '\"' + str(ll[0]) + '\"'
#            else:
#                Det = Det + ' | \"' + str(ll[0]) + '\"'
#        
#        
#    rules.append(S)
#    rules.append(VP)
#    rules.append(PP)
#    rules.append(NP + ' | Det N | Det N PP')
#    rules.append(N)
#    rules.append(V)
#    rules.append(P)
#    rules.append(Det)
#    
#    for r in rules:
#        fout.write(r + '\n')
#        
#    fout.close()
#    
    print('End buildCFG')
    return

# end buildCFG()

###
def buildKBs(word, tag):

    myErr = False
    
    print(' Currently words are added to KBs, but without any realationships.')
    print(' You will need to maually add relationships via a text editor.')
    print(' Adding: ' + str(word) + ' To KBs as per tag: ' + str(tag))

    if tag == 'NP':
        print('NP')
        myErr = False
    elif tag == 'N':
        print('N')
        myErr = False
    elif tag == 'V':
        print('V')
        myErr = True
    elif tag == 'P':
        print('P')
        myErr = True
    elif tag == 'Det':
        print('Det')
        myErr = True
    else:
        print('Unknown tag: ' + str(tag) + ' KBs not updated.')
        myErr = True

    if not myErr:
        fi = open(fKBis, fAMode)
        fi.write(word + ':')
        fi.close()

        print('Added: ' + str(word) + ' to: ' + str(fKBis))

        fc = open(fKBcan, fAMode)
        fc.write(word + ':')
        fc.close()

        print('Added: ' + str(word) + ' to: ' + str(fKBcan))
    else:
        print('Word: ' + str(word) + ' not added to KBs.')

    return

# End buildKBs

###
def getSentence():

    s = input("Enter a short sentence: ")

    tok_s = word_tokenize(s)

    print("You entered the" , len(tok_s), "words:" , tok_s)
#
#    pos_s = nltk.pos_tag(tok_s)
#    print('POS: ' + str(pos_s))
#    print('Original s: ' + str(s))

    return s
# end getSentence()

###
def chkGrammar(s):

##    simpleGrammar = nltk.data.load('file:/home/gary/src/simpleton/simp3.cfg')
##    simpleGrammar = nltk.data.load('file:/home/gary/src/simpleton/simpPTPoS.cfg')
    simpleGrammar = nltk.data.load('file:' + str(fCFG))

    fm = '/home/gary/src/simpleton/simpMem.txt'
    fmMode = 'a'

    rd_parser = nltk.RecursiveDescentParser(simpleGrammar) # , trace=2)
    treesFound = []

    slist = s.split()

    fmem = open(fm, fmMode)

    try:
        for tree in rd_parser.parse(slist):
            treesFound.append(tree)
            print('>' + str(tree) + '<')

        if len(treesFound) == 0:
            fmem.write('Input: ' + str(s) + ' - did not produce a tree:\n')
            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(tok_s)
            fmem.write('Simple tokenizer: ' + str(pos_s) + '\n')
            retCode = 0
        else:
            fmem = open(fm, fmMode)
            fmem.write('Input: ' + str(s) + ' - produced:\n')
            for t in treesFound:
                fmem.write(str(t))
                fmem.write('\n')
            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(tok_s)
            fmem.write('Simple tokenizer: ' + str(pos_s) + '\n')
            
#            retCode = len(treesFound)
            retCode = treesFound
    
    except ValueError as err:
#        print('Problem with input not covered by grammar')
#        print('ValueError: {0}'.format(err))
#        myErrHandler(err)        
#        retCode = -1
        retCode = err
        
    fmem.close()
    
    return retCode

# end chkGrammar(s)


###
def myErrHandler(err):

    learningMode = False
    
    print('ErrH: Problem with input not covered by grammar')
    print('ErrH: ValueError: {0}'.format(err))

#    missingWord = re.search('\'(.*)\'', str(err))
#    mw = missingWord.group(1)
#    print(mw)
#
    response = input('Shall we enter learning mode? <Y/N>')

    if (response == 'Y') or (response == 'y'):
        learningMode = True
    
    return learningMode

# end myErrHandler(err):


###
def getNodes(parent):

    ROOT = 'ROOT'
    tree = ...
    
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == ROOT:
                print("======== Sentence =========")
                print("Sentence:", " ".join(node.leaves()))
            else:
                print("Label:", node.label())
                print("Leaves:", node.leaves())

            getNodes(node)
        else:
            print("Word:", node)

# end getNodes(parent)


###
def searchMeaning(s, names, nouns):

    sNames = []
    sNouns = []
    matchedIsA = []
    matchedCanDo = []

    s = s.split(' ')
    print('Input s: ' + str(s))
#    print(len(nouns))

    # Build lists of names and nouns within input sentense
    for w in s:
        for n in names:
            if w == n.name:
                sNames.append(n)
                
        for noun in nouns:
            if w == noun.name:
                sNouns.append(noun)
                
    print("Found " + str(len(sNames)) + " name nouns (NNP).")
    print("Found " + str(len(sNouns)) + " nouns (NN).")
    print("----------------------")

    # Of the names found in the input sentense
    # extract their isA(s) and canDo(s)
    for sn in sNames:
        print(sn.name, sn.gender, sn.isA, sn.canDo, sep=' ; ')
        isAs = sn.isA
        canDos = sn.canDo

        print("Obj name: " + str(sn.name))
        
        if isAs != "DK":
            isAs = isAs.split(',')
            print(" Split isAs: " + str(isAs))
        else:
            print(" Obj isA: " + str(sn.isA))
        

        if canDos != "DK":
            canDos = canDos.split(',')
            print(" Split canDos: " + str(canDos))

            for w in s:
                if w in canDos:
                    print("=>Match: " + str(sn.name) + " " + str(w))
                    matchedCanDo.append(str(sn.name) + " " + str(w))
                    
        else:
            print(" Obj canDos: " + str(sn.canDo))
        

    print("Found " + str(len(sNouns)) + " nouns (N).")
    print("----------------------")
    # Of the nouns found in the input sentense
    # extract their isA(s)    
    for n in sNouns:
        print(n.name, n.isA, n.canDo, sep=' ; ')
        isAs = n.isA
        canDos = n.canDo
        
        print("Obj name: " + str(n.name))
        
        if isAs != "DK":
            isAs = isAs.split(',')
            print(" Split isAs: " + str(isAs))
        else:
            print(" Obj isA: " + str(n.isA))
        

        if canDos != "DK":
            canDos = canDos.split(',')
            print(" Split canDos: " + str(canDos))

            for w in s:
                if w in canDos:
                    print("=>Match: " + str(n.name) + " " + str(w))
                    matchedCanDo.append(str(n.name) + " " + str(w))
            
        else:
            print(" Obj canDos: " + str(n.canDo))

    if len(matchedCanDo) > 0:
        for d in matchedCanDo:
            print("matchedCanDo: " + str(d))
    else:
        print("No relationships found.")

    return s
# End searchMeaning(s)

###
def addWord(nw):

    tag_not_found = []
    word_added = []
    lines = []
    idx = 0

    print('Entering addWord...')

    nw = nw.replace(",", '')

#    print(len(nw))
#    print('>' + str(nw) + '<')
#    print(nw)
#    print(type(nw))

    tok_nw = word_tokenize(nw)
    pos_nw = pos_tag(tok_nw)
#    print(pos_nw)

    print('NLTK tagged input as:')
    for w in pos_nw:
        print(w)
#        print(type(w))
        
        response = input('Is the above tag correct <Yy>?')

        if response not in 'Yy':
            c_tag = input('Enter corrrect tag: ')
            w0 = w[0]
            new_w = (w0, c_tag)
            pos_nw[idx] = new_w
            print('You have entered: ' + str(new_w))
#            print(type(w))

        idx = idx + 1
        
    print(pos_nw)

    # Reading CFG
    #
    with open(fCFG, 'r') as fin:        
        while (line := fin.readline().rstrip()):        
            lines.append(line)
    fin.close()

    for l in lines:
        print(l)

        l = l.replace("-", '')
        l = l.replace(" ", '')
        l = l.split(">")

        print(l)


        for w in pos_nw:
            print(w)
            if l[0] == w[1]:
                print('== l[0]: ' + str(l[0]))
                print('   l[1]: ' + str(l[1]))
                print('== w[1]: ' + str(w[1]))
                print('   w[0]: ' + str(w[0]))

                # Does the new word exist? If not add it...
                #
                
                word_added.append(w)

            else:
                if w not in tag_not_found:
                    tag_not_found.append(w)
                
   
    if len(tag_not_found) > 0:
        for t in tag_not_found:
            print('-- Tag not in CFG: ' + str(t))

##    f = open(fLex, fAMode)
##    f.write(str(nw) + ',' + str(response))
##    f.close()

#    print(str(nw) + ',' + str(response) + ' added to lexicon')
#    print("Rebuilding CFG & KBs...")

#    buildKBs(nw, response)

    print('End addWord.')
      
    return

# End addWord()

###
def learningMode(nW):

    nWs = []
    
    print('Learning Mode:')
    print(nW)

    missingWord = re.search('\'(.*)\'', str(nW))    
    nW = missingWord.group(1)
    nW = nW.replace("'", '')

    addWord(nW)
    
#    res = input('[M]anual add, [A]uto-add, or [E]xit <M/A/E>?')
#    if res in 'Mm':
#        print('Manual add')
#        for w in nWs:
#            w = w.strip()
#            addWord(w)
#    elif res in 'Aa':
#        print('Auto-add')
#    else:
#        print('Else Exit')

    

    print('Exiting Learning Mode.')

    return
# End learningMode
