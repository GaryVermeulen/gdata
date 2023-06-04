#
# mrScapper.py
#


def seleniumSoup(word):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup

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


def parseAndPackage(word, text):

    curDef = 0
    maxDef = 0
    pos = []
    nextLineIsPOS = False
    lastLineWasDef = False
    defs = []
    defAndEx = []
    examp = []

    textList = text.split('\n')

#    print('len textList: ', len(textList))

    for i in range(len(textList)):
        l = textList[i].strip()

        if len(l) > 0:
#            print('-' * 5)
#            print('len l: ', len(l))
#            print('L>>{}<<'.format(l))
            lLst = l.split()
            print('lLst:')
            print(lLst)

            if nextLineIsPOS:
                pos = lLst[0]
                print('POS: ', pos)
                nextLineIsPOS = False
                

            if len(lLst) == 3: # '1 of 2' of '4 of 4'
                if lLst[0].isnumeric() and (lLst[1] == 'of') and lLst[2].isdigit():
                    print(lLst[0])
                    print(lLst[0].isnumeric())
                    print(lLst[1])
                    print(lLst[2])
                    print(lLst[2].isnumeric())
                    nextLineIsPOS = True
                    continue

            # No '1 of 2'
            if lLst[0] in ['noun', 'pronoun', 'adjective', 'adverb', 'verb', 'preposition', 'conjunction', 'interjection']:
#                print('POS found...')
                pos = lLst[0]

        
    
#            print('nextLineIsPOS: ', nextLineIsPOS)

#            if lastLineWasDef and len(lLst) > 1:
#                lastLineWasDef = False
#                examp.append(lLst)
                
            if lLst[0] == ':':
                lastLineWasDef = True
#                print('WORD: ', word)
#                print('POS: ', pos)
                defAndEx.append([word])
                defAndEx.append([pos])
                defAndEx.append(lLst)
                defs.append(defAndEx)
                defAndEx = []


#    print('len(defs): ', len(defs))
#    print('defs:')
#    print(defs)
    """
    # Assume special case 'past of': Ex: ran
    if len(defs) == 0:
        pastOf = []
        defAndEx = []
        for line in textList:
            l = line.strip()
            if len(l) > 0:
                lLst = l.split()
                if lLst[0] == 'past':  
                    pastOf = lLst
                    continue
                if len(pastOf) > 0:
                    defAndEx.append([word])
                    defAndEx.append([])     # Depends on the past of word
                    defAndEx.append(pastOf)
                    defAndEx.append(lLst)
                    defs.append(defAndEx)
                    pastOf = []
    """            
    return defs


if __name__ == "__main__":

    word = 'duck'

    print('scrapping for : ', word)

    rawText = seleniumSoup(word)

    print('-' * 10)
    print('rawText:')
    print(rawText)

    someStructure = parseAndPackage(word, rawText)

    print('-' * 10)
    print('someStructure:')
    print(type(someStructure))
    print(len(someStructure))
    
    for structure in someStructure:
        print(structure)


    


