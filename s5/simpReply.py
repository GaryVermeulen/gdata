#
# simpReply.py
#

from simpStuff import getNx


def reply(sA, rel):
    print('simpReply...')


    if len(rel) <= 0:
        print('No relationships')
    else:
        print('Relationship(s) found:')
        print(rel)

    sTypeLst = sA.sType.split(',')
    
    if len(sTypeLst) > 1:
        if sTypeLst[0] == 'declarative':
            print('declarative')
            print(str(sTypeLst))
        elif sTypeLst[0] == 'interrogative':
            print('interrogative')
            print(str(sTypeLst))

            if sA.sSubj == '':
                nnpData = getNx('nnp', sA.sObj)
            else:
                nnpData = getNx('nnp', sA.sSubj)

            if sTypeLst[1] == 'what':
                if sA.sMD == 'can' and sA.sVerb == 'do':
                    print('{} {} {}: {}'.format(nnpData[0], sA.sMD, sA.sVerb, nnpData[3]))
                elif sA.sVerb == 'is':
                    print('{} {}: {}'.format(nnpData[0], sA.sVerb, nnpData[1], nnpData[2]))
                else:
                    print('This interrogative senetence is undiscernible:')
                    print(sA.inSent)
                    
        elif sTypeLst[0] == 'imperative':
            print('imperative')
            print(str(sTypeLst))
        elif sTypeLst[0] == 'exclamative':
            print('exclamative')
            print(str(sTypeLst))
        else:
            print('unkown sentence type')
            print(str(sTypeLst))
    else:
        print('This senetence is undiscernible')
        
            
    print('End simpReply')
    return
# End reply()
