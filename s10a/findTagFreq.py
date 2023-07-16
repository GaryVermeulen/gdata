#
# findTagFreq.py
#

import pickle
from simpConfig import FANBOYS
from simpConfig import Node
from simpConfig import N_ary_Tree
from simpConfig import NodeNotFoundException


def getPickle():

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
    
    return ourPickle
    

def savePickle(p):

    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()


def addArr(tagFreqArr, s):

    print('start addArr', )
    print(s)
    if len(tagFreqArr) == 0:
        print('first add s: ', s)
        tagFreqArr.append(((s, 1)))
        
    else:
        print('else add s:', s)
        for i in tagFreqArr:
            print('i: ', i)
            if s in i[0]:
                cnt = i[1] + 1
                i[1] = cnt
            
            else:
                print('new else add s:', s)
                tagFreqArr.append(((s, 1)))
            
    
    return tagFreqArr

if __name__ == "__main__":

    print('--- start findTagFrreq ---')

    tagFreqArr = []
    
    ourPickle = getPickle()

    print('ourPickle:')
    print(len(ourPickle))
    print(type(ourPickle))
    
    # Extract tags
    tags = []
    for s in ourPickle:
        tmp = []
        for w in s:
            tmp.append(w[1])
        tags.append(tmp)

    print('tags:')
    print(len(tags))
    print(type(tags))

    # tagFreq: <list>
    # (['NNP', 'MD', 'VB'], count)
    #
    for s in tags:
        tagFreqArr = addArr(tagFreqArr, s)
    
    print('\ntagFreqArr:')
    print(len(tagFreqArr))
    print(type(tagFreqArr))

