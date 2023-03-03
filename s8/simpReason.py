#
# simpReason.py -- Attempt to emulate knowledge from linited data
#

import simpConfig as sc
import simpStuff as ss
   


################################################
# Search For Relationship(s) within the limited KB
#
def s4r(s, sObj, sPOS, sD, inData):
    
    rels = []
    
    print('==== s4r ====')

    if sObj.inSent == '':
        if sc.verbose:
            print('No or empty sentence object found')
            print(s)
            print(sPOS)
            print(sD)
            print('---')

        return ['s4r', 'ERROR', 'No or empty sentence object supplied'] 
    
    else:
        if sc.verbose:
            print(' Sentence object found for s:')
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
    
    
    print('--- s4r --- Calling process_sObj() ---')
    can, cannot = process_sObj(s, sObj, sD, inData)
    print('--- s4r --- process_sObj() returned:')
    print('can: ', can)
    print('cannot: ', cannot)
    print('--- End s4r ---')
    
    return can, cannot
# End s4r


################################################
# Process sObj
#
def process_sObj(s, sObj, sD, inData):

    wData = []
    rel = None
    canDo = []
    cannotDo = []
    vInflects = []

    justSubjects = []
    justObjects = []
    
    for w in s:
        for d in inData:
            if w == d[0]:
                wData.append(d)
    if sc.verbose: print('wData: ' + str(wData))
        

    sTypLst = sObj.sType.split(',') # More than one type? What was I thinking?

    if sTypLst[0] == 'declarative':
        if sc.verbose: print(' declarative response')
        # Does the verb(s) match the actions on the nouns?
        # First get the inflections
            
        verbs = sObj.sVerb.split(',')
        if sc.verbose: print('  verbs: ', verbs)
        for v in verbs:
            vInflects.append(ss.getInflections(v, "VB"))

        if sc.verbose: print('  vInflects: ', vInflects)

        subjects = sObj.sSubj.split(';')
        objects = sObj.sObj.split(';')

        print('  subjects: ', subjects)
        print('  objects: ', objects)
        
        if len(subjects) > 1:
            for s in subjects:
                tmp = s.split(',')
                justSubjects.append(tmp[0])
                    
        else:
            tmp = subjects[0].split(',')
            justSubjects.append(tmp[0])

        if len(objects) > 1:
            for o in objects:
                tmp = o.split(',')
                justObjects.append(tmp[0])
                    
        else:
            tmp = objects[0].split(',')
            justObjects.append(tmp[0])



        print('  justSubjects: ', justSubjects)
        print('  justObjects: ', justObjects)



        for w in wData:
#            print(' ---')
#            if sc.verbose: print('   w: ', w)
#            if sc.verbose: print('   w[0]: ', w[0])

                
                
            if w[0] in justSubjects:

#                print(' checking subjects...')
                
                actions = set(w[3].split(','))
#                print('   actions: ', actions)
                    
                for v in vInflects:
                    v = v.split(',')
                    inflect = set(v)
                    inflect.intersection_update(actions)

                if len(inflect) == 0:
                    
                    cannotDo.append(w[0] + ',' + str(vInflects))
                    if sc.verbose: print(str(w[0]) + ' cannot ' + str(vInflects))
                else:
                    rel = inflect.pop()
                    canDo.append(w[0] + ',' + rel)
                    if sc.verbose: print(str(w[0]) + ' can ' + rel)
            elif w[0] in justObjects:

#                print(' checking objects...')

                actions = set(w[3].split(','))
#                print('   actions: ', actions)
                    
                for v in vInflects:
                    v = v.split(',')
                    inflect = set(v)
                    inflect.intersection_update(actions)

                if len(inflect) == 0:
                    
                    cannotDo.append(w[0] + ',' + str(vInflects))
                    if sc.verbose: print(str(w[0]) + ' cannot ' + str(vInflects))
                else:
                    rel = inflect.pop()
                    canDo.append(w[0] + ',' + rel)
                    if sc.verbose: print(str(w[0]) + ' can ' + rel)


            
    elif sTypLst[0] == 'imperative':
        if sc.verbose: print('   imperative response')

        # Can Simp do any of the verbs?
        simpCanDo, simpCannotDo = canSimpDo(sD, sObj.sVerb, wData)

        print('   simpCanDo:    ', simpCanDo)
        print('   simpCannotDo: ', simpCannotDo)

        # Can the sentence subject(s) perform any of the verbs?
        sub_CanDo, sub_CannotDo = subCanDo(sObj.sSubj, sObj.sVerb, wData)

        print('   sub_CanDo: ', sub_CanDo)
        print('   sub_CannotDo: ', sub_CannotDo)

        # Can the sentence object(s) perform any of the verbs?
        obj_CanDo, obj_CannotDo = objCanDo(sObj.sObj, sObj.sVerb, wData)

        print('   obj_CanDo: ', obj_CanDo)
        print('   obj_CannotDo: ', obj_CannotDo)


    elif sTypLst[0] == 'interrogative':
        if sc.verbose: print('   interrogative response')

        print("   Under construction")   
        #if sObj.sSubj == '':
        #    rels.append(sObj.sObj + ',' + wData[2][3])
    else:
        print('   unkonwn senetence type')

    return canDo, cannotDo
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
# subCanDo - Can sentence subject(s) perform any of the sentence verbs?
#
def subCanDo(sSubj, sVerb, wData):

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


################################################
# objCanDo - Can sentence object(s) perform any of the sentence verbs?
#
def objCanDo(sObj, sVerb, wData):

    objLst = []
    
    objects = sObj.split(',')

    for o in range(len(objects)):
        print('objects[{}]: {}'.format(o, objects[o])) 
        if objects[o] == ['NN', 'NNS']:
            print('objects[{}]: {}'.format(s, objects[o - 1]))
            objLst.append(objects[o - 1])

    print('   objLst: ', objLst)


    can = 'x'
    cannot = 'y'
    
    return can, cannot
# End  objCanDo()

