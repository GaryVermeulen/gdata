#
# pickleChecker.py
#

import pickle
from simpConfig import FANBOYS
from simpConfig import Node
from simpConfig import N_ary_Tree
from simpConfig import NodeNotFoundException


def getPickles():

    """
    # untaggedCorpusSents
    # List of Lists...
    # 275
    # <class 'list'>
    # ['see', 'bob']
    # ['see', 'bob', 'run']
    # ['mary', 'saw', 'pookie', 'in', 'the', 'park', 'with', 'a', 'telescope']
    # ...
    # NOTE: May contain nonsensical or partial/incomplete sentances
    # ['use', 'caution', 'inbetween']
    # ['but', 'once', 'it', 'was', 'on']
    # ['oh']
    #
    with open('pickles/untaggedCorpusSents.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded untaggedCorpusSents.pkl')
    fp.close()
    """
    """
    # taggedCorpusSents
    # List of lists containing tuples...
    # 275
    # <class 'list'>
    # [('see', 'VB'), ('bob', 'NNP')]
    # [('see', 'VB'), ('bob', 'NNP'), ('run', 'VB')]
    # [('mary', 'NNP'), ('saw', 'VBD'), ('pookie', 'NNP'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('with', 'IN'), ('a', 'DT'), ('telescope', 'NN')]
    # ...
    # NOTE: May contain nonsensical or partial/incomplete sentances
    # [('use', 'VB'), ('caution', 'NN'), ('inbetween', 'JJ')]
    # [('but', 'CC'), ('once', 'IN'), ('it', 'PRP'), ('was', 'VBD'), ('on', 'IN')]
    # [('oh', 'UH')]
    #
    with open('pickles/taggedCorpusSents.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded taggedCorpusSents.pkl')
    fp.close()
    """
    
    # taggedBoW
    # List of tuples...
    # 715
    # <class 'list'>
    # ('my', 'PRP$')
    # ('name', 'NN')
    # ('is', 'VBZ')
    # ('allie', 'NNP')
    # ('kay', 'NNP')
    # ('and', 'CC')
    #
    with open('pickles/taggedBoW.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded taggedBoW.pkl')
    fp.close()
    
    """
    # Inflections:
    # List of lists...
    # 112505
    # <class 'list'>
    # ['acadia', 'n', 'acadias', 'acadiae']
    # ['acadian', 'n', 'acadians']
    # ['acalepha', 'n', 'acalephae']
    # ['acalypha', 'n', 'acalyphas', 'acalyphae']
    # ...
    # ['zoom', 'n', 'zooms']
    # ['zoom', 'v', 'zoomed', 'zooming', 'zooms']
    # ...
    # ['zymosis', 'n', 'zymoses']
    # ['zymotechnic', 'n', 'zymotechnics']
    # ['zymotic', 'a', 'zymoticer', 'zymoticcer', 'zymoticest', 'zymoticcest']
    # ['zymurgy', 'n', 'zymurgies']
    # ['zyzzyva', 'n', 'zyzzyvas']
    #
    with open('pickles/inflections.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded inflections.pkl')
    fp.close()
    """
    """
    # kbDict
    # List of dictionaries...
    # 31
    # <class 'list'>
    # {'name': 'instrument', 'ppt': 't', 'tag': 'NN', 'canDo': 'TBD', 'superclass': 'thing'}
    # {'name': 'recreation_ground', 'ppt': 'p', 'tag': 'NN', 'canDo': 'TBD', 'superclass': 'thing'}
    #{'name': 'animal', 'ppt': 't', 'tag': 'NN', 'canDo': 'see,eat,walk,run', 'superclass': 'thing'}
    # ...
    #
    # {'name': 'man', 'ppt': 't', 'tag': 'NN', 'canDo': 'see,eat,walk,run', 'superclass': 'human'}
    # {'name': 'cat', 'ppt': 't', 'tag': 'NN', 'canDo': 'see,eat,walk,run', 'superclass': 'feline'}
    # {'name': 'dog', 'ppt': 't', 'tag': 'NN', 'canDo': 'see,eat,walk,run', 'superclass': 'canine'}
    # {'name': 'park', 'ppt': 'p', 'tag': 'NN', 'canDo': 'recreation', 'superclass': 'recreation_ground'}
    # {'name': 'playground', 'ppt': 't', 'tag': 'NN', 'canDo': 'play', 'superclass': 'park'}
    # {'name': 'duck', 'ppt': 't', 'tag': 'NN', 'canDo': 'see,eat,walk,run,fly', 'superclass': 'bird'}
    # ...
    #{'name': 'sam', 'ppt': 'P', 'tag': 'NNP', 'canDo': 'see,eat,walk,run', 'superclass': 'man'}
    #{'name': 'pookie', 'ppt': 't', 'tag': 'NNP', 'canDo': 'see,eat,walk,run', 'superclass': 'cat'}
    #{'name': 'daffy', 'ppt': 't', 'tag': 'NNP', 'canDo': 'see,eat,walk,run,fly', 'superclass': 'duck'}
    #
    with open('pickles/kbDict.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded kbDict.pkl')
    fp.close()
    """
    """
    # N_arry_Tree
    #
    with open('pickles/kbTree.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded kbTree.pkl')
    fp.close()
    """

    
    
    """
    # List of tuples...
    #152
    #<class 'list'>
    #('animal', 'NN')
    #('instrument', 'NN')
    #('simp', 'NNP')
    #
    with open('pickles/starterDictList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded startedDictList.pkl')
    fp.close()
    """

    """
    # List of lists...
    #246
    #<class 'list'>
    #['i', 'will', 'do', 'my', 'homework', 'right', 'now', 'mom']
    #['i', 'said']
    #['oh']
    #['i', 'just', 'could', 'not', 'wait']
    #
    with open('pickles/newCorpus.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newCorpus.pkl')
    fp.close()
    """
    
    """
    # List of tuples from corpus...
    #724
    #<class 'list'>
    #('however', 'RB')
    #('before', 'IN')
    #('i', 'PRP')
    #('can', 'MD')
    #
    with open('pickles/newTaggedList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()
    """

    """
    653
    <class 'dict'>
    key:  however
    val:  [[['however'], ['RB'], []], [['however'], ['conjunction'], [], [':', 'in', 'whatever', 'manner', 'or', 'way', 'that']], [['however'], ['conjunction'], [], [':', 'although']], [['however'], ['adverb'], [], [':', 'in', 'whatever', 'manner', 'or', 'way']], [['however'], ['adverb'], [], [':', 'to', 'whatever', 'degree', 'or', 'extent']], [['however'], ['adverb'], [], [':', 'in', 'spite', 'of', 'that', ':', 'on', 'the', 'other', 'hand']], [['however'], ['adverb'], [], [':', 'how', 'in', 'the', 'world']]]
    ---
    [['however'], ['RB'], []]
    [['however'], ['conjunction'], [], [':', 'in', 'whatever', 'manner', 'or', 'way', 'that']]
    [['however'], ['conjunction'], [], [':', 'although']]
    [['however'], ['adverb'], [], [':', 'in', 'whatever', 'manner', 'or', 'way']]
    [['however'], ['adverb'], [], [':', 'to', 'whatever', 'degree', 'or', 'extent']]
    [['however'], ['adverb'], [], [':', 'in', 'spite', 'of', 'that', ':', 'on', 'the', 'other', 'hand']]
    [['however'], ['adverb'], [], [':', 'how', 'in', 'the', 'world']]
    ----------
    key:  before
    val:  [[['before'], ['IN'], []], [['before'], ['adverb'], [], [':', 'in', 'advance', ':', 'ahead']], [['before'], ['adverb'], [], [':', 'at', 'an', 'earlier', 'time']], [['before'], ['preposition'], [], [':', 'forward', 'of', ':', 'in', 'front', 'of']], [['before'], ['preposition'], [], [':', 'in', 'the', 'presence', 'of']], [['before'], ['preposition'], [], [':', 'under', 'the', 'jurisdiction', 'or', 'consideration', 'of']], [['before'], ['preposition'], [], [':', 'at', 'the', 'disposal', 'of']], [['before'], ['preposition'], [], [':', 'in', 'store', 'for']], [['before'], ['preposition'], [], [':', 'preceding', 'in', 'time', ':', 'earlier', 'than']], [['before'], ['preposition'], [], [':', 'in', 'a', 'higher', 'or', 'more', 'important', 'position', 'than']], [['before'], ['conjunction'], [], [':', 'earlier', 'than', 'the', 'time', 'that']], [['before'], ['conjunction'], [], [':', 'sooner', 'or', 'quicker', 'than']], [['before'], ['conjunction'], [], [':', 'so', 'that', '…', 'do', 'not']], [['before'], ['conjunction'], [], [':', 'until', 'the', 'time', 'that']], [['before'], ['conjunction'], [], [':', 'or', 'else', '…', 'not']], [['before'], ['conjunction'], [], [':', 'or', 'else']], [['before'], ['conjunction'], [], [':', 'rather', 'or', 'sooner', 'than']]]
    ---
    [['before'], ['IN'], []]
    [['before'], ['adverb'], [], [':', 'in', 'advance', ':', 'ahead']]
    [['before'], ['adverb'], [], [':', 'at', 'an', 'earlier', 'time']]
    [['before'], ['preposition'], [], [':', 'forward', 'of', ':', 'in', 'front', 'of']]
    [['before'], ['preposition'], [], [':', 'in', 'the', 'presence', 'of']]
    [['before'], ['preposition'], [], [':', 'under', 'the', 'jurisdiction', 'or', 'consideration', 'of']]
    [['before'], ['preposition'], [], [':', 'at', 'the', 'disposal', 'of']]
    [['before'], ['preposition'], [], [':', 'in', 'store', 'for']]
    [['before'], ['preposition'], [], [':', 'preceding', 'in', 'time', ':', 'earlier', 'than']]
    [['before'], ['preposition'], [], [':', 'in', 'a', 'higher', 'or', 'more', 'important', 'position', 'than']]
    [['before'], ['conjunction'], [], [':', 'earlier', 'than', 'the', 'time', 'that']]
    [['before'], ['conjunction'], [], [':', 'sooner', 'or', 'quicker', 'than']]
    [['before'], ['conjunction'], [], [':', 'so', 'that', '…', 'do', 'not']]
    [['before'], ['conjunction'], [], [':', 'until', 'the', 'time', 'that']]
    [['before'], ['conjunction'], [], [':', 'or', 'else', '…', 'not']]
    [['before'], ['conjunction'], [], [':', 'or', 'else']]
    [['before'], ['conjunction'], [], [':', 'rather', 'or', 'sooner', 'than']]
    """
    """
    with open('pickles/mainDictionary.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded mainDictionary.pkl')
    fp.close()
    """
    
    return ourPickle
    

def fixPickle(ourPickle):

    betterPickle = []

    print('Before fix: ', len(ourPickle))

    # Correct CC to only FANBOYS
    for p in ourPickle:
        if p[1] == 'CC':
            if p[0] in FANBOYS:
                tmpToken = (p[0], p[1])
                betterPickle.append(tmpToken)
        else:
            betterPickle.append(p)
                
    print('After fix: ', len(betterPickle))

    return betterPickle


def savePickle(p):

    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()
    


if __name__ == "__main__":

    limit = 1

    print('Pickle checker...')
    
    ourPickle = getPickles()

    print('ourPickle:')
    print(len(ourPickle))
    print(type(ourPickle))
#    print(ourPickle.print_tree(ourPickle.root, ''))

#    print(ourPickle)
    """
    for p in ourPickle:
        print(len(p))
        print(type(p))
        print(p)
        print(p.keys())
        print(p.values())
    """
    """
    # list the 1st 100 entries
    for p in ourPickle:
        if limit > 100:
            break
        print(p)
        limit += 1
    
    """
    # Checking for a word
    cnt = 1
    for p in ourPickle:
        if p[0] == 'hammy':
            print(p)
    """ 
        # fun can be noun, adjective, or verb -- OUCH!
        # run can be noun or verb -- OUCH!
        #
        if 'run' in p:
            print(p)


        print("{}, {}".format(cnt, p))
        cnt += 1
    """
    """
    cnt = 1
    for w, d in ourPickle.items():
        #if limit > 100:
        #    break
        print(cnt)
        print('key: ', w)
        print('val: ',d)
        print('---')
        for v in d:
            print(v)
        print('-' * 10)
        cnt += 1
    """
    """
        if p[0] == 'not' or p[0] == 'fast':
            print('not | fast: ', p)
        if p[1] == 'CC':
            print('CC: ', p)
            
    bP = fixPickle(ourPickle)

    for p in bP:
        if p[0] == 'not' or p[0] == 'fast':
            print('not | fast: ', p)
        if p[1] == 'CC':
            print('CC: ', p)
    
#    savePickle(bP)

#    print('-' * 5)
    
    print('newDict:')
    print(len(newDict))
    print(type(newDict))
    print(newDict.get("eat_1"))
    print(newDict.get("do_1"))
    
    
    # Temp fix for the hammy problem
    newList = []
    for p in ourPickle:
        #print(p)
        if p[0] == 'hammy':
            print('org found: {} at p[0]: {}'.format(p, p[0]))
            if p[1] != 'NNP':
                newList.append((p[0],'NNP'))
            else:
                newList.appned(p)
        else:
            newList.append(p)
    
    for n in newList:
        if n[0] == 'hammy':
            print('new found: {} at n[0]: {}'.format(n, n[0]))

    # Save modified pickle...
    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(newList, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()
    
    
    cnt = 1
    testWord = 'pookie'
    print('looking for: ', testWord)
    for p in ourPickle:
        if testWord in p:
            print('found {} at {} {}'.format(testWord, cnt, p))
        cnt += 1 
    """
    """
    # Checking inflections...
#    print(ourPickle[2000:2020:]) # Just look at some

    mySlice = ourPickle[2000:2200:]
    cnt = 2000
    for s in mySlice:
        print('{}, {}'.format(cnt, s))
        cnt += 1
    """
    """
    testWord = 'saw' # 'run'
    cnt = 1
    for line in ourPickle:
        if testWord in line:
            print('found {} at {} {}'.format(testWord, cnt, line))
            if line[1] == 'v': # incorrect tag 
                print('found v {} at {} {}'.format(testWord, cnt, line))

        cnt += 1
    """

    """    
    # newTaggedList
    print(ourPickle[0:60:]) # Just look at some
    testWord = 'saw' # 'run'
    cnt = 1
    for line in ourPickle:
#        print(line)
#        print(line[0])
#        print(line[1])
        if testWord in line[0]:
            print('found {} at {} {}'.format(testWord, cnt, line))
#            if line[1] == 'v': # correct tag VB, VBD, etc.
#                print('found v {} at {} {}'.format(testWord, cnt, line))

        cnt += 1
    
    """
    
