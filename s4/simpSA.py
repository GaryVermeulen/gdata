#
# simpSA.py
#
#    Sentence analysis--determine SVO
#

import sys

################################################
def sentAnalysis(tl, f):
# Attempt to analyze the sentence per CFG
    
    print('--- sentAnalysis ---')

    sType = ''
    sSubj = ''
    sVerb = ''
    det = ''

    sTag = ''
    sIdx = 0
#    rows, cols = (63, 63)
#    sMatrix = [[' ']*cols]*rows
#    print(sMatrix)
    
    for i in tl:
        print('>>' + str(i) + '<<')

    print('---')


    if len(tl) < 1:
        print('tl should never be less than 1')
    elif len(tl) == 1:
        # Simple sentence trees are just 1 line
        print('simple sentence')

        tStr = tl[0]

#        print(type(tStr))
#        print(len(tStr))
#        print(tStr)

        # Remove "\Tree " from tree string
        tStr = tStr.replace('\Tree ', '')

        tStrLen = len(tStr)

        print(tStrLen)
        print(tStr)

        # Build sentence metrix
        row = []
        col = []

        for sIdx in range(tStrLen):
            if tStr[sIdx] == ' ':
                col.append(row)
                row = []
            else:
                row.append(tStr[sIdx])                

        print('---')

        tags = []
        word = ""
        wordTags = []
        for c in col:
            print(c)
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
                

#        print(wordTags)
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
                    
            #elif wordTags[0][1] == 'VP':
                # Starting with VP

        print('det: ' + str(det))
        print('subject: ' + str(sSubj))
        print('nnp?: ' + str(nnpFound))
        print('verb/action: ' + str(sVerb))
        
        sys.exit()


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
        
        f.write('    a some-what more complex sentence\n')
        print('a some-what more complex sentence')
        print(len(tl))

        # Start with NP VP
        # Typically the first NP is the Subject
        for t in tl:
            print(t)
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
                print(len(tStr))
                print('>' + str(tStr) + '<')
                

                print('----')
#                print(tIdx)
#                print(tStr[tIdx])

                nextTag = tStr[tIdx + 2] + tStr[tIdx + 3]

                if nextTag == 'NP':

#                    np = nextTag

                    nextTag = tStr[tIdx + 7] + tStr[tIdx + 8]

                    if nextTag == 'NN':

                        nextTag = tStr[tIdx + 7] + tStr[tIdx + 8] + tStr[tIdx + 9]

                        if nextTag in ['NNP', 'NNS']:
                            tIdx = 11
                        else:
                            tIdx =  10
                    
                        while tStr[tIdx] != ' ':                    
                            subject = subject + tStr[tIdx]
                            tIdx = tIdx + 1

                    elif nextTag == 'DT':

                        print(len(tStr))
                        print(':>' + tStr + '<:')

                        tIdx = 10

                        while tStr[tIdx] != ' ':                    
                            dt = dt + tStr[tIdx]
                            tIdx = tIdx + 1
                        

                        dtLen = len(dt)
                        print('dtLen: ' + str(dtLen))

                        print(tIdx)
                        print(dtLen)
                        print(tStr[tIdx])
                        print(tStr[tIdx + 1])
                        print(tStr[tIdx + 2])
                        
                        print('--')

                        tIdx = tIdx + dtLen

                        print(tIdx)
                        print(tStr[tIdx])
                        print(tStr[tIdx + 1])
                        print(tStr[tIdx + 2])

                        # Advance to next TAG
                        while tStr[tIdx] != '.':                    
                            tIdx = tIdx + 1

                        print('DOT: ' + str(tStr[tIdx]))

                        nextTag = ''
                        tIdx += 1
                        # Cap to next TAG
                        while tStr[tIdx] != ' ':                    
                            
                            nextTag = nextTag + tStr[tIdx]
                            tIdx += 1

                        print(nextTag)
                        print(tStr[tIdx])

                        subject = ''
                        tIdx +=1
                        # Cap to next NN
                        while tStr[tIdx] != ' ':                    
                            
                            subject = subject + tStr[tIdx]
                            tIdx += 1


                        print('sub: ' + str(subject))

                    if len(dt) == 0:
                        np = subject
                    else:
                        np = dt + ' ' + subject

                    print('dt: >' + dt + '<')
                    print('subject: ' + subject)
                    print('np:' + np)
                    
                    break

        
        

                else:

                    print('not ready for this tag: ' + str(nextTag))
                    
        
#        print(' parent = %s' % subTree.parent())
    

    print('--- end sentAnalysis ---')

    return([sType, sSubj, sVerb])
# End sentAnalysis
