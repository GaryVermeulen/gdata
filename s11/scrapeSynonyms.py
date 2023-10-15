#
# scappeSynonyms.py
#

import sys
import spacy


nlp = spacy.load("en_core_web_lg") # lg has best accuracy


def seleniumSoup(taggedWord):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup

    word = taggedWord[0].strip()

    print('*** word: ', word)

    options = Options()
    options.add_argument("--headless")

#    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
#    driver = webdriver.Firefox()

    print('*** Past options=options')
    
    driver.get("https://www.merriam-webster.com/dictionary/" + word)

    print('*** Past driver.get')
    print('*** driver.current_url:')
    print(driver.current_url)
    print('***')
    
    page_source = driver.page_source

    print('*** Past page_source')
    
    soup = BeautifulSoup(page_source, 'html.parser')

    print('*** Past soup')
    
    element = soup.find('div', id='left-content')

    print('*** Past element')

    if element == None:
        print('dictionary retuned NONE...')
        return None
        
    page_text = element.get_text()

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

#    for d in defs:
#        print(d)
        
    return defs


def scrapeAndProcess(taggedWord):

    tag = getInflectionTag(taggedWord[1])
    inflect = getInflections(taggedWord[0], tag)
    rawText = seleniumSoup(taggedWord)

    return parseAndPackage(taggedWord, inflect, rawText)


def packageDefs(taggedWord, newWordDef):

    wordDefs = []
    defCnt = 0

    for wordDef in newWordDef:
        
        word = wordDef[0][0]
        pos = wordDef[1][0]
        wordDefStr = ' '.join(wordDef[2])
        
        if pos == 'noun':
            tag = nn
        elif pos == 'verb':
            tag = vb
        elif pos == 'adverb':
            tag = rb
        elif pos == 'adjective':
            tag = jj
        elif pos == 'pronoun':
            tag = prp
        elif pos == 'preposition':
            tag = 'IN' 
        elif pos == 'conjunction':
            tag = 'CC'
        elif pos == 'interjection':
            tag = 'UH'
        else:
            tag = pos # Pass-along UNK tag to see what it is

        if defCnt == 0:
            tmpDict = {"word": word, "tag": tag, "inflections": wordDefStr}
        else:
            tmpDict = {"word": word, "tag": tag, "definition": wordDefStr}
        wordDefs.append(tmpDict)
        defCnt += 1
        
    return wordDefs


def scrapeWord(taggedWord):

    if taggedWord[1] not in validTags:
        print('Invalid tag: ', taggedWord)
        #sys.exit("Only for {} tags".format(nnx))
        return []

    results = checkWord(taggedWord[0])
    print(results)

    if results[2]["kb"]:
        print('{} found in KB, so why scrape web, exiting...'.format(taggedWord))
        return []
                
    newWordDef = scrapeAndProcess(taggedWord)

#    print('Scraped the following from the web:')
#    print(len(newWordDef))
#
#    for d in newWordDef:
#        print('-' * 5)
#        print('d: ', d)
        
    print('-' * 10)

    wordDefs = packageDefs(taggedWord, newWordDef)
    print('packageDefs returned:')
        
    print(len(wordDefs))
#    print(wordDefs)
    for d in wordDefs:
        print(d)

    return wordDefs


if __name__ == "__main__":

#    taggedWord = ('I', 'PRP')
#    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
#    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD') # Build in inflection check
#    taggedWord = ('boat', 'NN')
       
    print('-- scrapeNNX.py __main__ scrapping for : ', taggedWord)


    results = scrapeWord(taggedWord)

    print('results:')
    for r in results:
        print(r)

    print('-- scrapeNNX.py __main__ scrapping completed --')

