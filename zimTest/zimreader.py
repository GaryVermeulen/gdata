from zimscan import Reader
from bs4 import BeautifulSoup


path = "wikipedia_en_simple_all_nopic_2024-06.zim"
counter= 0
bigList = []

with Reader(open(path, "rb"), skip_metadata=True) as reader:
    for record in reader:
        counter += 1
        data = record.read()
        bigList.append(data)
        #print('Count: ', counter)
        #soup = BeautifulSoup(data)
        #if "pronun" in soup:
        #    print('Count: ', counter)
        #    print(soup.get_text())
        #if counter > 100:
        #    break

soupList = []
for i in bigList:
    soup = BeautifulSoup(i)
    soupList.append(soup.get_text())

    
print("Total count: ", counter)
print("len bigList: ", len(bigList))
print("len soupList: ", len(soupList))

print("\nFIN")
