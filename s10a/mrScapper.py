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
    element = soup.find('div', id='kidsdictionary')

    if element == None:
        print('no kids dictionary found...')
        element = soup.find('div', id='left-content')
        
    page_text = element.get_text()

    driver.close()

    return page_text


def parseAndPackage(word, text):

    curDef = 0
    maxDef = 0
    pos = ''
    nextLineIsPOS = False
    defs = []

    textList = text.split('\n')

    print('len textList: ', len(textList))

    for line in textList:
        l = line.strip()

        if len(l) > 0:

            print('len l: ', len(l))
            print('L>>{}<<'.format(l))

            if nextLineIsPOS:
                pos = l
                print('POS: ', pos)
                nextLineIsPOS = False
        
            if curDef == 0:
                if l[0].isnumeric():
                    if len(l) == 6: # '1 of 2' or '2 of 2' 
                        lineLst = l.split()
                        print('>: ', lineLst)
                        if lineLst[1] == 'of':
                            print('>: def: {} {} {}'.format(lineLst[0], lineLst[1], lineLst[2]))
                            if curDef == 0:
                                curDef = int(lineLst[0])
                                maxDef = int(lineLst[2])
                                print('>: ', type(curDef))
                                print(curDef)
                                print('>: ', type(maxDef))
                                print('>: ', maxDef)
                                nextLineIsPOS = True

            if curDef > 0 and curDef < maxDef:
                if l[0] == ':':
                    defs.append(l[0])
                    curDef += 1
            
                            
            if             



    return 'someStrucure'


if __name__ == "__main__":

    word = 'finish'

    print('scrapping for : ', word)

    rawText = seleniumSoup(word)

    print('-' * 10)
    print('rawText:')
    print(rawText)

    someStrucure = parseAndPackage(word, rawText)

    print('-' * 10)
    print('someStrucure:')
    print(someStrucure)


    


