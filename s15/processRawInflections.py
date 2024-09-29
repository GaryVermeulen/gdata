#
# processRawInflections.py
#
# My corny simplistic version of pyinflect.
# Loads inflections from pyinflect's infl.txt file and places
# them in a MongoDB.
#

from commonUtils import connectMongo


def loadInflFile():

    inflections = []
    cnt = 1
    k = 1000

    with open('inputData/infl.txt', 'r') as f:
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
    inflectionsCol = simpDB["inflectionsCol"]

    inflectionsCol.drop() # For now start fresh each run

#    for line in i:
#        inflectionsCol.insert_one({"inflections": line})

    
    inflectionsCol.insert_many(i)

    return "Added inflections to simp DB."



def formatInflections(i):

    dictionaryList = []
    keys = []

    for x in i:
#        print(len(x))
#        print(x)

        if len(x) > 2:
            if x[1] == 'n':
                tag = 'NN'
            elif x[1] == 'v':
                tag = 'VB'
            elif x[1] == 'a':
                tag = 'JJ' # Lumps RB's into JJ
            else:
                tag = 'UNK'

            inflect = x[2:]
            inflect.append(x[0]) # Hack to make base word searching easier

#            print('x: ', x)
#            print('inflect: ', inflect)
            
##            d = {"_id": x[0], "tag": tag, "inflections": inflect}
            d = {"word": x[0], "tag": tag, "inflections": inflect}

            #if x[0] not in keys:
            #    dictionaryList.append(d)
            #keys.append(x[0])
            #
            # Need to keep all words since some are nouns and verbs
            dictionaryList.append(d)

    return dictionaryList



if __name__ == "__main__":

    print("Start processRawInflections (__main__)")
    i = loadInflFile()
    
    print("\nFormatting inflections list (i) to list of dictionaries")
    i = formatInflections(i)
    
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
    
