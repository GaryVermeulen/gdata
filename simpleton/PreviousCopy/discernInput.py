#
# discernInput.py
#

import nltk
import re
import modGrammar

#
def chkGrammar(s):

    simpleGrammar = nltk.data.load('file:/home/gary/src/simpleton/simp.cfg')

#    f = open("/home/gary/src/simpleton/simp.cfg", "r")
#    print(f.read())
#    f.close()

    fm = '/home/gary/src/simpleton/simpMem.txt'
    fmMode = 'a'

    rd_parser = nltk.RecursiveDescentParser(simpleGrammar)
    treesFound = []

    try:
        for tree in rd_parser.parse(s[1]):
            treesFound.append(tree)
            print(tree)

        if len(treesFound) == 0:
            retCode = 0
        else:
            fmem = open(fm, fmMode)
            for t in treesFound:
                fmem.write(str(t))
                fmem.write('\n')
            fmem.close()
            retCode = len(treesFound)
    
    except ValueError as err:
#        print('Problem with input not covered by grammar')
#        print('ValueError: {0}'.format(err))
        myErrHandler(err)        
        retCode = -1

    return retCode

#
def featGrammar(s):
    from nltk import load_parser
#    cp = load_parser('file:/home/gary/src/lucid/feature.cfg')
    cp = load_parser('file:/home/gary/src/lucid/feat0.fcfg')

    for tree in cp.parse(s[1]):
        print(tree)

    return

def myErrHandler(err):
    print('Problem with input not covered by grammar')
    print('ValueError: {0}'.format(err))

    missingWord = re.search('\'(.*)\'', str(err))
    mw = missingWord.group(1)
    print(mw)

    response = input('Shall we add > ' + mw + ' < to the lexicon and grammar? <Y/N>')

    if (response == 'Y') or (response == 'y'): modGrammar.addWord(mw) 
    
    return

