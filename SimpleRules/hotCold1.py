# hotCold1.py
# Simple hot or cold rule
#

import pickle

freeze = 32.0

def isHot(y):
    if isinstance(y, float):
        if y > freeze:
            return True
    return False

def isCold(y):
    if isinstance(y, float):
        if y < freeze:
            return True
    return False

def isNeither(y):
    if isinstance(y, float):
        if not isHot(y) and not isCold(y):
            return True
    return False

def whatIsY(y):
    whatIsY = ''
    if isHot(y):
        print('y: {} isUp'.format(y))
        whatIsY = "isHot"
    elif isCold(y):
        print('y: {} isDown'.format(y))
        whatIsY = "isCold"
    elif isNeither(y):
        print('y: {} isNeither'.format(y))
        whatIsY = "isNeither"
    else:
        print('y: {} is unknown'.format(y))
        whatIsY = "UNKOWN"
    return whatIsY

def modifyDict(oldDict):

    newDict = {}
    cnt = 0
    
    for key, value in oldDict.items():
        print('key: {}, value: {}'.format(key, value))
        cnt += 1
        toTouch = whatIsY(value)
        tmpDict = {
                "name": key,
                "temperature": value,
                "toTouch": toTouch
        }
        newDict[cnt] = tmpDict


    return newDict

if __name__ == "__main__":

    bodyTemp = 98.6
    bakedBread = 200.0
    iceCream = 0.0
    kelvin = -459.67
    freezePoint = freeze
    nan = "not a hot or cold number"

    myDict = {
        'freezePoint': freezePoint,
        'bodyTemp': bodyTemp,
        'bakedBread': bakedBread,
        'iceCream': iceCream,
        'Kelvin': kelvin,
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

    with open("hotCold.p", "wb") as f:
        pickle.dump(newDict, f)
    f.close()

