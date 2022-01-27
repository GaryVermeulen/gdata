#
# Test bed
#

fCFG = '/home/gary/src/simpleton/simpPTPoS.cfg'
fRMode = 'r'

def getNouns():

    nouns = []

    with open(fCFG, fRMode) as fin:
        
        while (line := fin.readline().rstrip()):

            line = line.replace("-", '')
            line = line.replace(" ", '')

            line = line.split(">")

            print(line)

            if line[0] == 'NN':
                nouns.append(line)
                       
    fin.close()

    print(nouns)
    return(nouns)

myNouns = []

myNouns = getNouns()

print(myNouns)

