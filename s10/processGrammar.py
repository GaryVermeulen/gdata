#
# processGrammar.py
#

import pickle
import spacy


def getPickles():

    with open('data/newDict.pkl', 'rb') as fp:
        topicalDict = pickle.load(fp)
        print('Aunt Bee loaded newDict.pkl')
    fp.close()

    with open('data/ourCorpus.pkl', 'rb') as fp:
        topicalCorpus = pickle.load(fp)
        print('Aunt Bee loaded ourCorpus.pkl')
    fp.close()
    

    return topicalDict, topicalCorpus


if __name__ == "__main__":

    docs = []
    print('Processing grammar...')

    topicalDict, topicalCorpus = getPickles()

    print('len topicalDict: ', len(topicalDict))
    print('type topicalDict: ', type(topicalDict))
#    for x, y in topicalDict.items():
#        print('x: {} y: {}'.format(x,y))
    
    print('len topicalCorpus: ', len(topicalCorpus))
    print('type topicalCorpus: ', type(topicalCorpus))
    print('-' * 5)

    nlp = spacy.load("en_core_web_lg") # Going for the best accuracy
    for sentence in topicalCorpus:
        strSentence = ' '.join(sentence)
        print(strSentence)
        doc = nlp(strSentence)
        print('doc: ', doc)
        for token in doc:
            print('token.text: ', token.text)

            chkToken = token.text + '_1' 
            print('chkToken: ', chkToken)

            if chkToken in topicalDict:
                print(topicalDict[chkToken])
                
#                if chkToken == token.text:
#                    print(word, topicalDict(word))
#                else:
#                    print('not found')
                
            print(f'{token.text:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
#        docs.append(doc)
        
