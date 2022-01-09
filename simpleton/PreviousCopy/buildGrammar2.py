"""

 buildGrammar.py

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

# CFG file
#
fCFG = 'simp.cfg'
fCFGmode = 'w'

#
# Lexicon
#
fLex = 'simpLex.txt'
fLmode = 'r'

rules = []

def buildCFG():

    with open(fLex, fLmode)

    inFile = fL.read()

    print(inFile)
    print(type(inFile))

    
    

#        print('======')
#        print(f_in, end='')
#        print('------')
#
#    print('_+_+_+_+_+_+_')
#    for r in rules:
#        print(r, end='')
#
#    print('+_+_+_+_+_+_+')
#
#    fout = open(fCFG, fCFGmode)
#    for r in rules:
#        fout.write(r)
#    fout.close()
    
    print('End buildCFG')
    return

buildCFG()
