# sr2.py
# Simple Rules v2
# Basic (base rule set) rule, and attempt to add/modify/replace with new data
#

import pickle
import sys

class accumulateFacts:
    def __init__(self, name, limitName, limit, units, descriptor, value, result):
        self.name = name
        self.limitName = limitName
        self.limit = limit
        self.units = units
        self.descriptor = descriptor
        self.value = value
        self.result = result
             
    def isGreater(self):
        if isinstance(self.value, float):
            if self.value > self.limit:
                return True
        return False

    def isLess(self):
        if isinstance(self.value, float):
            if self.value < self.limit:
                return True
        return False

    def isEqual(self):
        if isinstance(self.value, float):
            if not self.isGreater() and not self.isLess():
                return True
        return False

    def whatIsValue(self):
        if self.isGreater():
            print('value: {} isGreater than limit: {}'.format(self.value, self.limit))
            self.result = "Greater"
        elif self.isLess():
            print('value: {} isLess than limit: {}'.format(self.value, self.limit))
            self.result = "Less"
        elif self.isEqual():
            print('value: {} isEqual to limit: {}'.format(self.value, self.limit))
            self.result = "Equal"
        else:
            print('value: {} is unknown; limit {}'.format(self.value, self.limit))
        return

    def printAll(self):
        print('name: ', self.name)
        print('limitName: ', self.limitName)
        print('limit: ', self.limit)
        print('units: ', self.units)
        print('descriptor: ', self.descriptor)
        print('value: ', self.value)
        print('result: ', self.result)

def findLimit(descriptor):

    limit = {}

    try:
        limits = pickle.load(open('limits.p', 'rb'))
        
    except FileNotFoundError:
        sys.exit("The file limits.p does not exist.")

    # Better be a list fo dictionaries
    for l in limits:
        if l["descriptor"] == descriptor:
            return l

    return limit


if __name__ == "__main__":

    #seaLevel = 0
    thingName = "Mount Hood"
    thingValue = 11249.0
    thingDescriptor = 'height'
    #grave = -6
    #nan = "not a number"

    limit = findLimit(thingDescriptor)

    if len(limit) <= 0:
        sys.exit("limit for: {} Not found.".format(thingDescriptor))
    else:
        print("descriptor limit found: ", limit)
        first_key = next(iter(limit))
        val = limit[first_key]
        print('first key: {}; value: {}'.format(first_key, val))

    factObj = accumulateFacts(None, None, None, None, None, None, None)
    
    factObj.printAll()
    factObj.whatIsValue()

    print('------------')

    factObj.name = thingName
    factObj.limitName = first_key
    factObj.limit = val
    factObj.units = limit["units"]
    factObj.descriptor = thingDescriptor
    factObj.value = thingValue
    factObj.result = None
    
    factObj.printAll()
    factObj.whatIsValue()
    print('-----')
    factObj.printAll()
