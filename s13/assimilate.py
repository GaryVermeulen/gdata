#
# assimilate.py
##
# Currently doing too much... need to simplfy

#from commonConfig import inputSentence
from commonConfig import Conversation
from commonUtils import isWordKnown, isWebWord
from commonUtils import getBaseWordFromInflections2
from commonUtils import connectMongo
from scrapeWord2 import scrapeWord2
from saveWebWord import saveWebWord
from findSVO import findSVO

mdb = connectMongo()
simpDB = mdb["simp"]
addNNP = simpDB["NNPs2Add"]

def assimilate(taggedCorpus, taggedSentence):

    limit = 7
    cnt = 0
    sentsRead = []
    saObjList = []
    manAdd = []
    conversationWindow = []
    conversationWindowSize = 3
    converSubectFreq = {}
    converSubectFreqLst = []
    firstLoop = True

    print('Start:--- assimilate ---')

    # First: Are we getting a sentence or a corpus?
    # Processing a corpus
    if taggedSentence == None:
        saveConverWin = False
        cursor = taggedCorpus.find({})

        for sent in cursor:
            cnt += 1
            print('{}: {}'.format(cnt, sent['taggedSentence']))
            manAdd = addWebWords(sent['taggedSentence'])
            sentsRead.append(sent['taggedSentence'])
          
            if cnt == limit:
                break
            
    # Processing a single sentence
    if taggedCorpus == None:
        print('taggedSentence:')
        print(taggedSentence)
        manAdd = addWebWords(taggedSentence)
        sentsRead.append(taggedSentence)
        saveConverWin = True

    print('assimilate manAdd: ', manAdd)
    if len(manAdd) > 0:
        for a in manAdd:
            print('Need to manually add: ', a)

    print('sentsRead len: ', len(sentsRead))
    if len(sentsRead) <= 0:
        print('sentsRead: ', sentsRead)
    else:
        print('sentsRead[0]: ', sentsRead[0])
        
    for s in sentsRead:
        
        print('---')
        print('s: ', s)

        print('-' * 10)
        print('findSVO:')
        saObj, error2 = findSVO(s)
        print('...')
        print('newSA_Obj:')
        saObj.printAll()

        if len(error2) > 0:
            print('findSVO returned an error:')
            for e in error2:
                print(e)

            print('Ignoring input sentence?')
            
        else:
            print('findSVO did not return any errors.')

        saObjList.append(saObj)

        print('-----')

        # Retrive saved conversation window (chatbot)
        #
        if saveConverWin:
            print('Retrieving converWinCol...')
            
            converWinCol = simpDB["ConverWinCol"]

            cursor = converWinCol.find({})
            for c in cursor:
                print('c: ', c)
                
                if firstLoop:
                    if len(c) > 0:
                        print('Copying con to conversationWindow.')
                        con = c["conversationWindow"]
                        conversationWindow = con.copy()


        print('conversationWindow', conversationWindow) 
        firstLoop = False

            
        print('-----')

        # Construct/maitain converstion window
        if len(conversationWindow) <= conversationWindowSize:
            conversationWindow.append(saObj.subject)
        else:
            conversationWindow.pop(0)
            conversationWindow.append(saObj.subject)
 
        print('len conversationWindow: ', len(conversationWindow))
        conCnt = 1
        print('=' * 10)

        
        print(conversationWindow)
        print('-' * 10)
        for con in conversationWindow: 
            print('---: ', conCnt)
            conCnt += 1
            print(con)

        # Determine subject frequency in conversation window
        print('-' * 10)
        grouped_data = {}
        for item in conversationWindow:
            if len(item) > 0:
                key = item[0]
                value = 1
                if key in grouped_data:
                    value += 1
                    grouped_data[key] = value
                else:
                    grouped_data[key] = value

        # Printing the subjects with frequency
        for key, values in grouped_data.items():
            print(key, ":", values)

        print('-' * 10)
        # Save conversation window for chatbot session
        if saveConverWin:
            print('Saving converWinCol...')
            
            converWinCol.drop()

            for c in conversationWindow:
                converWinCol.insert_one({"conversationWindow": c})
        
        print('=' * 10)
        

    print('Read {} sentences.'.format(len(saObjList)))


    print('End:--- assimilate ---')
    
    return 'Great wisdom and understanding'




def addWebWords(taggedSentence):

    wordDefs = ''
    lc_w = ''
    manAdd = []
    
    
    print('addWebWords: we are going to process:')
    print(taggedSentence)
    print('-' * 10)
    print('Check if Simp knows the input words...')

    for w in taggedSentence:
        print('w:')
        print(w)

        if w["tag"] not in ['NNP', 'NNPS']:
            # Is this an inflection or a base word
            wordlower = w["word"]
            wordlower = wordlower.lower()
            wlower = {"word": wordlower, "tag": w["tag"]}

            print('wordlower: ', wordlower)
            print('wlower: ', wlower)
                
            inflectLst = getBaseWordFromInflections2(wordlower) # All inflections are lower case

            if inflectLst[0][0] == 'NONE':
                searchWord = wlower
                print('{} has no inflections.'.format(w["word"]))
                baseWord = 'NONE';
            else:
                print('inflectLst:')
                print(inflectLst)

                if inflectLst[0][0] == w["word"]: # Is a "base word" not an inflection
                    searchWord = wlower
                    print('if scrape web for: ', searchWord)
                    #wordDefs = scrapeWord2((w["word"], w["tag"]))
                else:
                    searchWord = {"word": inflectLst[0][0], "tag": inflectLst[0][1]}
                    baseWord = (inflectLst[0][0], inflectLst[0][1])
                    print('{} is an inflection of {}'.format(w["word"], inflectLst[0][0]))
                    print('else scrape web for: ', searchWord)
                    print('baseWord: ', baseWord)
        else:
            searchWord = w # Keep NNP/S upper case
            print('Not checking for NNP or NNPS inflections...')

        print('searchWord: ', searchWord)
        # Ban-Aid to (Daffy,JJ) issue
        w2 = searchWord["word"].capitalize()
        t2 = searchWord["tag"]
        searchWord2 = {"word": w2, "tag": t2} 
        print('searchWord2: ', searchWord2)
        
        # Does the word exist nominalsKB or webWords?
        if isWordKnown(searchWord):
            print('"{}" is known in nominalsKB.'.format(w["word"]))

        elif isWordKnown(searchWord2):
            print("Possible tagging error")
            print('"{}" is known in nominalsKB as {}.'.format(w["word"], searchWord2["word"]))

        elif isWebWord(searchWord):
            print('"{}" is known in webWords.'.format(w["word"]))
            
        else:
            print('"{}" is completely unknown.'.format(w["word"]))
            if w["word"] in ['.', ',', '!', '?', ';', ':']:
                print('We shall not search for: ', (w["word"], w["tag"]))
            else:
                if searchWord["tag"] in ["NNP", "NNPS"]:
                    print('Need to manualy add NNP/NNPS: ', searchWord)
                    print('w: ', w)
                    if len(list(addNNP.find({"word": searchWord["word"]}))) <= 0:
                        print("INSERTING")
                        addNNP.insert_one(w)
                        manAdd.append(w)
                else:
                    # Hack for trouble words I & is
                    if not isWebWord(w):
                        print('We shall search for: ', (w["word"], w["tag"]))
                        if w["word"] == 'I':
                            wordDefs = scrapeWord2((w["word"], w["tag"]))
                        else:
                            if baseWord != 'NONE':
                                print('Scraping for: ', baseWord)
                                wordDefs = scrapeWord2(baseWord)
                            else:
                                s_word = w["word"].lower()
                                print('Scraping for: Lower cased word for search: ', s_word)
                                wordDefs = scrapeWord2((s_word, w["tag"]))
                    
                        print('wordDefs:')
                        print(wordDefs)
                        print('---')
                        if len(wordDefs) > 0:
                            saveWebWord(wordDefs)
                        else:
                            print('Web search/scrape failed for: ', w)
                    else:
                        print('last check found in webWords.', w)

            print('----')

    # All words should now be in nominalsKB, webWords, or flagged to add to nominalsKB    
    
    return manAdd
#
#
#
if __name__ == "__main__":

    print('Start: assimilate.py (__main__)')
    print('*** assimilate.py is not standalone ***')  
    print('End: assimilate.py (__main__)')  
