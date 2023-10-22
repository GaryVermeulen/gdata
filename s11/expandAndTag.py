#
# expandAndTag.py
#
# Take input sentence and
# attempt to provide the correct grammatical form.
# Ex: I'd can be I would or I had
#

import spacy # spacy is a pig

from commonConfig import *

nlp = spacy.load("en_core_web_sm") # lg has best accuracy


def expandAndTag(inputSentence):

    expandedSentence = []
    verySimple = False

    if len(inputSentence) == 0:
        return ['Error: input len 0']

    #print('START -- expandAndTag --')

    if inputSentence.find("'") != -1: # Possible contraction
        tmpSent = inputSentence.split()
        for w in tmpSent:
            
            w = w.strip()

            #print('w: ', w)
            
            if w.find("'") != -1: # Doesn't handle idioms such as: someone's
                if w in very_simple_contractions.keys():
                    result = very_simple_contractions[w]
                    resultList = result.split()
                    verySimple = True
                    for r in resultList:
                        expandedSentence.append(r)
                else:
                    #print('else-w: ', w)
                    verySimple = False
                    expandedSentence.append(w)

            else:
                expandedSentence.append(w)

        #print('expandedSentence:')
        #print(expandedSentence)

        doc = nlp(' '.join(expandedSentence))
        
        tagSent = []
        for token in doc:
            tmpToken = ((str(token.text)), (str(token.tag_)))
            tagSent.append(tmpToken)
            
        #print('if tagSent:')
        #print(tagSent)

        idx = 0
        if not verySimple:
            newTagSent = []
            #print('not simple')
            for w in tagSent:
                if w[0] == "'d":
                    #print('found d')
                    #print('w: ', w)
                    #print('idx: ', idx)
                    #print('tagSent[idx + 1]: ', tagSent[idx + 1])
                    if tagSent[idx + 1][1] in [rb, vbn, jj]:
                        w = ("had", vbd)
                    #    print('new had w: ', w)
                    else:
                        w = ("would", "MD")
                    #    print('new would w: ', w)
                        
                newTagSent.append(w)
                idx += 1

            #print('newTagSent:')
            #print(newTagSent)
            
            tagSent = newTagSent

    else: # No ' in sentence, so just tag it
        doc = nlp(inputSentence)
        
        tagSent = []
        for token in doc:
            tmpToken = ((str(token.text)), (str(token.tag_)))
            tagSent.append(tmpToken)
            
#        print('else tagSent:')
#        print(tagSent)
    
    #print('END -- expandAndTag --')
    
    return tagSent

#
if __name__ == "__main__":

    print('START -- expandAndTag -- main --')

    inputSentence = ''
    
    #inputSentence = "I'd never bused so many dishes in one night"
    # [('I', 'PRP'), ('had', 'VBD'), ('never', 'RB'), ('bused', 'VBN'), ('so', 'RB'), ('many', 'JJ'), ('dishes', 'NNS'), ('in', 'IN'), ('one', 'CD'), ('night', 'NN')]
    #
    #inputSentence = "I wish I'd waited longer"
    # [('I', 'PRP'), ('wish', 'VBP'), ('I', 'PRP'), ('had', 'VBD'), ('waited', 'VBN'), ('longer', 'RBR')]
    #
    #inputSentence = "He'd gone home"
    # [('He', 'PRP'), ('had', 'VBD'), ('gone', 'VBN'), ('home', 'RB')]
    #
    #inputSentence = "She'd just spoken to her"
    # [('She', 'PRP'), ('had', 'VBD'), ('just', 'RB'), ('spoken', 'VBN'), ('to', 'IN'), ('her', 'PRP')]
    
    #inputSentence = "I'd like some tea"
    # [('I', 'PRP'), ('would', 'MD'), ('like', 'VB'), ('some', 'DT'), ('tea', 'NN')]
    #
    #
    #inputSentence = "I'd have gone if I had had time"
    # [('I', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('gone', 'VBN'), ('if', 'IN'), ('I', 'PRP'), ('had', 'VBD'), ('had', 'VBN'), ('time', 'NN')]
    #
    #inputSentence = "He'd have been 70 today"
    # [('He', 'PRP'), ('would', 'MD'), ('have', 'VB'), ('been', 'VBN'), ('70', 'CD'), ('today', 'NN')]

    #inputSentence = "I'll see you tomorrow"
    # [('I', 'PRP'), ('will', 'MD'), ('see', 'VB'), ('you', 'PRP'), ('tomorrow', 'NN')]

    #inputSentence = "I thought love was only true in fairy tales"
    # [('I', 'PRP'), ('thought', 'VBD'), ('love', 'NN'), ('was', 'VBD'), ('only', 'RB'), ('true', 'JJ'), ('in', 'IN'), ('fairy', 'NN'), ('tales', 'NNS')]

    print('inputSentence:')
    print(inputSentence)

    expandedSentence = expandAndTag(inputSentence)

    print('expandedSentence:')
    print(expandedSentence)

    print('END -- expandAndTag -- main --')    
    
    
