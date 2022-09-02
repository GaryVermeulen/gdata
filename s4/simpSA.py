#
# simpSA.py
#
#    Sentence analysis--determine SVO
#

import sys

################################################
def sentAnalysis(tl, f):
# Attempt to analyze the sentence per CFG (find SVO)
    
    print('--- sentAnalysis ---')

    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''
    det = ''

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
    elif len(tl) == 1:
        # Simple sentence trees are just 1 line
        print('simple sentence, or so they seem...')

        tStr = tl[0]

#        print(type(tStr))
#        print(len(tStr))
#        print(tStr)

        # Remove "\Tree " from tree string
        tStr = tStr.replace('\Tree ', '')

        tStrLen = len(tStr)

        print(tStrLen)
        print(tStr)

        # Build sentence matrix
        row = []
        col = []

        for sIdx in range(tStrLen):
            if tStr[sIdx] == ' ':
                col.append(row)
                row = []
            else:
                row.append(tStr[sIdx])                

        print('---')
        # Now build simplified list for if-then processing
        tags = []
        word = ""
        wordTags = []
        for c in col:
#            print(c)
            tag = ''
            if len(c) > 2 and c[1] == '.':
#                print('dot found')
#                print(len(c))
                if len(c) == 4: # NP, DT, VB,...
                    tag = c[-2] + c[-1]
                elif len(c) == 5: # NNP, NNS, VBD,...
                    tag = c[-3] + c[-2] + c[-1]
                elif c[-1] == 'S': # Don't forget the S
                    tag = c[-1]

#                print('tag: ' + str(tag))

                tags.append(tag)
                
            elif c[0] not in ['[',']']:

#                print(' bare c: ' + str(c))
                word = ''.join(c)

#                print('word: ' + str(word))

                wordTags.append(tags)
                wordTags.append(word)
                tags = []
                

#        print('simp sent: ' + str(wordTags))
#        print(len(wordTags))
        
        nnpFound = False
        
        if wordTags[0][0] == 'S':
            # They should all start with S
            if wordTags[0][1] == 'NP':
                # Starting with NP
                if wordTags[0][2] == 'DT':
                    # Determiner found
                    det = wordTags[1]
                    
                    if 'NN' in wordTags[2]:
                        sSubj = wordTags[3]

                        if len(wordTags) > 2:
                            if 'VP' in wordTags[4][0]:
                                sVerb = wordTags[5]
        
                    elif 'NNP' in wordTags[2]:
                        sSubj = wordTags[3]
                        nnpFound = True

                        if len(wordTags) > 2:                    
                            if wordTags[4][0] == 'VP':
                                sVerb = wordTags[5]
        
                elif wordTags[0][2] == 'NN':
                    sSubj = wordTags[1]

                    if len(wordTags) > 2:
                            if wordTags[2][0] == 'VP':
                                sVerb = wordTags[3]
                    
                elif wordTags[0][2] == 'NNP':
                    sSubj = wordTags[1]
                    nnpFound = True

                    if len(wordTags) > 2:                    
                        if wordTags[2][0] == 'VP':
                            sVerb = wordTags[3]

                        if len(wordTags) > 4:
                            if wordTags[4][0] == 'NP':
                                if wordTags[4][1] == 'NNP':
                                    # set a secondary nnpFound?
                                    sObj = wordTags[5]
                                elif wordTags[4][1] in ['NN','NNS']:
                                    sObj = wordTags[5]
                    
            elif wordTags[0][1] == 'VP':
                # Starting with VP should be imperative or interrogative
                # We'll worry about infinitive and auxilary later...
#                print('VP: ' + str(wordTags))
                sVerb = wordTags[1]
                if len(wordTags) > 2: # Checking for one word commands ex: stop
                    
                    if wordTags[2][1] == 'NNP':
                        nnpFound = True
                        sSubj = wordTags[3]
                        if len(wordTags) > 4:
                            if wordTags[4][0] == 'VP':
                                if len(wordTags) > 6:
                                    print('S starting with VP has greater length than checks')
                                else:
                                    sCommand = sVerb
                                    sVerb = wordTags[5]
                        else:
                            sCommand = sVerb
                            twoWordCommand = True
                            
                    elif wordTags[2][1] in ['NN', 'NNS']:
                        nnpFound = False
                        sSubj = wordTags[3]
                        if len(wordTags) > 4:
                            if wordTags[4][0] == 'VP':
                                if len(wordTags) > 6:
                                    print('S starting with VP has greater length than checks')
                                else:
                                    sCommand = sVerb
                                    sVerb = wordTags[5]
                        else:
                            sCommand = sVerb
                            twoWordCommand = True
                        
                else:
                    oneWordCommand = True


#        print('det: ' + str(det))
#        print('subject: ' + str(sSubj))
#        print('nnp?: ' + str(nnpFound))
#        print('verb/action: ' + str(sVerb))
        
    else:
        # This is going to be enormous--for now just:
        #   NP -> NN
        #   NP -> DT NNx (NN, NNP, NNS)
        #
        # Long term goal: An algorithm that can handle any 
        #   tree input including new (learned) CFG rules.
        #

        subject = ''
        np = ''
        dt = ''
        nextTag = ''
        nnpFound = False
        
        f.write('    a some-what more complex sentence\n')
        print('a some-what more complex sentence')
        print(len(tl))

        # Start with NP VP
        # Typically the first NP is the Subject
        for t in tl:
            print('t: ' + str(t))
            if t[-1] == 'S':
                print('Sentence root -- little to no value...~?')
            else:
                tStr = t
                tIdx = 0

#                print(type(tStr))
#                print(len(tStr))
#                print('>>>' + str(tStr) + '<<<')

                # Remove leading spaces
                tStr = tStr.lstrip()
                tStrLen = len(tStr)
                print(tStrLen)
                print('>' + str(tStr) + '<')
                    
                print('----')
#                print(tIdx)
#                print(tStr[tIdx])

                nextTag = tStr[tIdx + 2] + tStr[tIdx + 3]

#                print('nextTag: ' + str(nextTag))

                # may need to modify this in case
                # length is shorter than just one POS Tag
                if tStrLen <= 4:
                    lastTag = nextTag
                    continue
    

                # Build sentence matrix
                row = []
                col = []

                for sIdx in range(tStrLen):
                    if tStr[sIdx] == ' ':
                        col.append(row)
                        row = []
                    else:
                        row.append(tStr[sIdx])                
        
                print('---')
                # Now build simplified list for if-then processing
                tags = []
                word = ""
                wordTags = []
                for c in col:
##                    print(c)
                    tag = ''
                    if len(c) > 2 and c[1] == '.':
#                       print('dot found')
#                       print(len(c))
                        if len(c) == 4: # NP, DT, VB,...
                            tag = c[-2] + c[-1]
                        elif len(c) == 5: # NNP, NNS, VBD,...
                            tag = c[-3] + c[-2] + c[-1]
                        elif c[-1] == 'S': # Don't forget the S
                            tag = c[-1]

#                       print('tag: ' + str(tag))

                        tags.append(tag)
                
                    elif c[0] not in ['[',']']:

#                       print(' bare c: ' + str(c))
                        word = ''.join(c)

#                       print('word: ' + str(word))

                        wordTags.append(tags)
                        wordTags.append(word)
                        tags = []
                

#                print(wordTags)
#                print(len(wordTags))
#                print('lastTag: ' + str(lastTag))
#                print('nextTag: ' + str(nextTag))

#                print(wordTags[0])
#                print(wordTags[0][0])
#                print(wordTags[0][1])
#                print(wordTags[1])
        
        
                if wordTags[0][0] == 'NP':
                    # Starting with NP
                    if wordTags[0][1] == 'DT':
                        # Determiner found
                        det = wordTags[1]
                    
                        if 'NN' in wordTags[1]:
                            sSubj = wordTags[2]

                            if len(wordTags) > 2:
                                if 'VP' in wordTags[3][0]:
                                    sVerb = wordTags[4]
        
                        elif 'NNP' in wordTags[1]:
                            sSubj = wordTags[2]
                            nnpFound = True

                            if len(wordTags) > 2:                    
                                if wordTags[3][0] == 'VP':
                                    sVerb = wordTags[4]
        
                    elif wordTags[0][1] == 'NN':
                        sSubj = wordTags[1]

                        if len(wordTags) > 2:
                            if wordTags[1][0] == 'VP':
                                sVerb = wordTags[2]
                    
                    elif wordTags[0][1] == 'NNP':
                        sSubj = wordTags[1]
                        nnpFound = True

                        if len(wordTags) > 2:                    
                            if wordTags[1][0] == 'VP':
                                sVerb = wordTags[2]
                                
                    # For the strange occurrence of: [NP, NP, NNS]
                    elif wordTags[0][1] == 'NP':
                        sSubj = wordTags[1]

                        if len(wordTags) > 2:
                            if wordTags[2][0] == 'VP':
                                sVerb = wordTags[3]

                        if sCommand != '':
                            twoWordCommand = True
                    
                elif wordTags[0][0] == 'VP':
                    # Starting with VP
#                    print(wordTags)

                    sVerb = wordTags[1]
                    if sSubj == '':
                        sSubj = wordTags[3]
                    else:
                        sObj = wordTags[3]

                    nxLen = len(wordTags[2])
#                    print('where is the nnp?: ' + str(wordTags[2]))
#                    print(nxLen)
                    
                    if nxLen == 2:
                        if wordTags[2][1] == 'NNP':
                            nnpFound = True
                    elif nxLen == 3:
                        if wordTags[2][2] == 'NNP':
                            nnpFound = True
                        
                    sSubj = wordTags[3]
                    if len(wordTags) > 4:
                        if wordTags[4][0] == 'VP':
                            if len(wordTags) > 6:
                                    print('S starting with VP has greater length than checks')
                            else:
                                twoWordCommand = True
                                sCommand = sVerb
                                sVerb = wordTags[5]

                if lastTag == 'VP' and nextTag == 'VB':
                    sCommand = wordTags[1]


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
    print('det: ' + str(det))
    print('subject: ' + str(sSubj))
    print('nnp?: ' + str(nnpFound))
    print('verb/action: ' + str(sVerb))
    print('object: ' + str(sObj))
                    
        
#        print(' parent = %s' % subTree.parent())
    

    print('--- end sentAnalysis ---')

    return([sType, sSubj, sVerb, sObj])
# End sentAnalysis
