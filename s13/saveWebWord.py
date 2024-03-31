#
# saveWebWords.py
#
#   Group scrapped words by POS and save them to webWords.
#

import pickle

from commonConfig import nn, vb, rb, jj, prp
from commonUtils import connectMongo

# word: 'scrappedWord'
# tags: ['NN', 'VB', ...] (A quick check)
# {tag: 'TAG1', definition: ["the word means...", "the word does...", ...]} 
#   ...
# {tag: 'TAGn', definition: ["the word means...", "the word does...", ...]} 

def packageDefs(w):

    wordDef = {}
    word = ''
    tags = []
    tmp = []

    for wd in w:
        word = wd["word"]
        if wd["tag"] not in tags:
            tags.append(wd["tag"])
        tmp.append(wd)

    wordDef = {"word": word, "tags": tags, "allDefs": tmp}

    return wordDef


def saveWebWord(w):
    mdb = connectMongo()
    simpDB = mdb["simp"]
    webWords = simpDB["webWords"]

    """
    res = input('Drop webWords collection <Y/n>? ')

    if res in ['Y', 'y']:
        webWords.drop()
        print('webWords collection dropped.')
    """
    
    wordDef = packageDefs(w)

    print('wordDef:')
    print(wordDef)
        
    results = webWords.insert_one(wordDef)
    print('insert results: ', results.inserted_id)
    

if __name__ == "__main__":

    print('--- saveWebWord.py -- __main__ ')

    webResults = [
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to touch (a body part, a person, etc.) lightly so as to excite the surface nerves and cause uneasiness, laughter, or spasmodic movements'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to excite or stir up agreeably please'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to provoke to laughter or merriment amuse'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to touch or stir gently'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to have a tingling or prickling sensation'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to excite the surface nerves to prickle'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'the act of tickling'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'a tickling sensation'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'something that tickles'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to touch a body part lightly so as to cause uneasiness, laughter, or jerky movements'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to have a tingling or prickling sensation'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to excite or stir up agreeably please'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to stir to laughter or merriment'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'the act of tickling'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'a tickling sensation'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'something that tickles'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to have a tingling or prickling sensation'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to excite the surface nerves to prickle'},
        {'word': 'tickle', 'tag': 'VB', 'definition': 'to touch (as a body part) lightly so as to excite the surface nerves and cause uneasiness, laughter, or spasmodic movements'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'the act of tickling'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'a tickling sensation'},
        {'word': 'tickle', 'tag': 'NN', 'definition': 'something that tickles'}
        ]


    saveWebWord(webResults)
            
    print('--- saveWebWord.py -- __main__ ')
