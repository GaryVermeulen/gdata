# leftRight1.py
# Simple left or right rule
# Less than zero equals left
# Greater than zero equlas right
#

import pickle

def isRight(x):
    #global zero
    if isinstance(x, float):
        if x > zero:
            return True
    return False

def isLeft(x):
    if isinstance(x, float):
        if x < zero:
            return True
    return False

def isNeither(x):
    if isinstance(x, float):
        if not isRight(x) and not isLeft(x):
            return True
    return False

def modifyDict(oldDict):

    newDict = {}
    cnt = 0
    
    for key, value in oldDict.items():
        print('key: {}, value: {}'.format(key, value))
        cnt += 1
        direction = whatIsX(value)
        tmpDict = {
                "name": key,
                "direction": direction
        }
        newDict[cnt] = tmpDict
    return newDict

def whatIsX(x):
    whatIsX = ''
    if isLeft(x):
        print('x: {} isLeft'.format(x))
        whatIsX = "isLeft"
    elif isRight(x):
        print('x: {} isRight'.format(x))
        whatIsX = "isRight"
    elif isNeither(x):
        print('x: {} isNeither'.format(x))
        whatIsX = "isNeither"
    else:
        print('x: {} is unknown'.format(x))
        whatIsX = "UNKOWN"

    return whatIsX

if __name__ == "__main__":


    zero = 0.0
    east = 10.0
    west = -10.0
    utc = 0.0
    nan = "not a left or right number"

    myDict = {
        'zero': zero,
        'east': east,
        'west': west,
        'utc': utc,
        'nan': nan
    }

    print(myDict)
    print('-----')
    
    newDict = modifyDict(myDict)
    print(newDict)
    print('-----')

    for key, val in newDict.items():
        print('key: ', key)
        print('val: ', val)

    with open("leftRight.p", "wb") as f:
        pickle.dump(newDict, f)
    f.close()
