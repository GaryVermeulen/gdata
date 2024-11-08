# sr2.py
# Simple Rules v2
# Basic (base rule set) rule, and attempt to add/modify/replace with new data
#

import pickle

class myRule:
    def __init__(self, name, limit, value, result):
        self.name = name
        self.limit = limit
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

    def whatIsVale(self):
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
        print('limit: ', self.limit)
        print('value: ', self.value)
        print('result: ', self.result)

if __name__ == "__main__":

    seaLevel = 0
    mtHood = 11249
    grave = -6
    nan = "not a number"

    myRuleObj = myRule(None, None, None, None)
    
    myRuleObj.printAll()
    myRuleObj.whatIsVale()

    print('------------')
    myRuleObj.name = "Mount Hood"
    myRuleObj.limit = 0.0
    myRuleObj.value = 11249.0
    myRuleObj.result = None

    myRuleObj.printAll()
    myRuleObj.whatIsVale()    
