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

            if line[0] == 'NNP':
                s = line[1].split('|')
#                nouns.append(s)
                       
    fin.close()

    print('s:' + str(s))

    
    return(s)

#myNouns = []

myNouns = getNouns()

print(myNouns)
print(len(myNouns))

