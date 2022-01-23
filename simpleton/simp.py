#
# Shell for Simpleton
#    Simple-Ton: A ton of simple things to do. From SpongeBob SquarePants.
#

from dataclasses import dataclass
import simpMods as sm

@dataclass
class NP:
    # Class attribute
    species = "et al"

    name: str
    gender: str
    isA: str
    canDo: str

@dataclass
class Nouns:
    # Vauge since the lex is so small
    name: str
    isA: str
    canDo: str
    

myNames = []
myNouns = []

print("Simple-Ton, A ton of simple things to do.")
print("Reading data, one moment please...")

# Build a list of nouns (N) from lex
lexNouns = sm.getNouns()
print(str(len(lexNouns)) + " Nouns (N) read.")

# Build a list of names (NP) from lex
lexNames = sm.getNames()
print(str(len(lexNames)) + " Nouns (NP) read.")

# Build an isA list from KB
isA = sm.getIsA()
print(str(len(isA)) + " isA relations read.")

# Build an canDo list from KB
canDo = sm.getCanDo()
print(str(len(canDo)) + " canDo relations read.")

# Build a list of name (NP) objects with attributes from KBs
for name in lexNames:
    name_isA = "DK"
    for x in isA:
        if x[0] == name[0]:
            if x[1] != '':
                name_isA = x[1]

    name_canDo = "DK"
    for x in canDo:
        if x[0] == name[0]:
            if x[1] != '':
                name_canDo = x[1]
    
    myNames.append(NP(name[0],"DK",name_isA,name_canDo))

print("----------------------")

for obj in myNames:
    print(obj.name, obj.gender, obj.isA, obj.canDo, sep=' : ')

print("----------------------")

# Build a list of noun (N) objects with attributes from KBs
for noun in lexNouns:
    noun_isA = "DK"
    for x in isA:
        if x[0] == noun[0]:
            if x[1] != '':
                noun_isA = x[1]

    noun_canDo = "DK"
    for x in canDo:
        if x[0] == noun[0]:
            if x[1] != '':
                noun_canDo = x[1]
    myNouns.append(Nouns(noun[0],noun_isA,noun_canDo))

for o in myNouns:
    print(o.name, o.isA, o.canDo, sep=' ')

# Build grammar
#
#r = input("Build CFG <y/n>?: ")
#if r == 'y' or r == 'Y':
#    simpMods.buildCFG()
#    print('New CFG built...')
#else:
#    print('Skipped CFG build...')

loop = True

while loop:
    
    # Get user input
    #
    s = sm.getSentence()

    # Simple tokenizer
    #tok_s = word_tokenize(s)

    # Parse input per grammar
    #
    retCode = sm.chkGrammar(s)

    # retCode will be either:
    # 1)
    #  retType: <class 'list'>
    #  [Tree('S', [Tree('NP', ['Mary']), Tree('VP', [Tree('V', ['walked']), Tree('NP', ['Pookie']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('N', ['park'])])])])])]
    # 2)
    #  retType: <class 'ValueError'>
    #  Grammar does not cover some of the input words: "'Harry'".
    # 3)
    #  retType: <class 'int'>
    #  0

    if retCode == 0:
        print('-->>Unable to find any productions in existing grammar')
    
    elif isinstance(retCode, ValueError):
        print('-->>retCode returned a ValueError' + str(ValueError))
#        print('ValueError: {0}'.format(retCode))
        if sm.myErrHandler(retCode):
            sm.learningMode(retCode)
    
    elif isinstance(retCode, list):
        print('-->>Input is grammatically correct per CFG')
        print('-->>Searching for relationships and/or meaning...')
        sm.searchMeaning(s, myNames, myNouns)
    else:
        print('-->>Something unexpected happened')
        

#        for x in retCode:
#            print(type(x))
#            print(x)
#
#        simpMods.getNodes(retCode)       
    
##    else:
##        print('-->>Something unexpected happened')

#    print('Checking for basic infrence(s) on raw input: ')
#    print('>' + str(s) + '<')
#
##    simpMods.analyzeInput(s)

    


    r = input("Conitune <y/n>?: ")
    if r == 'y' or r == 'Y':
        loop = True
    else:
        print('Exiting...')
        loop = False
    
print('End Simple-Ton.')

# end simp.py
