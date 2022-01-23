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

lex = []
rules = []

def buildCFG():

    with open(fLex, fLmode) as fin:
        
        while (line := fin.readline().rstrip()):
            
            lex.append(line)
           
    
#    print('_+_+_+_+_+_+_')
#    for l in lex:
#        print(l)
#
#    print(len(word))
#    print(len(lex))
#
#    print('_+_+_+_+_+_+_')
#    for l in lex:
#        ll = l.split(", ")
#        print('____________')
#        for w in ll:
#            print(w)
#    
#    print('+_+_+_+_+_+_+')

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

# buildCFG()
