# using naive method

def search(name, people):
    return [element for element in people if element['word'] == name]


def processList(inputList):

    global resList

    if len(inputList) <= 0:
#        print("NO INPUT")
        return
#    else:
#        print("inputList: ", inputList)
    
    workList = inputList.copy()

    for i in workList:

#        print('i: ', i)

        searchItem = i["word"]

#        print('searchItem: ', searchItem)

        tmpList = search(searchItem, workList)

#        print('tmpList: ', tmpList)

        tmpListLen = len(tmpList)

        if tmpListLen > 0:
            resList.append((tmpListLen, i))
#            print('resList append: ', resList)

        for j in tmpList:
#            print('j: ', j)
            tIndex = workList.index(j)
#            print('tIndex: ', tIndex)
            popped = workList.pop(tIndex)
#            print('popped: ', popped)
#        print('----')

#    print('workList: ', workList)
    
    processList(workList)

    return


# initializing list
startList = [{"word": "cat", "tag": "NN"}, {"word": "dog", "tag": "NN"}, {"word" : "bat", "tag": "NN"},
             {"word": "sat", "tag": "VBD"}, {"word": "cat", "tag": "NN"}, {"word" : "hat", "tag": "NN"},
             {"word": "cat", "tag": "NN"}, {"word" : "bat", "tag": "NN"}]

print("startList:")
print(startList)
print('----------')

#tmpList = []
workList = startList.copy()
resList = []
#count = 0
#index = 0

print("start workList:")
print(workList)
print('----------')

processList(workList)
    

print('-----------')
print(resList)
print('-----------')
print(workList)

