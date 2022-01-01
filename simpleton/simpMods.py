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

from pyke import knowledge_engine, krb_traceback, goal
# Compile and load .krb files in same directory that I'm in (recursively).
engine = knowledge_engine.engine(__file__)

fc_goal = goal.compile('family.how_related($person1, $person2, $relationship)')

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
        ll = l.split(', ')
        
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
def analyzeInput(i):

    # Existing knowledge base
    #
#    fName = '/home/gary/src/simpleton/kb.txt'
#   fMode = 'r'
#    f = open(fName, fMode)
#    kb = f.read()
    
    print('Analyzining input for infernces...')

    print('--Input given: ' + str(i))

    print('--But just testing for \'bob\'...')

#    driver.fc_test('bob') -- Below is from example driver.py

    '''
        This function runs the forward-chaining example (fc_example.krb).
    '''
    engine.reset()      # Allows us to run tests multiple times.

    person1 = 'bob'

    start_time = time.time()
    engine.activate('fc_example')  # Runs all applicable forward-chaining rules.
    fc_end_time = time.time()
    fc_time = fc_end_time - start_time

    print("doing proof")
    with fc_goal.prove(engine, person1=person1) as gen:
        for vars, plan in gen:
            print("%s, %s are %s" % \
                    (person1, vars['person2'], vars['relationship']))
    prove_time = time.time() - fc_end_time
    print()
    print("done")
    engine.print_stats()
    print("fc time %.2f, %.0f asserts/sec" % \
          (fc_time, engine.get_kb('family').get_stats()[2] / fc_time))


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
