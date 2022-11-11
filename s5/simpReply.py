#
# simpReply.py
#

from simpStuff import getNx


def reply(sA, rel, sD):
    print('simpReply...')


    if len(rel) <= 0:
        print(' No relationships')
    else:
        print(' Relationship(s) found:')
        print(rel)

    sTypeLst = sA.sType.split(',')

    print(' sTypeLst: ', sTypeLst)
    print(' len sTypeLst: ', len(sTypeLst))
    print(' sPOS: ' , sA.sPOS)
    print(' -' * 5)
    
    if len(sTypeLst) >= 1:
        if sTypeLst[0] == 'declarative':
            print(' declarative')
            print(str(sTypeLst))
        elif sTypeLst[0] == 'interrogative':
            print(' interrogative')
            print(str(sTypeLst))

            if sA.sSubj == '':
                n = sA.sObj.split(',')
                if n[1] == 'NNP':
                    nnpData = getNx('nnp', n[0])
                elif n[1] =='NN':
                    nnpData = getNx('nn', n[0])
                else:
                    print(' POS Error: ', n)
            else:
                n = sA.sObj.split(',')
                if n[1] == 'NNP':
                    nnpData = getNx('nnp', n[0])
                elif n[1] =='NN':
                    nnpData = getNx('nn', n[0])
                else:
                    print(' POS Error: ', n)

            print(' nnpData: ', nnpData)

            if sTypeLst[1] == 'what':
                if sA.sMD == 'can' and sA.sVerb == 'do':
                    print(' can and do: {} {} {}: {}'.format(nnpData[0], sA.sMD, sA.sVerb, nnpData[3]))
                elif sA.sVerb == 'is':
                    print(' is: {} {}: {}'.format(nnpData[0], sA.sVerb, nnpData[1], nnpData[2]))
                else:
                    print(' This interrogative senetence is undiscernible:')
                    print(sA.inSent)
                    
        elif sTypeLst[0] == 'imperative':
            print(' imperative')
            print(' sTypeLst: ', sTypeLst)
            print(' sPOS: ', sA.sPOS)
            print(' sD: ', sD)
            
            if sA.sPOS[0][1] in ['VB']:
                sDVerbs = sD[3].split(',')
                if sA.sPOS[0][0] not in sDVerbs:
                    sSubjLst = sA.sSubj.split(',')
                    
                    print(' {} cannot {} {}'.format(sD[0], sA.sPOS[0][0], sSubjLst[0]))
            
        elif sTypeLst[0] == 'exclamative':
            print(' exclamative')
            print(str(sTypeLst))
        else:
            print(' unkown sentence type')
            print(str(sTypeLst))
    else:
        print(' This senetence is grammatically undiscernible')
        
            
    print('End simpReply')
    return
# End reply()
