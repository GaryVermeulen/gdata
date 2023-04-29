#
# listTaggedWords.py
#

import pickle



def getNewTaggedList():

    with open('newTaggedList.pkl', 'rb') as fp:
        newTaggedList = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()

    return newTaggedList

if __name__ == "__main__":

    print('Current newTaggedList.pkl contents...')
    
    taggedList = getNewTaggedList()

    counter = 0
    for tag in taggedList:
        counter += 1
        #print(counter, tag)
        
        #if tag[1] in ['NN', 'NNS', 'NNP']:
        #    print(tag)
        
        if tag[0] == 'you':    
            print('at counter {} found {}'.format(counter, tag))
