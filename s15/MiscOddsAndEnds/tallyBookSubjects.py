# tallyBookSubjects.py

resList = []

def search(searchValue, listOfDicts):
    return [element for element in listOfDicts if element['word'] == searchValue]



# Come to find out--must resolve pronouns first :-(
def processBookSubjects(inputList, resList):

    #global resList

    if len(inputList) <= 0:
        print("NO INPUT")
        return resList
    else:
        print("INPUT: ", inputList)

    workList = inputList.copy()

    for i in workList:
        print('i: ', i)
        
        searchItem = i["word"]
        tmpList = search(searchItem, workList)

        tmpListLen = len(tmpList)

        if tmpListLen > 0:
            resList.append((tmpListLen, i))

        for j in tmpList:
            tIndex = workList.index(j)
            popped = workList.pop(tIndex)

        resList = processBookSubjects(workList, resList)
        
    return resList


def tallyBookSubjects(epistropheSents):

    #global resList
    subjectOnly = []
    resList = []
    
    for s in epistropheSents:
        
        for sub in s.subject:
            subjectOnly.append({"word": sub["word"], "tag": sub["tag"]})

    #for s in subjectOnly:
    #    print(s)

    workingList = subjectOnly.copy()

    for w in workingList:
        print('w: ', w)

    resList = processBookSubjects(workingList, resList)

    for r in resList:
        print('r: ', r)


 
    #processBookSubjects(workingList)

    #for r in resList:
    #    print('r: ', r)
    
    #resList = []
    
        #workingList = subjectOnly.copy()

        
        
        
        


        
#        processBookSubjects(workingList)
#
#        outputBooks.append((bookName, resList))
#        resList = []

    

    return None


if __name__ == "__main__":

    print('Not standalone')

