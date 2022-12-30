#
# simpGuess.py
#
# A slight to predictive AI, but we'll play with it
# to provide guessing capability. 
#

import string

import nltk
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pathlib import Path

import warnings
warnings.filterwarnings('ignore')


def guess(s):

    print('--- guess ---')

    h = readHistory()
    sentLst = sentTok(h)

    # Preprocessing
    lemmer = WordNetLemmatizer()
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    # Generating response
    def response(s):
        guess_response=''
        sentLst.append(s)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sentLst)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if(req_tfidf==0):
            guess_response = guess_response+"I am sorry! I don't understand you"
            return guess_response
        else:
            guess_response = guess_response + sentLst[idx]
            return guess_response

    s = s.lower()
    print("Guess response: ",end="")
    print(response(s))

    print('--- End of guess ---')

    return

def readHistory():
    
    fHist  = 'history.txt'
    file = Path(fHist)
    hist = []
    
    if file.is_file():

        fh = open(fHist, 'r')
        myHist = fh.read()
        fh.close()

        lines = myHist.split('\n')

        for line in lines:
            
            if len(line) > 0:
                if line[0] != '#':
                    lineLst = line.split(';')

                    # Rough-hewn, but readable
                    tmp = lineLst[0].replace('[', '')
                    tmp = tmp.replace(']', '')
                    tmp = tmp.replace(' ', '')
                    tmp = tmp.replace("'", "")
                    tmp = tmp.split(',')
                    
                    hist.append(tmp)
    else:
        print('No history file found, created new history file.')
        fh = open(fHist, 'w')
        fh.write('# Input sentence, Possible relationships, Date; Time')
        fh.close()

    return hist

# Conver to a list of sentences for NLTK processing
def sentTok(h):

    listOfSentences = []
    tmpStr = ' '
    
    for i in h:        
        tmpStr = tmpStr.join(i)        
        listOfSentences.append(tmpStr)
        tmpStr = ' ' 

    return listOfSentences

# Conver to a list of words for NLTK processing
def wordTok(sLst):

    listOfWords = []
    tmpStr = ' '
           
    tmpStr = tmpStr.join(sLst)
    listOfWords.append(tmpStr)

    return listOfWords

def rawConvert(lst):

    rawStr = ' '
    rawStr = rawStr.join(lst)

    return rawStr
