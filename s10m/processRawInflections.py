#
# processRawInflections.py
#

from commonUtils import connectMongo


def loadInflFile():

    inflections = []
    cnt = 1
    k = 1000

    with open('data/infl.txt', 'r') as f:
            while (line := f.readline().rstrip()):
                line = line.strip()
                line = line.split(' ')
                inflections.append(cleanLine(line))
                if (cnt % k) == 0:
                    print('k', end = '')
                #else:
                #    print('.', end = '')
                cnt += 1
    f.close()

    return inflections


def cleanLine(line):

    cleanedLine = []
    
    for x in line:
        cX = x.strip()
        cX = cX.replace(':', '')
        cX = cX.replace('?', '')
        cX = cX.replace('~', '')
        cX = cX.replace(',', '')
        cX = cX.replace('<', '')
        cX = cX.replace('>', '')
        
        if cX.isalpha():
            cX = cX.lower()
            cleanedLine.append(cX)

    return cleanedLine


def add2DB(i):

    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    inflections = simpDB["inflections"]

    inflections.drop() # For now start fresh each run

    for line in i:
        inflections.insert_one({"inflections": line})


    return "Added inflections to simp DB."




if __name__ == "__main__":

    print("Start processRawInflections (__main__)")
    i = loadInflFile()
    print('\nAdding {} inflections to DB...'.format(len(i)))
    print(add2DB(i))

    
    """
    cnt = 1
    for x in i:
        print(cnt, x)
        cnt += 1

    print('len i: ', len(i))
    print('type i: ', type(i))

    """

    print("Completed processRawInflections (__main__)")
    
