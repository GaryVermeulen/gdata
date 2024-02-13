#
# processRawPronouns.py
#
# Reads text file and builds a Mongo collection
#

from commonUtils import connectMongo

def loadFile():

    # Expects file structure:
    """
    # https://www.thefreedictionary.com/List-of-pronouns.htm
    subject:I,we,you,he,she,it,they
    object:me,us,you,her,him,it,them
    """
    cnt = 0
    lines = []
    totalLines = 0

    with open('data/pronouns.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] != '#':
                lines.append(line)
                cnt += 1
            totalLines += 1
    f.close()

    print('Processed {} lines, and kept {} lines.'.format(totalLines, cnt))

    return lines

def processLines(lines):

    dictList = []

    for line in lines:
        tLst = []
        l = line.split(':')
        key = l[0]
        val = l[1].split(',')
        tLst.append(key)
        tLst.append(val)
        dictList.append(tLst)

    return dictList

def processRawPronouns():

    l = loadFile()
    ld = processLines(l)

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    pronounsCol = simpDB["pronounsCol"]
    pronounsCol.drop() # For now start fresh each run
    
    for x in ld:
        print(x)
        d = {"type": x[0], "pronouns": x[1]}
        pronounsCol.insert_one(d)


if __name__ == "__main__":


    processRawPronouns()    

