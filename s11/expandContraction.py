#
# expandContraction.py
#
# Take input sentence and
# attempt to provide the correct grammatical form.
# Ex: I'd can be I would or I had
#

from commonConfig import simple_contractions


def expandContraction(inputSentence):

    expandedSentence = []

    print('START -- expandContraction --')

    tmpSent = inputSentence.split()
    
    for w in tmpSent:
            
            w = w.strip()
            
            if w.find("'") != -1: # Doesn't handle idioms such as: someone's
                if w in simple_contractions.keys():
                    result = simple_contractions[w]
                    resultList = result.split()
                    for r in resultList:
                        expandedSentence.append(r)
                else:
                    print('>>{}<< not in  contractions'.format(w))
                    print('inputSentence: ', inputSentence)
                continue
                        
            clean_word = ''.join(filter(str.isalnum, w))

            if len(clean_word) > 0:
                expandedSentence.append(clean_word)
                
    
    print('END -- expandContraction --')
    
    return expandedSentence

#
if __name__ == "__main__":

    print('START -- expandContraction -- main --')
    
    inputSentence = "I'd never bused so many dishes in one night"
    
    # [('I', 'PRP'), ('had', 'VBD'), ('never', 'RB'), ('bused', 'VBN'), ('so', 'RB'), ('many', 'JJ'), ('dishes', 'NNS'), ('in', 'IN'), ('one', 'CD'), ('night', 'NN')]
    #
    # I wish I'd waited longer
    # [('I', 'PRP'), ('wish', 'VBP'), ('I', 'PRP'), ('had', 'VBD'), ('waited', 'VBN'), ('longer', 'RBR')]
    #
    # He'd gone home
    # [('He', 'PRP'), ('had', 'VBD'), ('gone', 'VBN'), ('home', 'RB')]
    #
    # She'd just spoken to her
    # [('She', 'PRP'), ('had', 'VBD'), ('just', 'RB'), ('spoken', 'VBN'), ('to', 'IN'), ('her', 'PRP')]
    
    # I'd like some tea
    # [('I', 'PRP'), ('would', 'MD'), ('likw', 'VB'), ('some', 'DT'), ('tea', 'NN')]
    #
    #
    # I'd have gone if I had had time
    # [('I', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('gone', 'VBN'), ('if', 'IN'), ('I', 'PRP'), ('had', 'VBD'), ('had', 'VBN'), ('time', 'NN')]
    #
    # He'd have been 70 today
    # [('He', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('been', 'VBN'), ('70', 'CD'), ('today', 'NN')]

    expandedSentence = expandContraction(inputSentence)

    print('expandedSentence:')
    print(expandedSentence)

    print('END -- expandContraction -- main --')    
    
    
