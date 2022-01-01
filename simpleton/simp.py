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
    print('--Unable to find any productions in existing grammar')
elif isinstance(retCode, ValueError):
    print('--retCode returned a ValueError')
    print(str(retCode))
elif isinstance(retCode, list):
    print('--Input is grammatically correct per CFG')
    print('--Check for basic infrence(s)...')
    simpMods.analyzeInput(retCode)
else:
    print('--Something unexpected happened')


print('End Simple-Ton.')

# end simp.py
