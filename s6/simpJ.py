import json
import os
from pathlib import Path


kbFile   = 'simpKB2.json'
progPath = os.getcwd()
dataPath = progPath + '/kb'

file = Path(dataPath + '/' + kbFile)

if file.is_file():

    with open(file, "r") as jfile:
        data = json.load(jfile)

    jfile.close()

else:
    print("File not found: " + str(dataPath + '/' + kbFile))
    sys.exit("KB (JSON) file not found")





for x in data.values():
    v = x   

print(len(v))
print(type(v))
print(v)

print('----')

for y in v:
    print(y)
    print(y.keys())
    print(y.values())
#    print(type(y))
    
