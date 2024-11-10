# upDownLevel1.py
# Simple up, down, or level rule
#
import pickle

seaLevel = 0.0

def isUp(y):
    #global seaLevel
    if isinstance(y, float):
        if y > seaLevel:
            return True
    return False

def isDown(y):
    #global seaLevel
    if isinstance(y, float):
        if y < seaLevel:
            return True
    return False

def isLevel(y):
    if isinstance(y, float):
        if not isUp(y) and not isDown(y):
            return True
    return False

def whatIsY(y):
    if isUp(y):
        print('y: {} isUp'.format(y))
        return "isUp"
    elif isDown(y):
        print('y: {} isDown'.format(y))
        return "isDown"
    elif isLevel(y):
        print('y: {} isLevel'.format(y))
        return "isLevel"
    else:
        print('y: {} is unknown'.format(y))
    return "UNKNOWN"

def modifyDict(oldDict):

    newDict = {}
    cnt = 0
    
    for key, value in oldDict.items():
        print('key: {}, value: {}'.format(key, value))
        cnt += 1
        direction = whatIsY(value)
        tmpDict = {
                "name": key,
                "elevation": value,
                "direction": direction
        }
        newDict[cnt] = tmpDict


    return newDict

if __name__ == "__main__":

    #seaLevel = 0.0
    mtHood = 11249.0
    grave = -6.0
    nan = "not a up or down number"

    myDict = {
        'mtHood': mtHood,
        'seaLevel': seaLevel,
        'grave': grave,
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


        
    with open("upDownLevel.p", "wb") as f:
        pickle.dump(newDict, f)
    f.close()

    

