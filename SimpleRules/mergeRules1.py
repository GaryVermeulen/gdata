# mergeRules1.py
# But why? Because I can ;-)
#
import pickle
import upDownLevel1
from upDownLevel1 import whatIsY

def loadRules():
    global upDownLevel
    global hotCold
    global leftRight
    
    upDownLevel = pickle.load(open('upDownLevel.p', 'rb'))
    hotCold = pickle.load(open('hotCold.p', 'rb'))
    leftRight = pickle.load(open('leftRight.p', 'rb'))
    
    return




if __name__ == "__main__":
    
    upDownLevel = {}
    hotCold = {}
    leftRight = {}

    newData = {
        'name': 'airPlane',
        'ceilingAlt': 30000.0,
        'currentAlt': 0.0
    }
    
    loadRules()

    direction = whatIsY(newData["currentAlt"])

    print('direction: ', direction)

    for cntKey, val in upDownLevel.items():
        print('cntKey: {}, val: {}'.format(cntKey, val))
        print('nextKey:', cntKey + 1)

    #print(upDownLevel)
    #print(hotCold)
    #print(leftRight)

    
