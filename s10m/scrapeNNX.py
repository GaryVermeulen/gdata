#
# scappeNNX.py
#
#   Was mrScapper.py, but was too broad.
#   This version is focussed on just scrapping
#   missing NNXs in KB
#

import sys
import spacy

from commonUtils import getInflectionTag
from commonUtils import getInflections
from commonConfig import *
from checkWord import *

nlp = spacy.load("en_core_web_lg") # lg has best accuracy


def seleniumSoup(taggedWord):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup

    word = taggedWord[0]

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
#    driver = webdriver.Firefox()
    driver.get("https://www.merriam-webster.com/dictionary/" + word.strip())

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
#    element = soup.find('div', id='kidsdictionary')
    element = soup.find('div', id='left-content')

    if element == None:
#        print('no kids dictionary found...')
        print('dictionary retuned NONE...')
#        element = soup.find('div', id='left-content')
        return None
        
    page_text = element.get_text()

    # Save plain text for debug purposes
#    f = open('rawHTML.txt', 'w', encoding="utf-8")
#    f.write(page_text)
#    f.close()

    driver.close()

    return page_text


def parseAndPackage(taggedWord, inflect, text):

    word = taggedWord[0]
    tag = taggedWord[1]
    cleanedList = []
    defs = []
    pos = []
    nextLineIsPOS = False
    tmp = []
    inflections = []

    # First item is what we can glean without web scrape
    tmp.append([word])
    tmp.append([tag])
    tmp.append(inflect)
    defs.append(tmp)

    if text == None:
        return defs # Web scrapping retunred nothing

    tmp = [] # reset tmp

    textList = text.split('\n')

    for line in textList:   # Remove blanks lines
        l = line.strip()
        if len(l) > 0:
            cleanedList.append(l)

    for i in range(len(cleanedList)):
        word = taggedWord[0]
        curLine = cleanedList[i]
        curLineLst = curLine.split()
        curFirstWord = curLineLst[0]
        if len(curLineLst) > 1:
            curSecondWord = curLineLst[1]
        else:
            curSecondWord = 'UNK'
        
        if nextLineIsPOS:
            pos = curLineLst[0]
            nextLineIsPOS = False
            continue

        # '1 of 2' of '4 of 4'
        if len(curLineLst) == 3: 
            if curLineLst[0].isnumeric() and (curLineLst[1] == 'of') and curLineLst[2].isnumeric():
                nextLineIsPOS = True
                continue

        # No '1 of 2'
        if curLineLst[0] in ['noun', 'pronoun', 'adjective', 'adverb', 'verb', 'preposition', 'conjunction', 'interjection']:
            pos = curLineLst[0]
            continue

        # Gathering easy definitions
        if curLineLst[0] == ':':
            tmp = []
            tmp.append([word])
            tmp.append([pos])
            tmpW = []
            for w in curLineLst:
                if w != ':':
                    tmpW.append(w)
            tmp.append(tmpW)
            defs.append(tmp)
            
            continue

        # No need to continue once we reach the Synonyms or Phrases
        if len(curLineLst) == 1:
            if curLineLst[0] == 'Synonyms' or curLineLst[0] == 'Phrases':
                break
    
    # Assume special case 'past of': Ex: ran
    ## Do not remember what I was doing here, something with tense...~?
    """
    if len(defs) == 0:
        pastOf = []
        tmp = []
        for line in cleanedList:
            lLst = line.split()
            if lLst[0] == 'past':  
                pastOf = lLst
                continue
            if len(pastOf) > 0:
                tmp.append([word])
                tmp.append(['past of?'])     # Depends on the past of word
                tmp.append(pastOf)
                tmp.append(lLst)
                defs.append(tmp)
                pastOf = []
                tmp = []
    """         
    return defs


def scrapeAndProcess(taggedWord):

    tag = getInflectionTag(taggedWord[1])
    inflect = getInflections(taggedWord[0], tag)
    rawText = seleniumSoup(taggedWord)

    return parseAndPackage(taggedWord, inflect, rawText)


def gleanSimilars(newWordDef):

    similars = []
    defCnt = 0

    for wordDef in newWordDef:
        if defCnt > 0:
            wordDefStr = ' '.join(wordDef[2])

            doc = nlp(wordDefStr)

            taggedWordDef = []
            for token in doc:
                tmpToken = ((str(token.text)), (str(token.tag_)))
                taggedWordDef.append(tmpToken)

            #print('Spacy tagged wordDef:')
            print(taggedWordDef)

            tmpSim = []
            for w in taggedWordDef:
                if w[1] in ['JJ', 'NN']:
                    #tmpW = []
                    #tmpW.append(w[0])
                    tmpSim.append(w[0])
            tmpSimLen = len(tmpSim)
            item = {"len": tmpSimLen, "arr": tmpSim}
            similars.append(item)
        defCnt += 1

    defCnt = 0
    for i in similars:
        iLen = i["len"]
        if defCnt < iLen:
            defCnt = iLen

    print('defCnt: ', defCnt)

    return similars


if __name__ == "__main__":

    #word = 'i'

#    taggedWord = ('i', 'PRP')
    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
#    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
#    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD')

    
    if taggedWord[1] not in nnx:
        print('Invalid tag: ', taggedWord)
        sys.exit("Only for {} tags".format(nnx))
        
    print('scrapping for : ', taggedWord)

    results = checkWord(taggedWord[0])
    print(results)

    if not results[2]["kb"]:
        print('not in kb--so let us look for it on the web...')
        newWordDef = scrapeAndProcess(taggedWord)
        print(len(newWordDef))

        for d in newWordDef:
            print('-' * 5)
            print('d: ', d)
        similars = gleanSimilars(newWordDef)           
        print(len(similars))
        print(similars)
    else:
        print('found in kb')



    

