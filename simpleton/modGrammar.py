#
# modGrammar.py
#

fLex = 'simpLex.txt'
fLmode = 'a'

def addWord(nw):

    validInput = ["NP", "N", "V", "P", "Det"]
    

    print('Adding ' + nw + ' to lexicon')
    print('Tags: NP (names), N (nouns), V (verbs), P (preposition: in, on, with), Det (determiner: a, an, the)')
    response = input('Please a tag for > ' + nw + ' < from the above tags: <Q/q to Quit> ')

    if (response == 'Q') or (response == 'q') or (response not in validInput):
        print('Quiting or invalid entry...')
        return
    
    f = open(fLex, fLmode)
    f.write('\n' + str(nw) + ',' + str(response))
    f.close()

    print(str(nw) + ',' + str(response) + ' added to lexicon')
  
    return

# addWord('some')
