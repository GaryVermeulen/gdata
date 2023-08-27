#
# mrScapper.py
#

from commonUtils import getInflectionTag
from commonUtils import getInflections

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
        word = taggedWord[0]
        curLine = cleanedList[i]
        curLineLst = curLine.split()
        curFirstWord = curLineLst[0]
        if len(curLineLst) > 1:
            curSecondWord = curLineLst[1]
        else:
            curSecondWord = 'UNK'

#        print('cl i: ', cleanedList[i])
        """
        print('-' * 5)
        print('curLine:')
        print(curLine)
        print('curLineLst:')
        print(curLineLst)
        """
        
        if nextLineIsPOS:
            pos = curLineLst[0]
#            if pos == 'verb':
#                inflections = cleanedList[i + 1].split(';')
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
#            if pos == 'verb':
#                inflections = cleanedList[i + 1].split(';')
            continue
        
        """
        if curFirstWord == 'plural' and len(curLineLst) > 1:
            inflections.append(curSecondWord)
            continue

        if curSecondWord == 'plural' and len(curLineLst) == 2:
            word = curFirstWord
            inflections.append(word)
            continue

        print('word: ', word)
        """
        
        if curLineLst[0] == ':':
            tmp.append([word])
            tmp.append([pos])
#            tmp.append(inflections)
            tmp.append([]) # Gathering inflections from web is going to be a challenge
            tmp.append(curLineLst)
            defs.append(tmp)
            tmp = []
            inflections = []
            continue

#        print('word after: ', word)

        # No need to continue once we reach the Synonyms or Phrases
        if len(curLineLst) == 1:
            if curLineLst[0] == 'Synonyms' or curLineLst[0] == 'Phrases':
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

    tag = getInflectionTag(taggedWord[1])
#    inflect = getInflections(taggedWord[0], tag, True)
    inflect = getInflections(taggedWord[0], tag)

    rawText = seleniumSoup(taggedWord)
    """
    print('seleniumSoup returned:')
    print(type(rawText))
    print(len(rawText))
    print(rawText)
    """
#    if rawText == None:
#        return None

    newWordDef = parseAndPackage(taggedWord, inflect, rawText)

    return newWordDef


if __name__ == "__main__":

    #word = 'i'

    taggedWord = ('i', 'PRP')
#    taggedWord = ('good', 'JJ')
#    taggedWord = ('cut', 'VBD')
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
    

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
        print(d[0][0])
        print(d[1][0])
        if len(d) > 3:
            print(d[3])
        else:
            print(d[2])

        
    

    

