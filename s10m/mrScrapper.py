#
# mrScapper.py
#

from commonUtils import getInflectionTag
from commonUtils import getInflections

from checkWord import * 

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
                
        if curLineLst[0] == ':':
            tmp.append([word])
            tmp.append([pos])

            tmp.append(['why?']) # Gathering inflections from web is going to be a challenge
            tmp.append(curLineLst)
            defs.append(tmp)
            tmp = []
            inflections = []
            continue

        # No need to continue once we reach the Synonyms or Phrases
        if len(curLineLst) == 1:
            if curLineLst[0] == 'Synonyms' or curLineLst[0] == 'Phrases':
                break
    
    # Assume special case 'past of': Ex: ran
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
                
    return defs


def scrapeAndProcess(taggedWord):

    tag = getInflectionTag(taggedWord[1])
    inflect = getInflections(taggedWord[0], tag)
    rawText = seleniumSoup(taggedWord)

    return parseAndPackage(taggedWord, inflect, rawText)


if __name__ == "__main__":

    #word = 'i'

#    taggedWord = ('i', 'PRP')
#    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
#    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD')

    

    print('scrapping for : ', taggedWord)

    results = checkWord(taggedWord[0])
    print(results)

    if not results[2]["kb"]:
        print('not in kb--so let us look for it on the web...')
        newWordDef = scrapeAndProcess(taggedWord)

        print(type(newWordDef))
        print(len(newWordDef))

        for d in newWordDef:
            print('-' * 5)
            print('d: ', d)
            print('d[0][0]: ', d[0][0])
            print('d[1][0]: ', d[1][0])
            print('d[2][0]: ', d[2][0])
            if len(d) > 3:
                print('d>3 (d[3]): ', d[3])
            
    else:
        print('found in kb')

    """
    rawText = seleniumSoup(word)

#    print('-' * 10)
#    print('rawText:')
#    print(rawText)

    someStructure = parseAndPackage(word, rawText)

    print('-' * 10)
    print('someStructure:')
    print(type(someStructure))
    print(len(someStructure))
    
    for structure in someStructure:
        print(structure)
    """
    """
    newWordDef = scrapeAndProcess(taggedWord)

    print(type(newWordDef))
    print(len(newWordDef))

    for d in newWordDef:
        print('-' * 5)
        print('d: ', d)
        print('d[0][0]: ', d[0][0])
        print('d[1][0]: ', d[1][0])
        if len(d) > 3:
            print('d>3 (d[3]): ', d[3])
        else:
            print('d>3 else (d[2]): ', d[2])

        
    """
    

    

