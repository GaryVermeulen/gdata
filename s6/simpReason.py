#
# simpReason.py
#

import simpConfig as sc
import simpStuff as ss
   


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
        
    sObj.sPOS = wData # Is this really needed?

    sTypLst = sObj.sType.split(',')

    if sTypLst[0] == 'declarative':
        if sc.verbose: print('   declarative response')
        # Does the verb(s) match the actions on the nouns?
        # First get the inflections
            
        verbs = sObj.sVerb.split(',')
        if sc.verbose: print('verbs: ', verbs)
        for v in verbs:
            vInflects.append(ss.getInflections(v, "VB"))

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

        # Can Simp do any of the verbs?
        simpCanDo, simpCannotDo = canSimpDo(sD, sObj.sVerb, wData)

        print('   simpCanDo:    ', simpCanDo)
        print('   simpCannotDo: ', simpCannotDo)

        # Can the NNP(s) perform any of the verbs?
        nnp_CanDo, nnp_CannotDo = nnpCanDo(sObj.sSubj, sObj.sVerb, wData)

        print('   nnp_CanDo: ', nnp_CanDo)
        print('   nnp_CannotDo: ', nnp_CannotDo)
            
    elif sTypLst[0] == 'interrogative':
        if sc.verbose: print('   interrogative response')
            
        if sObj.sSubj == '':
            rels.append(sObj.sObj + ',' + wData[2][3])
    else:
        print('   unkonwn senetence type')

    return rels
# End process_sObj()


################################################
# Process sPOS
#
def process_sPOS(s, sPOS, sD, inData):

    wData = []
    rel = None
    rels = []
    vInflects = []
    
    for w in s:
        for d in inData:
            if w == d[0]:
                wData.append(d)
    if sc.verbose: print('wData: ' + str(wData))

       
    # Do a basic NP vs VP check on first word
    # A sudo declarative vs imperative check
    if wData[0][1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        # Implies some kind of action, so can Simp do this action?
        print('   process_sPOS first word: ', wData[0][1])
        
    


    return rels
# End process_sPOS()


################################################
# canSimpDo - Can Simp perform any of the sentence verbs?
#
def canSimpDo(sD, sVerbs, wData):

    sentVerbLst = []
    can = []
    cannot = []

    simpVerbLst = sD[3].split(',')
    simpVerbSet = set(simpVerbLst)

    print('   simp verb list: ', simpVerbLst)
    print('   simp verb set:  ', simpVerbSet)

         
    for w in wData:
        print('   w: ', w)

        if w[-1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
            sentVerbLst.append(w[0])

    sentVerbSet = set(sentVerbLst)

    print('   sent verb list: ', sentVerbLst)
    print('   sent verb set:  ', sentVerbSet)

    intersectionSimpSent = simpVerbSet.intersection(sentVerbSet)

    print('   intersectionSimpSent: ', intersectionSimpSent)

    difference = sentVerbSet.difference(simpVerbSet)

    print('   difference: ', difference)

    can = list(intersectionSimpSent)
    cannot = list(difference)
            
    return can, cannot
# End  simpCanDo()


################################################
# nnpCanDo - Can NNP(s) perform any of the sentence verbs?
#
def nnpCanDo(sSubj, sVerb, wData):

    subjLst = []
    
    subjects = sSubj.split(',')

    for s in range(len(subjects)):
        print('subjects[{}]: {}'.format(s, subjects[s])) 
        if subjects[s] == 'NNP':
            print('subjects[{}]: {}'.format(s, subjects[s - 1]))
            subjLst.append(subjects[s - 1])

    print('   subjLst: ', subjLst)


    can = 'x'
    cannot = 'y'
    
    return can, cannot
# End  nnpCanDo()


