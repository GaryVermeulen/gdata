#
# checkPickles.py
#

import pickle
from commonConfig import Sentence


def getSA_Pickle():

    with open('pickles/sA_Obj.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded sA_Obj.pkl')
    fp.close()
    
    return ourPickle


def getNewWords_Pickle():

    with open('pickles/newWords.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newWords.pkl')
    fp.close()
    
    return ourPickle

    

def savePickle(p):
    
    with open('pickles/sA_Obj.pkl', 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a sA_Obj pickle')
    fp.close()
    


if __name__ == "__main__":

    print('Pickle checker...')
    
    ourPickle = getNewWords_Pickle()

    print('ourPickle:')
    print(type(ourPickle))
    print(ourPickle)

    # For SA Pickle
    #print(ourPickle.printAll())

    # For newWords list
    print(len(ourPickle))
    for i in ourPickle:
        print("-" * 10)
        print(i)

    

