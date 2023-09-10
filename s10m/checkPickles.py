#
# checkPickles.py
#

import pickle
from commonConfig import Sentence


def getPickle():

    with open('pickles/sA_Obj.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded sA_Obj.pkl')
    fp.close()
    
    return ourPickle
    

def savePickle(p):
    
    with open('pickles/sA_Obj.pkl', 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a sA_Obj pickle')
    fp.close()
    


if __name__ == "__main__":

    print('Pickle checker...')
    
    ourPickle = getPickle()

    print('ourPickle:')
    print(type(ourPickle))
    print(ourPickle)
    print(ourPickle.printAll())

    

