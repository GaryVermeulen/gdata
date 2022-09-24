#
# simpSA.py
#
#    Sentence analysis--determine SVO
#

import sys

ftslog = 'tagged_sentence_log.txt'


################################################
def sentAnalysis(tl, f):
# Attempt to analyze the sentence per CFG (find SVO)
    
    print('--- sentAnalysis x version---')

    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''
    sDet = ''
    sIN = ''

    sVerbs = []
    sentence = []

    sCommand = '' # Imperative sentence start verb
    oneWordCommand = False 
    twoWordCommand = False # 'See Bob' or 'Do something'

    lastTag = ''

    sTag = ''
    sIdx = 0

    print('tl len: ' + str(len(tl)))
    
    for i in tl:
        print('>>' + str(i) + '<<')

    print('---')


    if len(tl) < 1:
        print('tl should never be less than 1')
        
    else:

        subject = ''
        np = ''
        dt = ''
        nextTag = ''
        nnpFound = False
        
#        f.write('    a some-what more complex sentence\n')
        print('tl: ')
        print(tl)
        print('tl len: ' + str(len(tl)))

        
        for t in tl:
            # Skip blank lines
            if len(t) <= 0:
                continue
            
            print('t len: ' + str(len(t)))
            print('t: ' + str(t))
            
            tStr = t
            tIdx = 0

            print(type(tStr))
            print(len(tStr))
            print('>>>' + str(tStr) + '<<<')

            # Remove "\Tree " & S tag from tree string
            tStr = tStr.replace('\Tree ', '')
            tStr = tStr.replace('[.S' , '')

            # Remove leading spaces
            tStr = tStr.lstrip()
            tStrLen = len(tStr)

            # In case everything was repalced
            if tStrLen <= 0:
                continue

            # String contains only a POS tag
            if tStrLen <= 4:
                lastTag = nextTag
                continue
            
            print(tStrLen)
            print('>' + str(tStr) + '<')
                    
            print('----')
#            print(tIdx)
#            print(tStr[tIdx])

#            nextTag = tStr[tIdx + 2] + tStr[tIdx + 3]

#            print('nextTag: ' + str(nextTag))


            # Build sentence matrix
            row = []
            col = []

            for sIdx in range(tStrLen):
                if tStr[sIdx] == ' ':
                    col.append(row)
                    row = []
                else:
                    row.append(tStr[sIdx])                
        
#            print('---')
            # Now build simplified list for if-then processing
            tags = []
            word = ""
            wordTags = []

#            print('col: ' + str(col))
            for c in col:
#                print('1st c: ' + str(c))
                tag = ''
                if len(c) > 2 and c[1] == '.':
#                    print('dot found')
#                    print(len(c))
                    if len(c) == 4: # NP, DT, VB,...
                        tag = c[-2] + c[-1]
                    elif len(c) == 5: # NNP, NNS, VBD,...
                        tag = c[-3] + c[-2] + c[-1]
                    elif c[-1] == 'S': # Don't forget the S
                        tag = c[-1]
#                    print('tag: ' + str(tag))

                    tags.append(tag)
                
                elif c[0] not in ['[',']']:

#                    print(' bare c: ' + str(c))
                    word = ''.join(c)

#                    print(' word: ' + str(word))

                    wordTags.append(tags)
                    wordTags.append(word)
                    tags = []
                

            print('wordTags: ' + str(wordTags))

            sentence.append(wordTags)
#               

        # End of for loop -- for t in tl

        fl = open(ftslog, 'a')
        fl.write(str(sentence) + '\n')
        fl.close()


        print('sentence len: ' + str(len(sentence)))
        print('sentence:')
        print(sentence)
        print('---')

        for s in sentence:
            print(s)

        print('---')

#            if lastTag == 'VP' and nextTag == 'VB':
#                sCommand = wordTags[1]


    if oneWordCommand:
        if sVerb == 'compute':
            print('What do you wish me to ' + str(sVerb))
        else:
            print('Sorry, I cannot ' + str(sVerb))

    if twoWordCommand:
        if sCommand == 'compute':
            print('What do you wish me to ' + str(sCommand))
        else:
            print('Sorry, I cannot ' + str(sCommand))
        


    print('sCommand: ' + str(sCommand))
    print('oneWordCommand: ' + str(oneWordCommand))
    print('twoWordCommand: ' + str(twoWordCommand))
    print('det: ' + str(sDet))
    print('sin: ' + str(sIN))
    print('subject: ' + str(sSubj))
    print('nnp?: ' + str(nnpFound))
    print('verb/action: ' + str(sVerb))
    print('all verbs: ' + str(sVerbs))
    print('object: ' + str(sObj))

    sType = 'unknown'

    sVerb = ','.join(sVerbs)
                    
        
#        print(' parent = %s' % subTree.parent())
    

    print('--- end sentAnalysis ---')

    return([sType, sSubj, sVerb, sObj])
# End sentAnalysis
