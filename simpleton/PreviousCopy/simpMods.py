#
# simpMods.py
#
"""

 buildCFG()

 Contruct a simple CFG file using the the example from the NLTK Book

 Input:  simpLex.txt
 Input format: 'word', 'N, V, P, or Det', 'optional short description'
 
 Output: simp.cfg
 Output foramt: S -> NP VP
                VP -> V NP | V NP PP
                PP -> P NP
                NP -> "John" | "Mary" | "Bob" | Det N | Det N PP
                N -> "man" | "dog" | "cat" | "telescope" | "park"
                V -> "saw" | "ate" | "walked"
                P -> "in" | "on" | "by" | "with"
                Det -> "a" | "an" | "the" | "my"

 Modified for my wild plans to take over the world
     Step one add new words to the CFG
     Step two add/modify the CFG to handle more complex sentences


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


"""


import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
import re
import modGrammar

# Pyke implementation
#
import contextlib
import sys
import time


# CFG file
#
fCFG = 'simp.cfg'
fCFGmode = 'w'

#
# Lexicon
#
fLex = 'simpLex.txt'
fLmode = 'r'

lex = []
rules = []

###
def buildCFG():

    with open(fLex, fLmode) as fin:
        
        while (line := fin.readline().rstrip()):
            
            lex.append(line)

    fout = open(fCFG, fCFGmode)

    # Currently only adding words
    #
    S = 'S -> NP VP'
    VP = 'VP -> V NP | V NP PP'
    PP = 'PP -> P NP'
    NP = ''
    N = ''
    V = ''
    P = ''
    Det = ''

    for l in lex:
        ll = l.split(',')
        
        if ll[1] == 'NP':
            if len(NP) == 0:
                NP = 'NP -> ' + '\"' + str(ll[0]) + '\"'
            else:
                NP = NP + ' | \"' + str(ll[0]) + '\"'
        elif ll[1] == 'N':
            if len(N) == 0:
                N = 'N -> ' + '\"' + str(ll[0]) + '\"'
            else:
                N = N + ' | \"' + str(ll[0]) + '\"'
        elif ll[1] == 'V':
            if len(V) == 0:
                V = 'V -> ' + '\"' + str(ll[0]) + '\"'
            else:
                V = V + ' | \"' + str(ll[0]) + '\"'
        elif ll[1] == 'P':
            if len(P) == 0:
                P = 'P -> ' + '\"' + str(ll[0]) + '\"'
            else:
                P = P + ' | \"' + str(ll[0]) + '\"'
        elif ll[1] == 'Det':
            if len(Det) == 0:
                Det = 'Det -> ' + '\"' + str(ll[0]) + '\"'
            else:
                Det = Det + ' | \"' + str(ll[0]) + '\"'
        
        
    rules.append(S)
    rules.append(VP)
    rules.append(PP)
    rules.append(NP + ' | Det N | Det N PP')
    rules.append(N)
    rules.append(V)
    rules.append(P)
    rules.append(Det)
    
    for r in rules:
        fout.write(r + '\n')
    fout.close()
    
    print('End buildCFG')
    return

# end buildCFG()

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

    simpleGrammar = nltk.data.load('file:/home/gary/src/simpleton/simp.cfg')

#    f = open("/home/gary/src/simpleton/simp.cfg", "r")
#    print(f.read())
#    f.close()

    fm = '/home/gary/src/simpleton/simpMem.txt'
    fmMode = 'a'

    rd_parser = nltk.RecursiveDescentParser(simpleGrammar)
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
# For now checking input sentence aginst simpLex.txt
# Not using grammar or retCode from chkGrammar
#
def analyzeInput(inSent):

    fKB = 'simpKB.txt'
    fMode = 'r'
    f = open(fKB, fMode)
    KB = {}
    sTagged = []
    
    print('Analyzining input for infernces...')

#    print('--Input given: ' + str(i))

    inSent = inSent.split(' ')

#    print('--Split Input: ' + str(inSent))   

    with open(fLex, fLmode) as fin:
        while (line := fin.readline().rstrip()):
            lex.append(line)

#    print('>' + str(lex) + '<')

    wordcount = 0
    lexcount = 0

    for word in inSent:
        wordcount = wordcount + 1
        for l in lex:
            lexcount = lexcount + 1
            l = l.split(',')
            if word in l:
#                print('Found: ' + str(word) + ' wordcount: ' + str(wordcount) + ' In: ' + str(l) + ' lexcount: ' + str(lexcount))
                sTagged.append(str(l))

#    print('sTagged: ' + str(sTagged))

    sT =[]
    for i in sTagged:
        if i not in sT:
            sT.append(i)
            
    print('--Input sentenace tagged: ' + str(sT))


    for line in f:
        line = line.strip('\n')
        key, value = line.split(':')
        KB[key] = value
#        print(line)

    f.close()

#    print(KB)
    
    keyFigures = []

    for key, value in KB.items():
        if key in inSent:
#            print('key: ' + str(key) + ' in inSent: ' + str(inSent))
            print('--' + str(key) + ' can: ' + str(value))
            keyFigures.append(str(key) + ':' + str(value))
    

    print('--Key Features of input sentance: ')
    print('--: ' + str(keyFigures))

    conclusion = []
    
    for k in keyFigures:
        print(k)
        kS = k.split(':')
        print(kS)
        print(kS[0])
        print(kS[1])

        for w in inSent:
            if w in kS[1]:
                print('  w: ' + str(w) + ' found in kS[1]: ' + str(kS[1]))
                conclusion.append(str(kS[0] + ' : ' + w))

    print('Conclusion: ' + str(conclusion))
    
    return 

# end analyzeInput(i)

###
def myErrHandler(err):
    print('Problem with input not covered by grammar')
    print('ValueError: {0}'.format(err))

    missingWord = re.search('\'(.*)\'', str(err))
    mw = missingWord.group(1)
    print(mw)

    response = input('Shall we add > ' + mw + ' < to the lexicon and grammar? <Y/N>')

    if (response == 'Y') or (response == 'y'): modGrammar.addWord(mw) 
    
    return

# end myErrHandler(err):


ROOT = 'ROOT'
tree = ...
#
def getNodes(parent):
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

