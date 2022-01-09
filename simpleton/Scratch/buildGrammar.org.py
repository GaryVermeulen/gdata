#
# buildGrammar.py
#

# New CFG file
#
fCFG = 'simp.cfg'
fCFGmode = 'w'

#
# Source files
#
fS = 'S.txt'
fVP = 'VP.txt'
fPP = 'PP.txt'
fNP = 'NP.txt'
fN = 'N.txt'
fV = 'V.txt'
fP = 'P.txt'
fDet = 'Det.txt'
mode = 'r'

fall = []
fall.append(fS)
fall.append(fVP)
fall.append(fPP)
fall.append(fNP)
fall.append(fN)
fall.append(fV)
fall.append(fP)
fall.append(fDet)

rules = []

def buildCFG():
#    print(len(fall))
#    print(fall)

    for f in fall:   
        fx = open(f, mode)

        f_in = fx.read()
        rules.append(f_in)

        fx.close()

#        print('======')
#        print(f_in, end='')
#        print('------')

    print('_+_+_+_+_+_+_')
    for r in rules:
        print(r, end='')

    print('+_+_+_+_+_+_+')

    fout = open(fCFG, fCFGmode)
    for r in rules:
        fout.write(r)
    fout.close()
    
    print('End buildCFG')
    return
