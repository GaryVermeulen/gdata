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

from commonUtils import connectMongo
from commonConfig import nn, vb, rb, jj, prp

# Build pos as we go...
#
noun = 'noun'
pronoun = 'pronoun'
verb = 'verb'
transitiveVerb = 'transitive verb'
intransitiveVerb = 'intransitive verb'
adjective = 'adjective'
adverb = 'adverb'
preposition = 'preposition'
conjunction = 'conjunction'
interjection = 'interjection'

posList = [noun, pronoun, verb, transitiveVerb, intransitiveVerb, adjective, adverb, preposition, conjunction, interjection]


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
        print('soup.find retuned NONE...')
        return None
        
    page_text = element.get_text()

    driver.close()

    return page_text


def parseRawText(taggedWord, rawText):

    print("Start parseRawText:")
    print('taggedWord: ', taggedWord)
    print('type rawText: ', type(rawText))

    if rawText != None:
        print('len rawText: ', len(rawText))
    else:
        return None
    
    print('----')
    #print(rawText)
    #print('----')

    if len(rawText) <= 0:
        print('Nothing to parse...exiting...')
        return None

    pos = ''
    inflections = ''
    plural = ''
    past = ''
    adjectiveLine = ''
    definition = ''
    defList = []
    getNextLine = False

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
        #print(lineCount, line)
        # Typically the first line is the returned word.
        # Beware for searching for "walked" returns "walk"
        if lineCount == 1:
            #print("Line: {}; Search for: {} Returned: {}.".format(lineCount, taggedWord[0], line))
            searchedReturnPair = (taggedWord[0], line)
            #print('searchedReturnPair: ', searchedReturnPair)
        else:
            #print("Line: {}; {}".format(lineCount, line))

            line = line.lstrip() # Hopefully this won't break other things

            # Looking for "verb", "noun", etc.
            if line in posList:
                #print('pos found: ', line)
                pos = line
                #print('pos: ', pos)

            # Looking for "verb (1)" "or noun (1)"
            parenFoundAt = line.find("(")
            if parenFoundAt > -1:
                #print('paren found at postion: ', parenFoundAt)
                if parenFoundAt == 5: # noun and verb are same length; verb (1), etc.
                    lineLst = line.split('(')
                    #print('lineLst: ', lineLst)
                    if lineLst[0].rstrip() in posList:
                        pos = lineLst[0].rstrip()
                        #print('lineLst[0]: ', lineLst[0])
                        #print('pos: ', pos)

            # Looking for inflections
            semicolonFoundAt = line.find(";")
            if semicolonFoundAt > -1:
                #print('semicolon (inflections) found at postion: ', semicolonFoundAt)
                inflections = line
                #print(inflections)

            # Looking for plural
            pluralFoundAt = line.find("plural")
            if pluralFoundAt > -1:
                #print('plural found at position: ', pluralFoundAt)
                if pluralFoundAt == 0:
                    plural = line
                    #print(pluralFoundAt)
                    #print(plural)

            # Looking for past tense (past tense and past participle)
            pastFoundAt = line.find("past")
            if pastFoundAt > -1:
                #print('past found at position: ', pastFoundAt)
                if pastFoundAt == 0:
                    past = line

            # Looking for adjective
            adjectiveFoundAt = line.find("adjective")
            #print('adjectiveFoundAt: ', adjectiveFoundAt)
            if adjectiveFoundAt > -1:
                #print('adjective found at position: ', adjectiveFoundAt)
                if adjectiveFoundAt == 0:
                    adjectiveLine = line
                    #print('adjectiveLine: ', lineCount, adjectiveLine)

            # Looking for definitions
            definitionFoundAt = line.find(":")
            if definitionFoundAt == 0:
                #print('Definition Found:')
                definition = line.replace(":", "")
                definition = definition.lstrip()
                if len(adjectiveLine) > 0:
                    definition = adjectiveLine + ' ' + taggedWord[0] + ','+ definition
                    adjectiveLine = ''
                #print(definition)

            if len(definition) > 0:
                #print('BOTTOM LINE:')
                #print('searchedReturnPair: ', searchedReturnPair)
                #print('pos: ', pos)
                #print('inflections: ', inflections)
                #print('plural: ', plural)
                #print('definition: ', definition)
                tmpDef = {"word": searchedReturnPair[1], "tag": pos, "definition": inflections + ',' + plural + ',' + ',' + past + ',' + definition}
                defList.append(tmpDef)
                definition = ''
                continue

            # Stop parsing condiction...~?
            if line == 'Phrases': # or line == 'Synonyms':
                print("Stop at (Phrases): ", lineCount, line)
                break

            if taggedWord[1] != 'VBD' and line == 'Synonyms':
                print("Stop at(VBD & Synonyms): ", lineCount, line)
                break

            # Past tense?
            if len(past) > 0:
                if getNextLine:
                    past = past + ' ' + line
                    # Hopefully a verb
                    if len(pos) <= 0:
                        pos = "VBD"
                    tmpDef = {"word": searchedReturnPair[1], "tag": pos, "definition": inflections + ',' + plural + ',' + ',' + past + ',' + definition}
                    defList.append(tmpDef)
                    break
                else:
                    getNextLine = True
                
    #print('--------')
    #print('len defList: ', len(defList))
    #for d in defList:
    #    print(d)

    return defList


def scrapeAndProcess(taggedWord):

    rawText = seleniumSoup(taggedWord)

    #print('rawText:')
    #print(rawText)

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

    retagged = updateTags(parsedText)

    #print('len retagged: ', len(retagged))
    #for r in retagged:
    #    print('r: ', r)

    return retagged


def updateTags(parsedText):

    wordDefs = []
    defCnt = 0

    #print('parsedText:')
    #print(parsedText)

    for wordDef in parsedText:

        #print('wordDef:')
        #print(wordDef)
        
        word = wordDef["word"]
        pos = wordDef["tag"]
        wordDefStr = wordDef["definition"]
        
        if pos == noun:
            tag = nn
        elif pos in [verb, transitiveVerb, intransitiveVerb]:
            tag = vb
        elif pos == adverb:
            tag = rb
        elif pos == adjective:
            tag = jj
        elif pos == pronoun:
            tag = prp
        elif pos == preposition:
            tag = 'IN' 
        elif pos == conjunction:
            tag = 'CC'
        elif pos == interjection:
            tag = 'UH'
        else:
            tag = pos # Pass-along UNK tag to see what it is
          
        tmpDict = {"word": word.capitalize(), "tag": tag, "definition": wordDefStr}            
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
    #else:
        #print('Scraped the following from the web:')
        #print(len(newWordDef))
        #print(newWordDef)
        #
        #for d in newWordDef:
        #    print('-' * 5)
        #    print('d: ', d)
        
        #print('-' * 10)

    #wordDefs = packageDefs(taggedWord, newWordDef)
    #print('packageDefs returned:')
    #    
    print('scrapeWord returning {} defs...'.format(len(newWordDef)))
    #print(wordDefs)
    #for d in wordDefs:
    #    print(d)

    return newWordDef


if __name__ == "__main__":

#    taggedWord = ('I', 'PRP')
#    taggedWord = ('boy', 'NN')
#    taggedWord = ('bus', 'NN')
#    taggedWord = ('tickle', 'NN') # But is also a verb
#    taggedWord = ('stinky', 'JJ')
#    taggedWord = ('runny', 'JJ')
#    taggedWord = ('sunny', 'JJ')
    taggedWord = ('fart', 'NN')
#    taggedWord = ('run', 'VB')
#    taggedWord = ('ran', 'VBD') # Build in inflection check
#    taggedWord = ('walked', 'VBD')
#    taggedWord = ('had', 'VBD')
#    taggedWord = ('boat', 'NN')
#    taggedWord = ('boating', 'VBG')
#    taggedWord = ('wind', 'NN')
#    taggedWord = ''
#    taggedWord = ('walled', 'VBD')
#    taggedWord = ('walls', 'NNS')
#    taggedWord = ('often', 'RB')

    print('-- scrapeWord.py __main__ scrapping for : ', taggedWord)

    mdb = connectMongo()
    simpDB = mdb["simp"]
    webDictionary = simpDB["webDictionary"]

    webDictionary.drop()


    results = scrapeWord(taggedWord)

    if results == None:
        print('scrapeWord retunred: None')
    else:
        print('results:')
        for r in results:
            print(r)
            webDictionary.insert_one(r)


#for line in taggedDict:
#        if line[2] != 'UNK':
#            simpDictionary.insert_one({"index": line[0], "word": line[1], "tag": line[2], "definition": line[3]})
        

    print('-- scrapeWord.py __main__ scrapping completed --')

