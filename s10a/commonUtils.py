#
# commonUtils.py
#

import os

import pickle
from simpConfig import *


def getInflectionsPickle():
    
    with open('pickles/inflections.pkl', 'rb') as fp:
        inflects = pickle.load(fp)
        print('Aunt Bee loaded inflections.pkl')
    fp.close()

    return inflects


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
            soup2 =soup.find(class_="luna-pos")
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


def getInflections(word, tag, baseWordSearch):
    # This is really going to be fun, ex: saw (to cut) vs. past tense of see
#    cnt = 1
#    print('searching for word: {} tag: {}'.format(word, tag))

    allInflections = getInflectionsPickle()
    
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
        f = open('sA_Obj.pkl', 'wb')
        pickle.dump(p, f)
        f.close()
        print('Aunt Bee saved sA_Obj.pkl')
    else:
        print('Unrecognized pickle name')


def loadPickle(whichPickle):

    if whichPickle == 'sA_Obj':
        f = open('sA_Obj.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded sA_Obj.pkl')
        return obj
    elif whichPickle == 'taggedList':
        f = open('pickles/newTaggedList.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/newTaggedList.pkl')
        return obj

    elif whichPickle == 'newCorpus':
        f = open('pickles/newCorpus.pkl', 'rb')
        obj = pickle.load(f)
        f.close()
        print('Aunt Bee loaded pickles/newCorpus.pkl')
        return obj
    else:
        print('Unrecognized pickle name')

    return None
