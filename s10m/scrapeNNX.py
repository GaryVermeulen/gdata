#
# scappeNNX.py
#
#   Was mrScapper.py, but was too broad.
#   This version is focussed on just scrapping missing pure
#   nouns missing from the nnxKB.
#   Will not process nouns-verbs--those will be processed
#   by a (yet to be developed) noun-verb processor.
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
    element = soup.find('div', id='left-content')

    if element == None:
        print('dictionary retuned NONE...')
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
    return defs


def scrapeAndProcess(taggedWord):

    tag = getInflectionTag(taggedWord[1])
    inflect = getInflections(taggedWord[0], tag)
    rawText = seleniumSoup(taggedWord)

    return parseAndPackage(taggedWord, inflect, rawText)


def isNounOnly(newWordDef):

    cnt = 1
    for d in newWordDef:
        print('isNounOnly -- d: ', d)
        if cnt > 1:
            if d[1] != ['noun']:
                print('d[1]: ', d[1])
                return False
        cnt += 1
    return True


def gleanSimilars(taggedWord, newWordDef):

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

            tmpSim = []
            for w in taggedWordDef:
                if w[1] in ['JJ', 'NN']:
                    tmpSim.append(w[0])
            tmpSimLen = len(tmpSim)
            item = {"word": taggedWord, "similars": tmpSim}
            similars.append(item)
        defCnt += 1
   
    return similars


def scrapeNNX(taggedWord):

    if taggedWord[1] not in nnx:
        print('Invalid tag: ', taggedWord)
        sys.exit("Only for {} tags".format(nnx))

    results = checkWord(taggedWord[0])
    print(results)

    if not results[2]["kb"]:
        print('not in kb--so let us look for it on the web...')
        newWordDef = scrapeAndProcess(taggedWord)

        print('Scraped the following from the web:')
        print(len(newWordDef))

        for d in newWordDef:
            print('-' * 5)
            print('d: ', d)

        print('Is this word a pure noun or a noun-verb?')
        #newWordDef = isNounOnly(newWordDef)

        if not isNounOnly(newWordDef):
            print('WARNING: {} was found to be a noun-verb and will be processed later--skipping.'.format(taggedWord))
            return []
            #sys.exit("Noun-verb found, exiting.")
        else:
            print("Yes, continuing...")

            print('-' * 10)
            similars = gleanSimilars(taggedWord, newWordDef)
            print('gleanSimilars returned:')
        
            print(len(similars))
            print(similars)
            for s in similars:
                print(s)
          
    else:
        print('found in kb')




    return similars


if __name__ == "__main__":

#    taggedWord = ('i', 'PRP')
    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
#    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
#    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD')
#    taggedWord = ('boat', 'NN')
       
    print('-- scrapeNNX.py __main__ scrapping for : ', taggedWord)


    results = scrapeNNX(taggedWord)

    print('results:')
    for r in results:
        print(r)

    print('-- scrapeNNX.py __main__ scrapping completed --')

