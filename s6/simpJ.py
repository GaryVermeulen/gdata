import json
import os
from pathlib import Path


def readJSON():
    
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

    d = data.values()
    
    return(d)

if __name__ == "__main__":

    d = readJSON()

    print('----')


    for x in d: v = x   


    for y in v:
        print(y)
        print(' ', y.keys())
        print(' ', y.values())
    
