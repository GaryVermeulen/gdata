#
# buildDict.py
#

import os
import spacy
import pickle


def getData():
    # Read the test files
    corpusList = []
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r') as f:
            while (line := f.readline().rstrip()):
                corpusList.append(line)
    f.close()

    return corpusList


def getRawData():
    # Read the test files
    corpusStr = ''
    progPath = os.getcwd()
    dataPath = progPath + '/Corpus'
    dirList = os.listdir(dataPath)

    for inFile in dirList:
        with open(dataPath + '/' + inFile, 'r') as f:
            while (line := f.readline().rstrip()):
                corpusStr += line
    f.close()

    return corpusStr


def buildList(corpus):
    # Build a POS tagged lexicon from the input corpus
    wordList = []

    for line in corpus:
        line = line.replace('.', '') # Ugly but simple
        line = line.replace(',', '')
        line = line.replace('!', '')
        line = line.replace('?', '')
        line = line.replace('"', '')
        line = line.replace('-', ' ')
        line = line.replace(':', '')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace(';', '')
        
        cleanedLine = line.split()
        
        for word in cleanedLine:
            word = word.lower()
            # Kind of heavy handed, but some " were getting past the .replace
            cleanedWord = ''.join(x for x in word if x.isalnum())
            
            if cleanedWord not in wordList:
                if len(cleanedWord) > 0:
                    wordList.append(cleanedWord)

    return wordList


def buildDict(words):

    myDict = {}

    strWords = str(words)
    strWords = strWords.replace("'", "")
    strWords = strWords.replace("'", "")
    strWords = strWords.replace("[", "")
    strWords = strWords.replace("]", "")
    strWords = strWords.replace(",", "")

    taggedWords = nlp(strWords)

    for token in taggedWords:
        attributes = {"POS": token.pos_, "Tag": token.tag_, "TagExplain": spacy.explain(token.tag_), "Lemma": str(token.lemma_)}
        myDict.update({token.text: attributes})


    return myDict, taggedWords


def buildSentences():
    nlp = spacy.load("en_core_web_sm")
    corpus = getRawData()

    print('corpus:')
    print(len(corpus))
    print(type(corpus))

    
    doc = nlp(str(corpus))
    sentences = list(doc.sents)

    return sentences


if __name__ == "__main__":

#    nlp = spacy.load("en_core_web_sm")
#    verbose = True
#    text_corpus = getData()

#    print('nlp type: ', type(nlp))
#    
#    print('text_corpus:')
#    print(len(text_corpus))
#    print(type(text_corpus))

#    if verbose:
#        for t in text_corpus:
#            print(t)

#    words = buildList(text_corpus)

#    print('words:')
#    print(len(words))
#    print(type(words))

    
#    print(f"{'text':{8}} {'POS':{6}} {'TAG':{6}} {'Dep':{6}} {'POS explained':{20}} {'tag explained'} ")
#
#    for token in taggedWords:
#        print(f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_):{40}} {str(token.lemma_)}')
#        attributes = {"POS": token.pos_, "Tag": token.tag_, "TagExplain": spacy.explain(token.tag_), "Lemma": str(token.lemma_)}
#        myDict.update({token.text: attributes})

#    myDict, taggedWords = buildDict(words)

#    print('myDict len: ', len(myDict))
#    print('taggedWords type: ', type(taggedWords))
    
#    for x, y in myDict.items():
#        print(x, y)


#    with open('myDict.pkl', 'wb') as fp:
#        pickle.dump(myDict, fp)
#        print('made a dictionary pickle')
#    fp.close()
#
#    with open('taggedWords.pkl', 'wb') as fp:
#        pickle.dump(taggedWords, fp)
#        print('made a taggedWords pickle')
#    fp.close()

#    print('-' * 5)
#
#    with open('myDict.pkl', 'rb') as fp:
#        newDict = pickle.load(fp)
#        print('made new pickle')
#    fp.close()

#    for x, y in newDict.items():
#        print(x, y)
    
#    with open('taggedWords.pkl', 'rb') as fp:
#        newTaggedWords = pickle.load(fp)
#        print('loaded taggedWords pickle')
#    fp.close()
#
#    print(type(newTaggedWords))

    
    sentences = buildSentences()

    print(len(sentences))
    print(type(sentences))

    for s in sentences:
        print(s)
