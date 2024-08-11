# using naive method

# initializing list
test_list = [{"Akash" : 1}, {"Kil" : 2}, {"Akshat" : 3},
             {"Kil" : 2}, {"Akshat" : 3}, {"Akash" : 1}]

# printing original list
print ("Original list : " + str(test_list))

# using naive method to
# remove duplicates
res_list = []
for i in range(len(test_list)):
    if test_list[i] not in test_list[i + 1:]:
        res_list.append(test_list[i])

# printing resultant list
print ("Resultant list is : " + str(res_list))
