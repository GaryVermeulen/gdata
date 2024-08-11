# using naive method

# initializing list
startList = [{"word": "cat", "tag": "NN"}, {"word": "dog", "tag": "NN"}, {"word" : "bat", "tag": "NN"},
             {"word": "sat", "tag": "VBD"}, {"word": "cat", "tag": "NN"}, {"word" : "hat", "tag": "NN"},
             {"word": "cat", "tag": "NN"}, {"word" : "bat", "tag": "NN"}]

print("startList:")
print(startList)
print('----------')
# using naive method to
# count dupicates
tmpList = []
chkList = []
resList = []
count = 0
index = 0

for d in startList:
    count += 1    
    print("count: {};  d: {}".format(count, d))
    print("index: {};  startList[index]: {}".format(index, startList[index]))

    if len(tmpList) == 0:
        tmpList.append((1, d))
        chkList.append(d)
        print("0 tmpList:")
        print(tmpList)

    else:
        print("else tmpList:")
        print(tmpList)

        tCnt = 0
        for t in tmpList:
            tCnt = += 1
            

               

            
        """
            if d["word"] == t["word"]:
                tIndex = tmpList.index(d)
                popped = tmpList.pop(tIndex)
                print("appending modified")
                tmpList.append({"word": popped["word"], "count": popped["count"] + 1})
                break
            else:
                print("appending d")
                tmpList.append(d)
                break
        """
        print('...')
    print("tmpList:")
    print(tmpList)

    index += 1

    print('---')
    

print('----')
for tl in tmpList:
    print(tl)

    
# printing resultant list
#print ("Resultant list is : " + str(res_list))
