#
# Shell for Simpleton
#    Simple-Ton: A ton of simple things to do. From SpongeBob SquarePants.
#

import buildGrammar
import getInput
import discernInput

# Build grammar
#
buildGrammar.buildCFG()

# Get user input
#
s = getInput.getSentence()

print(str(s[0]))
print(str(s[1]))

# Parse input per grammar
#
retCode = discernInput.chkGrammar(s)

# Results of parse
#
if retCode == -1:
    print('retCode is -1 something not in grammar')
elif retCode == 0:
    print('Unable to find any productions in existing grammar')
else:
    print('chkGrammar is happy, productions found: ' + str(retCode))

# Uses feature grammar
#
# discernInput.featGrammar(s)

print('End Simple-Ton.')
