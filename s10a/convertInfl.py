#
# convertInfl.py
#

import pickle

def loadInflFile():

    inflections = []

    with open('data/infl.txt', 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.strip()
                line = line.split(' ')
                inflections.append(cleanLine(line))
    f.close()

    return inflections


def cleanLine(line):

    cleanedLine = []
    
    for x in line:
        cX = x.strip()
        cX = cX.replace(':', '')
        cX = cX.replace('?', '')
        cX = cX.replace('~', '')
        cX = cX.replace(',', '')
        cX = cX.replace('<', '')
        cX = cX.replace('>', '')
        
        if cX.isalpha():
            cX = cX.lower()
            cleanedLine.append(cX)

    return cleanedLine




if __name__ == "__main__":


    i = loadInflFile()

    # Save inflection pickle...
    with open('pickles/inflections.pkl', 'wb') as fp:
        pickle.dump(i, fp)
        print('Aunt Bee made a inflections pickle')
    fp.close()

    
    cnt = 1
    for x in i:
        print(cnt, x)
        cnt += 1

    print('len i: ', len(i))
    print('type i: ', type(i))
