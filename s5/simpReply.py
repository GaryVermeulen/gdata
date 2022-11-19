#
# simpReply.py
#

from simpStuff import getNx
import simpConfig as sc 


def reply(sA, rel, sD):
    print('simpReply...')

    if sc.verbose:
        print(type(sA))
        print('--- sA:')
        print('    inSent: ', sA.inSent)
        print('    sPOS  : ', sA.sPOS)
        print('    sType : ', sA.sType)
        print('    sSubj : ', sA.sSubj)
        print('    sObj  : ', sA.sObj)
        print('    sVerb : ', sA.sVerb)
        print('    sDet  : ', sA.sDet)
        print('    sIN   : ', sA.sIN)
        print('    sPP   : ', sA.sPP)
        print('    sMD   : ', sA.sMD)
        print('--- end sA')
        print('--- sD    : ', sD)

    if sc.verbose: 
        if len(rel) <= 0:
            print(' No relationships')
        else:
            print(' Relationship(s) found:')
            print(rel)

    sTypeLst = sA.sType.split(',')

    if sc.verbose: 
        print(' sTypeLst: ', sTypeLst)
        print(' len sTypeLst: ', len(sTypeLst))
        print(' sPOS: ' , sA.sPOS)
        print(' -' * 5)
    
    if len(sTypeLst) >= 1:
        if sTypeLst[0] == 'declarative':
            declarativeReply(sTypeLst, sA, sD)
                
        elif sTypeLst[0] == 'interrogative':
            interrogativeReply(sTypeLst, sA, sD)
                    
        elif sTypeLst[0] == 'imperative':
            imperativeReply(sTypeLst, sA, sD)
            
        elif sTypeLst[0] == 'exclamative':
            exclamativeReply(sTypeLst, sA, sD)
            
        else:
            print(' unkown sentence type')
            print(str(sTypeLst))
    else:
        print(' This senetence is grammatically undiscernible')
        print(str(sTypeLst))
            
    print('End simpReply')
    return
# End reply()

#
# declarativeReply
#
def declarativeReply(sTypeLst, sA, sD):

    if sc.verbose:
        print(' declarative')
        print(str(sTypeLst))

    return
# End declarativeReply


#
# interrogativeReply
#
def interrogativeReply(sTypeLst, sA, sD):

    o = sA.sObj.split(',')
    s = sA.sSubj.split(',')

    if sc.verbose: 
        print(' interrogative')
        print('sA.sObj: ', sA.sObj)
        print('sA.sSubj: ', sA.sSubj)
        print('sTypeLst:', str(sTypeLst))
        print('o: ', o)
        print('s: ', s)

    if sA.sSubj == '' and sA.sObj == '':
        print('subject and object cannot be blank')
        return
    elif sA.sSubj == '':
        if o[1] == 'NNP':
            nnpData = getNx('nnp', o[0])
        elif o[1] =='NN':
            nnpData = getNx('nn', o[0])
        else:
            print(' POS Error: ', o)
    else:
        if s[1] == 'NNP':
            nnpData = getNx('nnp', s[0])
        elif s[1] =='NN':
            nnpData = getNx('nn', s[0])
        else:
            print(' POS Error: ', s)

    if sc.verbose: print(' nnpData: ', nnpData)

    if sTypeLst[1] == 'what':
        if sA.sMD == 'can' and sA.sVerb == 'do':
            print(' can and do: {} {} {}: {}'.format(nnpData[0], sA.sMD, sA.sVerb, nnpData[3]))
        elif sA.sVerb == 'is':
            if sA.sDet == '':
                print(' is: {} {}: {} and a {}'.format(nnpData[0], sA.sVerb, isA(nnpData[1]), nnpData[2]))
            else:
                print(' is: {} {} {}: {} and a {}'.format(nnpData[0], sA.sVerb, sA.sDet, isA(nnpData[1]), nnpData[2]))
        else:
            print(' This interrogative senetence is undiscernible:')
            print(sA.inSent)
    elif sTypeLst[1] == 'where':
        print('At this point in time I have no idea where anything is!')



    
    return
# End interrogativeReply


#
# imperativeReply
#
def imperativeReply(sTypeLst, sA, sD):

    if sc.verbose: 
        print(' imperative')
        print(' sTypeLst: ', sTypeLst)
        print(' sPOS: ', sA.sPOS)
        print(' sD: ', sD)
            
    if sA.sPOS[0][1] in ['VB']:
        sDVerbs = sD[3].split(',')
        if sA.sPOS[0][0] not in sDVerbs:
            sSubjLst = sA.sSubj.split(',')
                    
            print(' {} cannot {} {}'.format(sD[0], sA.sPOS[0][0], sSubjLst[0]))

    return
# End imperativeReply


#
# exclamativeReply
#
def exclamativeReply(sTypeLst, sA):

    if sc.verbose: 
        print(' exclamative')
        print(str(sTypeLst))

    return
# End exclamativeeply


#
# isA
#
def isA(x):

    if sc.verbose: 
        print(' isA')
        print(x)

    if x == 'P':
        r = 'Person'
    elif x == 'p':
        r = 'Place'
    elif x == 't':
        r = 'Thing'
    else:
        r = 'Unkonown'

    return r
# End exclamativeeply


