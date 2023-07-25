#
# commonUtils.py
#

import os

import pickle
from simpConfig import *



def listDepth(lst):

    d = 0

    for item in lst:
        if isinstance(item, list):
            d = max(listDepth(item), d)

    return d + 1


def scrapeWeb(word):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup

    print("Starting scrape for: ", word)

    req = Request(
            url = "https://www.collinsdictionary.com/us/dictionary/english/" + word.strip() + "",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

    try:
        htmlFile = urlopen(req).read()
        found = True
    except:
        notFound.append(word)
        found = False
          
    soup = BeautifulSoup(htmlFile, 'html.parser')

    soup1 = soup.find("script")
    """
    try:
        soup1 = soup1.get_text()
        found = True
    except AttributeError:
        found = False
    """     

    print('soup1: ', soup1)

    return 'dum', 'my'


def chkUnkownWords(wordsNotFound):
    from urllib.request import Request, urlopen
    from bs4 import BeautifulSoup

    newWords = []
    notFound = []
	
    print("Starting scrape for {} words".format(len(wordsNotFound)))
    for word in wordsNotFound:
        print('.', end='')

        req = Request(
            url = "http://www.dictionary.com/browse/" + word.strip() + "",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        try:
            htmlFile = urlopen(req).read()
            found = True
        except:
            notFound.append(word)
            found = False
            continue
          
        soup = BeautifulSoup(htmlFile, 'html.parser')
        soup1 = soup.find("meta", attrs={'name':'description'})

        try:
            soup1 = soup1.get_text()
            found = True
        except AttributeError:
            found = False
            continue
        if found:            
            soup2 = soup.find(class_="luna-pos")
            txt = soup2.get_text()
            pos = os.linesep.join([s for s in txt.splitlines() if s])
            pos = pos.replace(',', '')

            soup3 = soup.find("meta", attrs={'name':'description'})                        
            txt3 = str(soup3)
            txt4 = removeHTML(txt3) # Soup get_text not working or I can't figure it our :-(

        newWords.append(word + ';' + pos + ';' + txt4)
	
    print("\nScraping Completed.")

    return newWords, notFound


def removeHTML(txt):

    txt = txt.replace('<meta content="', '') # Start of htmp string
    txt = txt.replace('See additional meanings and similar words.', '')
    txt = txt.replace('See more.', '')
    txt = txt.replace('" name="description"/>', '')

    return txt


def newWordTag(w, newWords):
    # Crude tagger

    tag = 'UNK'

    for newWord in newWords:
        newWordLst = newWord.split(';')
        print('w: ', w.strip())
        print('newWordLst:')
        print(newWordLst)
        print('newWordLst[0]: ', newWordLst[0].strip())
        if w == newWordLst[0]:
            print('1st if')
            if newWordLst[1].strip() == 'noun':
                tag = nn
            elif newWordLst[1].strip() == 'verb':
                tag = vb
            else:
                print('else')

    return tag


def getInflectionTag(tag):

    if tag in [vb, vbd, vbg, vbn, vbp, vbz]:
        return 'v'
    elif tag in [nn, nnp, nns]:
        return 'n'
    elif tag in [jj, jjr, jjs]:
        return 'a'

    return 'x'


def getInflections(word, tag, baseWordSearch, allInflections):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag))

    if len(allInflections) == 0:
        allInflections = loadPickle('inflections')
    
    for line in allInflections:
        if word in line:
#            print('found {} at {} {}'.format(word, cnt, line))
#            print('tag: ', tag)
            if line[1] == tag:
#                print('found v {} with tag {} at {} {}'.format(word, tag, cnt, line))
                if baseWordSearch:
#                    print('base word match {} at {} {}'.format(word, cnt, line))
                    return line
                else: # Search inflections only
                    idx = 0
                    for i in line:
                        if idx > 1:
                            if i == word:
#                                print('i: ', i)
#                                print('idx: ', idx)
#                                print('Non-base word match {} at {} {}'.format(word, cnt, line))
                                return line
                        idx += 1
#        cnt += 1

    return []


def savePickle(whichPickle, p):

    if whichPickle == 'sA_Obj':
        f = open('pickles/sA_Obj.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved sA_Obj.pkl')
        
    elif whichPickle == 'taggedCorpusSents':
        f = open('pickles/taggedCorpusSents.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved taggedCorpusSents.pkl')

    elif whichPickle == 'untaggedCorpusSents':
        f = open('pickles/untaggedCorpusSents.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved untaggedCorpusSents.pkl')

    elif whichPickle == 'taggedBoW':
        f = open('pickles/taggedBoW.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved taggedBoW.pkl')

    elif whichPickle == 'kbTree':
        f = open('pickles/kbTree.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved kbTree.pkl')
 
    else: 
        print('Unrecognized pickle name: ', whichPickle)


def loadPickle(whichPickle):

    if whichPickle == 'sA_Obj':
        f = open('sA_Obj.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded sA_Obj.pkl')
        return obj
    
    elif whichPickle == 'taggedBoW':
        f = open('pickles/taggedBoW.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/taggedBoW.pkl')
        return obj

    elif whichPickle == 'taggedCorpusSents':
        f = open('pickles/taggedCorpusSents.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/taggedCorpusSents.pkl')
        return obj

    elif whichPickle == 'kbTree':
        f = open('pickles/kbTree.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/kbTree.pkl')
        return obj

    elif whichPickle == 'inflections':
        f = open('pickles/inflections.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/inflections.pkl')
        return obj
    
    else:
        print('Unrecognized pickle name')

    return None


def insertKBNode(kbTree, node2Insert):

    print('  --- insertKBNode ---')

    if kbTree == None:
        kbTree = loadPickle('kbTree')

    print(kbTree.print_tree(kbTree.root, ''))
    print('---')
    if len(node2Insert) != 5:
        print('node2Insert length error:')
        print(node2Insert)
        return None
    print(node2Insert)
    new_Node    = node2Insert[0]
    new_similar = node2Insert[1]
    new_tag     = node2Insert[2]
    new_canDo   = node2Insert[3]
    
    # Ensure parent node exists
    parentNode = kbTree.find_node(kbTree.root, node2Insert[-1])

    if parentNode == None:
        print('Parent node {} for new node {} does not exist.'.format(node2Insert[-1], new_Node))
        return None

    print('Parent node {} for new node {} found.'.format(node2Insert[-1], new_Node))
    print(parentNode.key)
    print(parentNode.similar)
    print(parentNode.tag)
    print(parentNode.canDo)
    print(parentNode.children)
    for c in parentNode.children:
        print(c)

    print('Warning: ')
    print('This will insert a new node {} between {} node and the above childern.'.format(new_Node, parentNode.key))
    result = input('Continue <Y/N>? ')
    if result not in ['Y', 'y']:
        return None

    # Keep a copy of the parent children
    parentNodeChildren = [] 
    for c in parentNode.children:
        parentNodeChildren.append(c)

    print('Adding/inserting new node: ', new_Node, new_similar, new_tag, new_canDo, parentNode.key)
    kbTree.add(new_Node, new_similar, new_tag, new_canDo, parentNode.key)

    insertedNode = kbTree.find_node(kbTree.root, new_Node)

    # Add the orignal parent children to inserted node
    for c in parentNodeChildren:
        insertedNode.children.append(c)

    # Keep the newly added child and clear the old children
    keepChild = parentNode.children[-1]
    parentNode.children.clear()
    parentNode.children.append(keepChild)


    print('  --- insertKBNode Complete ---')
    return kbTree


def chkTagging(taggedInput, taggedBoW):

    tagging = []

    for w in taggedInput:
        tmpTag = []
        word = w[0]
        tag = w[1]
        tmpTag.append(word)
        tmpTag.append(tag)
        for t in taggedBoW:    
            if w[0] == t[0]:
                tmpTag.append(t[1])
                print('t and i match: ')
                print('w; ', w)
                print('t: ', t)
        tagging.append(tmpTag)
        
    print('---')
    for t in tagging:
        print('t: ')
        print(t)


    return 'tags match BoW or do not match BoW'

