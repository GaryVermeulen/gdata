#
# scapeWord.py
#
#   Scrape a word definition from Merriam-Webster and return
#   {
#       {"word": word, "tag": tag, "definitions": "def1"}
#           ...
#       {"word": word, "tag": tag, "definitions": "def(n)"}
#   ]
#

#from commonConfig import nn, vb, rb, jj, prp

# Build pos as we go...
#
noun = 'noun'
verb = 'verb'
transitiveVerb = 'transitive verb'
intransitiveVerb = 'intransitive verb'
adjective = 'adjective'
adverb = 'adverb'
preposition = 'preposition'
conjunction = 'conjunction'
interjection = 'interjection'

posList = [noun, verb, transitiveVerb, intransitiveVerb, adjective, adverb, preposition, conjunction, interjection]


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

    try:
    
        driver.get("https://www.merriam-webster.com/dictionary/" + word)
    #except selenium.common.exceptions.TimeoutException:
    except driver.common.exceptions.TimeoutException:
        print('Timeout caught--returning nothing.')
        return ''

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


def parseAndPackage(taggedWord, text):

    word = taggedWord[0]
    tag = taggedWord[1]
    cleanedList = []
    defs = []
    pos = []
    nextLineIsPOS = False
    tmp = []

    saveNextLine = True
    lastLine = []

    # First item is what we can glean without web scrape
#    tmp.append([word])
#    tmp.append([tag])
#    
#    defs.append(tmp)

    if text == None:
        return defs # Web scrapping retunred nothing

#    tmp = [] # reset tmp

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

        print('bottom: curLineLst:')
        print(curLineLst)
        print('-----')
        if "past" == curLineLst[0] and "of" == curLineLst[1]:
            print('Past of found')
            print('curLine: ', curLineLst)
            nextLine = cleanedList[i + 1]
            curLineLst.append(nextLine)

            if len(defs) == 0:
                tmpDefs = []
                tmpDefs.append([word])
                tmpDefs.append([tag])
                tmpDefs.append([' '.join(curLineLst)])
                defs.append(tmpDefs)
            
        print('defs:')
        print(defs)

        # No need to continue once we reach the Synonyms or Phrases
        #if len(curLineLst) == 1:
        #    if curLineLst[0] == 'Synonyms' or curLineLst[0] == 'Phrases':
        #        break

#    for d in defs:
#        print(d)
        
    return defs


##############################################################
def parseRawText(taggedWord, rawText):

    print("Start parseRawText:")
    print('taggedWord: ', taggedWord)
    print('type rawText: ', type(rawText))
    print('len rawText: ', len(rawText))

    if len(rawText) <= 0:
        print('Nothing to parse...exiting...')
        return None

    pos = ''
    inflections = ''
    plural = ''
    definition = ''
    defList = []

    rawTextList = rawText.split('\n')

    # Remove blank lines, leading and trailing spaces
    tmpLst = []
    
    for line in rawTextList:
        line = line.lstrip()
        line = line.rstrip()
        if len(line) > 0:
            #print(line)
            tmpLst.append(line)

    lineCount = 0
    
    for line in tmpLst:
        lineCount += 1
        # Typically the first line is the returned word.
        # Beware for searching for "walked" returns "walk"
        if lineCount == 1:
            print("Line: {}; Search for: {} Returned: {}.".format(lineCount, taggedWord[0], line))
            searchedReturnPair = (taggedWord[0], line)
            print('searchedReturnPair: ', searchedReturnPair)
        else:
            print("Line: {}; {}".format(lineCount, line))

            # Looking for "verb", "noun", etc.
            if line in posList:
                print('pos found: ', line)
                pos = line
                print('pos: ', pos)

            # Looking for "verb (1)" "or noun (1)"
            parenFoundAt = line.find("(")
            if parenFoundAt > -1:
                print('paren found at postion: ', parenFoundAt)
                if parenFoundAt == 5: # noun and verb are same length; verb (1), etc.
                    lineLst = line.split('(')
                    print('lineLst: ', lineLst)
                    if lineLst[0].rstrip() in posList:
                        pos = lineLst[0].rstrip()
                        print('lineLst[0]: ', lineLst[0])
                        print('pos: ', pos)

            # Looking for inflections
            semicolonFoundAt = line.find(";")
            if semicolonFoundAt > -1:
                print('semicolon (inflections) found at postion: ', semicolonFoundAt)
                inflections = line
                print(inflections)

            # Looking for plural
            pluralFoundAt = line.find("plural")
            if pluralFoundAt > -1:
                print('plural found at position: ', pluralFoundAt)
                if pluralFoundAt == 0:
                    plural = line
                    print(pluralFoundAt)
                    print(plural)

            # Looking for definitions
            definitionFoundAt = line.find(":")
            if definitionFoundAt == 0:
                print('Definition Found:')
                definition = line.replace(":", "")
                definition = definition.lstrip()
                print(definition)

            if len(definition) > 0:
                print('BOTTOM LINE:')
                print('searchedReturnPair: ', searchedReturnPair)
                print('pos: ', pos)
                print('inflections: ', inflections)
                print('plural: ', plural)
                print('definition: ', definition)
                tmpDef = {"word": searchedReturnPair[1], "tag": pos, "definition": inflections + ',' + plural + ',' + definition}
                defList.append(tmpDef)
                definition = ''

            # Stop parsing condiction...~?
            if line == 'Phrases' or line == 'Synonyms':
                print("Stop at: ", lineCount, line)
                break
                

    print('--------')
    for d in defList:
        print(d)


    return None


def scrapeAndProcess(taggedWord):

    rawText = seleniumSoup(taggedWord)

    print('rawText:')
    print(rawText)

    #return parseAndPackage(taggedWord, rawText)
    #parseAndPackaged = parseAndPackage(taggedWord, rawText)
    #print('parseAndPackaged:')
    #print(parseAndPackaged)
    #
    #return parseAndPackaged

    parsedText = parseRawText(taggedWord, rawText)

    if parsedText == None:
        print('parseRawText returned None')
        return None

    return parsedText


def packageDefs(taggedWord, newWordDef):

    wordDefs = []
    defCnt = 0

    print('newWordDef:')
    print(newWordDef)

    for wordDef in newWordDef:

        print('wordDef:')
        print(wordDef)
        
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
          
        tmpDict = {"word": word, "tag": tag, "definition": wordDefStr}            
        wordDefs.append(tmpDict)
        defCnt += 1
        
    return wordDefs


def scrapeWord(taggedWord):
    # Assumes the input is truly unknown
    # Does not mess with known inflections

    if len(taggedWord) <= 0:
        print('No input given...exiting...')
        return None

    newWordDef = scrapeAndProcess(taggedWord)

    if newWordDef == None:
        print("scrapeAndProcess returned None")
        return None
    else:
        print('Scraped the following from the web:')
        print(len(newWordDef))
        print(newWordDef)
        #
        for d in newWordDef:
            print('-' * 5)
            print('d: ', d)
        
        print('-' * 10)

    #wordDefs = packageDefs(taggedWord, newWordDef)
    #print('packageDefs returned:')
    #    
    #print(len(wordDefs))
    #print(wordDefs)
    #for d in wordDefs:
    #    print(d)

    return wordDefs


if __name__ == "__main__":

#    taggedWord = ('I', 'PRP')
#    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
#    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('fart', 'NN')
#    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD') # Build in inflection check
    taggedWord = ('walked', 'VBD')
#    taggedWord = ('boat', 'NN')
#    taggedWord = ('boating', 'VBG')
#    taggedWord = ('wind', 'NN')
#    taggedWord = ''
#    taggedWord = ('walled', 'VBD')
#    taggedWord = ('walls', 'NNS')
#    taggedWord = ('often', 'RB')

    print('-- scrapeWord.py __main__ scrapping for : ', taggedWord)


    results = scrapeWord(taggedWord)

    if results == None:
        print('scrapeWord retunred: None')
    else:
        print('results:')
        for r in results:
            print(r)

    print('-- scrapeWord.py __main__ scrapping completed --')

