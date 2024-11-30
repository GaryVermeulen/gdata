# testFunctions.py
# Test the DNA functions

import random
import cell1DNA as c1




if __name__ == "__main__":

    whoami = __file__

    c1.isNumPrime1(2)

    num0 = 0
    num1 = 0
    for i in range(1, 120):
        print(i, end = ' ')
        random_int = random.randint(0, 1)
        if random_int == 1:    
            num1 +=1
            print('1', end = ' ')
        else:
            num0 += 1
            print('0', end = ' ')

        # P% * X = Y
        # P = 10% (If 10% or less then starving
        #
        X = 120
        Y = num1
        P = Y / X
        print("What % of {} is {}? {} or {}".format(X, Y, P, round(P*100)))
        

            
    print("\nTotal num1: ", num1)
    print("Total num0: ", num0)
    print("Total num0 + num1: ", num0 + num1)

    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    newStr = whoami[:res[-1]]
    print(newStr)
    

