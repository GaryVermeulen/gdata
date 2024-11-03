# sr1.py
# Simple Rules v1
# Basic (base rule set) rule, and attempt to add/modify/replace with new data
#

def isUp(y):
    if isinstance(y, int):
        if y > 0:
            return True
    return False

def isDown(y):
    if isinstance(y, int):
        if y < 0:
            return True
    return False

def isLevel(y):
    if isinstance(y, int):
        if not isUp(y) and not isDown(y):
            return True
    return False

def whatIsY(y):
    if isUp(y):
        print('y: {} isUp'.format(y))
    elif isDown(y):
        print('y: {} isDown'.format(y))
    elif isLevel(y):
        print('y: {} isLevel'.format(y))
    else:
        print('y: {} is unknown'.format(y))
    return

if __name__ == "__main__":

    seaLevel = 0
    mtHood = 11249
    grave = -6
    nan = "not a number"

    myDict = {
        'mtHood': mtHood,
        'seaLevel': seaLevel,
        'grave': grave,
        'nan': nan
    }

    whatIsY(myDict.get('mtHood'))
    whatIsY(myDict.get('seaLevel'))
    whatIsY(myDict.get('grave'))
    whatIsY(myDict.get('nan'))
    
