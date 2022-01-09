#
# Shell for Simpleton
#    Simple-Ton: A ton of simple things to do. From SpongeBob SquarePants.
#

##import simpMods
import simpMods

# Build grammar
#
r = input("Build CFG <y/n>?: ")
if r == 'y' or r == 'Y':
    simpMods.buildCFG()
    print('New CFG built...')
else:
    print('Skipped CFG build...')

loop = True

while loop:
    
    # Get user input
    #
    s = simpMods.getSentence()

    # Simple tokenizer
    #tok_s = word_tokenize(s)

    # Parse input per grammar
    #
    retCode = simpMods.chkGrammar(s)

    # retCode will be either:
    # 1)
    # retType: <class 'list'>
    # [Tree('S', [Tree('NP', ['Mary']), Tree('VP', [Tree('V', ['walked']), Tree('NP', ['Pookie']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('N', ['park'])])])])])]
    # 2)
    # retType: <class 'ValueError'>
    # Grammar does not cover some of the input words: "'Harry'".
    # 3)
    # retType: <class 'int'>
    # 0

    if retCode == 0:
        print('-->>Unable to find any productions in existing grammar')
    
    elif isinstance(retCode, ValueError):
        print('-->>retCode returned a ValueError')
    
    elif isinstance(retCode, list):
        print('-->>Input is grammatically correct per CFG')

#        for x in retCode:
#            print(type(x))
#            print(x)
#
#        simpMods.getNodes(retCode)       
    
    else:
        print('-->>Something unexpected happened')

#    print('Checking for basic infrence(s) on raw input: ')
#    print('>' + str(s) + '<')
#
    simpMods.analyzeInput(s)

    r = input("Conitune <y/n>?: ")
    if r == 'y' or r == 'Y':
        loop = True
    else:
        print('Exiting...')
        loop = False
    
print('End Simple-Ton.')

# end simp.py
