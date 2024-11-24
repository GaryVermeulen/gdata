# fileNameTest.py
#



if __name__ == "__main__":

    num = 234
    testChar = "/"
    whoami = __file__

    print("Original String: ", whoami)
    
    # Using list comprehension
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)] 

    print("res: ", res)

    newStr = whoami[:res[-1]]

    print("newStr: ", newStr)

    newFile = newStr + "/replicants/rep" + str(num) + ".py"

    print("newFile: ", newFile)
    
    #baseStr = whoami[:-3] # remove the .py
    #newStr = baseStr + str(num) + ".py"
    #print("newStr: ", newStr)
