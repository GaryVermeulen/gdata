#
# simpSA.py
#
#    Sentence analysis--determine SVO
#

################################################
def sentAnalysis(tl, f):
# Attempt to analyze the sentence per CFG
    
    print('--- sentAnalysis ---')

    sType = ''
    sSubj = ''
    sVerb = ''
    
#    print('s:')
#    print(s)
#    print('sd:')
#    print(sd) # simpData
    
    # Fewer rules to check then words
#    cfgRules = getCFGRules()

    # Break up sentence into phrases
#    lstSize = len(s)
#    lstIdx = [lstIdx + 1 for lstIdx, lstVal in enumerate(s) if lstVal not in cfgRules]
#
#    res = [s[i: j] for i, j in
#           zip([0] + lstIdx, lstIdx +
#               ([lstSize] if lstIdx[-1] != lstSize else []))]

#    print('res:')             
#    print(res)
#    print(len(res))

    # Sentence type? Declarative, imperative, interrogative, or exclamatory.
    # This will most liekly change many times...
    #
    # Let's start with super simple sentences...
    #
#    for w in res:
#        print(w)
#        
#        if w[0] == 'VP':
#            vpLen = len(w)
#            action = w[vpLen - 1]
#            actions.append(action)
#            print(action)
#            # Can I (Simp) do any of these actions?
#            if action not in sd:
#                print('I cannot: ' + str(action))
#
#        # Looking for object
#        if w[0] == 'NP':
#            npLen = len(w)
#            subject = w[npLen - 1]
#            subjects.append(subject)
#            print(subject)
#
#            subjectData = getNx(subject)
#
#            print(subjectData[len(subjectData)- 1])
#
#    print('---')
#    print(actions)
#    print(subjects)
#
#    print('---')
#    print(type(tl))
#    print(len(tl))
    for i in tl:
        print('>>' + str(i) + '<<')

    print('---')


    if len(tl) < 1:
        print('tl should never be less than 1')
    elif len(tl) == 1:
        # Simple sentence trees are just 1 line
        print('simple sentence')

        tStr = tl[0]

        tlIndex = 12 # Single line tree starting index

        # Does the sentence start with a VP or NP?
        if tStr[tlIndex] == 'V' and tStr[tlIndex + 1] == 'P':
            if tStr[tlIndex + 5] == 'V' and tStr[tlIndex + 6] == 'B':

                vb = ''
                sType = 'simple imperative starting with V'
                
                print('simple imperative sentence starting with VP -> VB')

                if tStr[tlIndex + 7] == ' ':
                    tlIndex = 20
                elif tStr[tlIndex + 7] in ['D', 'G', 'N', 'Z']:
                    tlIndex = 21
                
                while tStr[tlIndex] != ' ':                    
                    vb = vb + tStr[tlIndex]
                    tlIndex = tlIndex + 1
    
                sVerb = vb

                print('VP -> VB -> ' + vb)

                # Advance to next phrase (if one exists)
                if tStr[tlIndex + 3] == '[':

                    if tStr[tlIndex + 12] == ' ':
                        # NP NN
                        tlIndex = tlIndex + 13
                    else:
                        # NP NNP, NNS, etc
                        tlIndex = tlIndex + 14    
                    
                    nnx = ''

                    while tStr[tlIndex] != ' ':                    
                        nnx = nnx + tStr[tlIndex]
                        tlIndex = tlIndex + 1
                        nnxLen = len(nnx)

                    if (tStr[tlIndex - (nnxLen + 3)]) == 'D' and (tStr[tlIndex - (nnxLen + 2)]) == 'T':
                        # Found DT, so continue parsing sentence
                        dt = nnx
                        nnx = ''

                        if tStr[tlIndex + 7] in ['P', 'S']:
                            tlIndex = tlIndex + 9
                        else:
                            tlIndex = tlIndex + 8

                        while tStr[tlIndex] != ' ':                    
                            nnx = nnx + tStr[tlIndex]
                            tlIndex = tlIndex + 1
                    else:
                        dt = ''

                    if dt == '':
                        sSubj = nnx
                        print('NP -> nnx -> ' + nnx)
                    else:
                        sSubj = dt + ' ' + nnx
                        print('DT -> ' + dt + ' nnx -> ' + nnx)
                        
        # Does the sentence start with a NP?
        elif tStr[tlIndex] == 'N' and tStr[tlIndex + 1] == 'P':
            # NP -> NNx
            if tStr[tlIndex + 5] == 'N' and tStr[tlIndex + 6] == 'N':

                sType = 'simple declarative sentence strting with N'
                
                print('simple declarative sentence strting with NP -> NNx')

                if tStr[tlIndex + 7] == ' ':
                    tlIndex = 20
                elif tStr[tlIndex + 7] in ['P', 'S']:
                    tlIndex = 21

                nnx = ''
                
                while tStr[tlIndex] != ' ':                    
                    nnx = nnx + tStr[tlIndex]
                    tlIndex = tlIndex + 1

                sSubj = nnx
                print('NP -> nnx -> ' + nnx)

                # Advance to next phrase (if one exists)
                vp = ''
                
                if tStr[tlIndex + 3] == ']':

                    if tStr[tlIndex + 14] == ' ':
                        # NP VP
                        tlIndex = tlIndex + 15
                    else:
                        # NPx VP, VBD, VBG, etc
                        tlIndex = tlIndex + 16

                    while tStr[tlIndex] != ' ':                    
                        vp = vp + tStr[tlIndex]
                        tlIndex = tlIndex + 1
    
                sVerb = vp
                print('VP -> VBx -> ' + vp)

            elif tStr[tlIndex + 5] == 'D' and tStr[tlIndex + 6] == 'T':
            # NP -> DT

                sType = 'simple declarative sentence strting with NP -> DT -> NNx'
                print('simple declarative sentence strting with NP -> DT -> NNx')           
                print('found DT')

                dt = ''
                tlIndex = tlIndex + 8

                while tStr[tlIndex] != ' ':                    
                    dt = dt + tStr[tlIndex]
                    tlIndex = tlIndex + 1

                # Advance to next phrase
                nnx = ''
                
                if tStr[tlIndex + 7] == ' ':
                    tlIndex = 31
                elif tStr[tlIndex + 7] in ['P', 'S']:
                    tlIndex = 32
                
                while tStr[tlIndex] != ' ':                    
                    nnx = nnx + tStr[tlIndex]
                    tlIndex = tlIndex + 1

                sSubj = dt + ' ' + nnx
                print('NP -> DT -> ' + dt + ' nnx -> ' + nnx)

                # Advance to next phrase (if one exists)
                vp = ''

                if tStr[tlIndex + 3] == ']':

                    tlIndex = 49                    

                    if tStr[tlIndex] == ' ':
                        # NP VP
                        tlIndex = tlIndex + 1
                    else:
                        # NPx VP, VBD, VBG, etc
                        tlIndex = tlIndex + 2

                    while tStr[tlIndex] != ' ':                    
                        vp = vp + tStr[tlIndex]
                        tlIndex = tlIndex + 1

                    sVerb = vp
                    print('VP -> VBx -> ' + vp)
    else:
        # Multi-item trees:
        # EX:
        #\Tree [.S
        #        [.VP
        #          [.VB see ]
        #          [.NP [.NP [.NNP Mary ] ] [.VP [.VB walk ] ] ] ] ]
        #
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
