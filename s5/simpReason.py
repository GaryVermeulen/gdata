#
# simpReason.py
#

import simpConfig as sc


################################################
# Search For Relationship(s) within the limited KB
#
def s4r(s, sObj, sPOS, sD, inData):
    
    rels = []
    no_sObj = True
    no_sPOS = True
    
    
    print('--- s4r ---')

    if sObj.inSent == '':
        if sc.verbose:
            print('no sent obj found')
            print(s)
            print(sPOS)
            print(sD)
            print('---')
    else:
        no_sObj = False
    
    if len(sPOS) == 0:
        if sc.verbose:
            print('no sPOS found')
            print(s)
            print('    inSent: ', sObj.inSent)
            print('    sPOS  : ', sObj.sPOS)
            print('    sType : ', sObj.sType)
            print('    sSubj : ', sObj.sSubj)
            print('    sObj  : ', sObj.sObj)
            print('    sVerb : ', sObj.sVerb)
            print('    sDet  : ', sObj.sDet)
            print('    sIN   : ', sObj.sIN)
            print('    sPP   : ', sObj.sPP)
            print('    sMD   : ', sObj.sMD)
            print(sD)
    else:
        no_sPOS = False

    if no_sObj and no_sPOS:
        rels.append('--- s4r --- No sObj and No sPOS ---')
        print(rels)
        return rels

    if no_sObj:
        print('--- s4r --- Calling process_sPOS() ---')
        rels = process_sPOS(s, sPOS, sD, inData)
        print('--- s4r --- process_sPOS() returned:') 
        print(rels)
        return rels

    if no_sPOS:
        print('--- s4r --- Calling process_sObj() ---')
        rels = process_sObj(s, sObj, sD, inData)
        print('--- s4r --- process_sObj() returned:')
        print(rels)
        return rels

    if sc.verbose: print('   Technically should not get here, rels: ', str(rels))
        
    print('--- End s4r ---')
    return rels
# End s4r


################################################
# Process sObj
#
def process_sObj(s, sObj, sD, inData):

    wData = []
    rel = None
    rels = []
    vInflects = []
    
    for w in s:
        for d in inData:
            if w == d[0]:
                wData.append(d)
    if sc.verbose: print('wData: ' + str(wData))
        
    sObj.sPOS = wData

    sTypLst = sObj.sType.split(',')

    if sTypLst[0] == 'declarative':
        if sc.verbose: print('   declarative response')
        # Does the verb(s) match the actions on the nouns?
        # First get the inflections
            
        verbs = sObj.sVerb.split(',')
        if sc.verbose: print('verbs: ', verbs)
        for v in verbs:
            vInflects.append(getInflections(v, "VB"))

        if sc.verbose: print('vInflects: ', vInflects)

        subjects = sObj.sSubj.split(',')

        for w in wData:
            if w[0] in subjects:
                if sc.verbose: print('w: ', w)

                actions = set(w[3].split(','))
                    
                for v in vInflects:
                    v = v.split(',')
                    inflect = set(v)
                    inflect.intersection_update(actions)

                if len(inflect) == 0:
                    if sc.verbose: print(str(w[0]) + ' cannot ' + str(v))
                    rel = None
                else:
                    rel = inflect.pop()
                    rels.append(w[0] + ',' + rel)
                    if sc.verbose: print(str(w[0]) + ' can ' + rel)
            
    elif sTypLst[0] == 'imperative':
        if sc.verbose: print('   imperative response')

        sD_verbLst = sD[3].split(',')

        print('   simp verb list: ', sD_verbLst)

        sD_verbSet = set(sD_verbLst)

        if len(sObj.sSubj.split(',')) < 3:
            sSubj = sObj.sSubj.split(',')

            print('len wData: ', len(wData))
            print(wData)
            print('sSubj: ', sSubj)
            print('-------')
                
            for i in wData:
                print('   i: ', i)
                
                if i[0][0] == sSubj[0][0]:
                    sSubj_verbLst = i[3].split(',')
                    sSubj_verbSet = set(sSubj_verbLst)

                    print('sSubj_verbSet: ', sSubj_verbSet)

                    sD_intersec = sD_verbSet.intersection(sSubj_verbSet)

                    print('sD_intersec: ', sD_intersec)

                    diff = sSubj_verbSet.difference(sD_verbSet)
                    diff = sD_verbSet.difference(sSubj_verbSet)
                        
                    print('   diff:' , diff)

                    sO_u = sSubj_verbSet.union(sD_verbSet)
                    print('union: ', sO_u)

                    sVerbSet = set(sObj.sVerb.split(','))

                    print('sVerbSet: ', sVerbSet)

                    sVerbx = sVerbSet.intersection(sSubj_verbSet)

                    print('sVerbx: ' , sVerbx)
                        
                    break     
        else:
            print('bummer')

        print('wtf')
            
    elif sTypLst[0] == 'interrogative':
        if sc.verbose: print('   interrogative response')
            
        if sObj.sSubj == '':
            rels.append(sObj.sObj + ',' + wData[2][3])
    else:
        print('   unkonwn senetence type')

    return rels
# End process_sObj()



def process_sPOS(s, sPOS, sD, inData):

    rels = []

    rels.append(' --- s4r --- process_sPOS() stub ---')

    print(rels)

    return rels
# End process_sPOS()

