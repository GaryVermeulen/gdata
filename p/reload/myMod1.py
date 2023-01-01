#
# myMod1, module reload testing
#

def myFun1(i):

    myFun1Var = 40

    print('In myFun1 with {} and {}'.format(i, myFun1Var))

    if i == "Cat":
        print('{} = Cat'.format(i))
        o = 'myFun1 output with ' + str(i) + ' and ' + str(myFun1Var)
    elif i == "Dog":
        print('{} = Dog'.format(i))
        o = 'myFun1 output with ' + str(i) + ' and ' + str(myFun1Var)
    elif i == "Bob":
        o = 'myFun1 output with ' + str(i) + ' and ' + str(myFun1Var)
    else:
        print('{} is undefined'.format(i))
        o = 'Undefined'

    return o

#
# Main
#
if __name__ == "__main__":

    x = myFun1('Bob')

    print("myFun1: ", x)

