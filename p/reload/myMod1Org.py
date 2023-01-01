#
# myMod1, module reload testing
#

def myFun1(i):

    myFun1Var = 10

    print('In myFun1 with {} and {}'.format(i, myFun1Var))

    o = 'myFun1 output with ' + str(i) + ' and ' + str(myFun1Var)

    return o

#
# Main
#
if __name__ == "__main__":

    x = myFun1(9)

    print("myFun1: ", x)
    
