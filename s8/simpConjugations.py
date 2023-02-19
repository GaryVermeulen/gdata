#
# simpConjugations.py -- A lightweight version of pyinflect
#

vbFile = '/home/gary/src/s8/data/vb'
vbdFile = '/home/gary/src/s8/data/vbd'
vbgFile = '/home/gary/src/s8/data/vbg'
vbnFile = '/home/gary/src/s8/data/vbn'
vbpFile = '/home/gary/src/s8/data/vbp'
vbzFile = '/home/gary/src/s8/data/vbz'

vbFileList = [vbFile, vbdFile, vbgFile, vbnFile, vbpFile, vbzFile]


def buildVBs(word):

    allVBs = []
    
    for inFile in vbFileList:
        with open(inFile, "r") as f:
            while (line := f.readline().rstrip()):
                if '#' not in line:
                    allVBs.append(line)
        f.close()

    return allVBs

def getInflections(allVBs, word):

    wordInflections = []
    allVBsSet = set(allVBs)

    for v in allVBsSet:
        if word in v:
            print('found: {} in: {}'.format(word, v))
            wordInflections.append(v)

    return wordInflections


def findBaseWord(word):

    baseWord = ''

    print('findBaseWord, word: ', word)
    
    


    return baseWord

#
#
if __name__ == "__main__":

    w = 'walk'
    allVerbs = buildVBs(w)

    bw = findBaseWord(w)

    print('------')
    print('bw: ', bw)
    
    inflections = getInflections(allVerbs, w)

    print(allVerbs)
    print('-------')
    print('inflections: ', inflections)
