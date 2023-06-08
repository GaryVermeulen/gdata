#
# mrScapper.py
#


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
        print('no kids dictionary found...')
        element = soup.find('div', id='left-content')
        
    page_text = element.get_text()

    driver.close()

    return page_text


def parseAndPackage(taggedWord, text):

    word = taggedWord[0]
    tag = taggedWord[1]
    cleanedList = []
    defs = []
    pos = []
    nextLineIsPOS = False
    tmp = []
    inflections = []

    defs.append(taggedWord)
#    defs.append(tag)

    textList = text.split('\n')

#    print('len textList: ', len(textList))
#    print(textList)

    for line in textList:   # Remove blanks lines
        l = line.strip()
        if len(l) > 0:
            cleanedList.append(l)

#    print('len cleanedList: ', len(cleanedList))
#    for c in cleanedList:
#        print(c)

    for i in range(len(cleanedList)):
        curLine = cleanedList[i]
        curLineLst = curLine.split()
        
        """
        print('-' * 5)
        print('curLine:')
        print(curLine)
        print('curLineLst:')
        print(curLineLst)
        """
        if nextLineIsPOS:
            pos = curLineLst[0]
            if pos == 'verb':
                inflections = cleanedList[i + 1].split(';')
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
            if pos == 'verb':
                inflections = cleanedList[i + 1].split(';')
            continue

        if curLineLst[0] == 'plural':
                inflections.append(curLineLst[1])
                continue

        if curLineLst[0] == ':':
            tmp.append([word])
            tmp.append([pos])
            tmp.append(inflections)
            tmp.append(curLineLst)
            defs.append(tmp)
            tmp = []
            inflections = []
            continue

        # No need to continue once we reach the Synonyms
        if len(curLineLst) == 1:
            if curLineLst[0] == 'Synonyms':
                break


#    print('len(defs): ', len(defs))
#    print('defs:')
#    print(defs)
    
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
                tmp.append([])     # Depends on the past of word
                tmp.append(pastOf)
                tmp.append(lLst)
                defs.append(tmp)
                pastOf = []
                tmp = []
                
    return defs


def scrapeAndProcess(taggedWord):

    rawText = seleniumSoup(taggedWord)

    newWordDef = parseAndPackage(taggedWord, rawText)

    return newWordDef


if __name__ == "__main__":

    word = 'i'

    taggedWord = ('however', 'RB')
    

    print('scrapping for : ', taggedWord)

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

    newWordDef = scrapeAndProcess(taggedWord)

    print(type(newWordDef))
    print(len(newWordDef))

    for d in newWordDef:
        print(d)
    

    


