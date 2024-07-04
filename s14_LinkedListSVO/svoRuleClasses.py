# Classes containing SVO rules

from commonConfig import Sentence, nnx, prpx, vbx

# Create a simple data class to store
# a wee bit more complex data within
# node of LL

class Data:
    def __init__(self, ruleNumber, ruleCondition, result):
        self.ruleNumber    = ruleNumber
        self.ruleCondition = ruleCondition
        self.result        = result

    def printData(self):
        print('ruleNumber:    ', self.ruleNumber)
        print('ruleCondition: ', self.ruleCondition)
        print('result:        ', self.result)



