#
# Simpleton -- simp.py
#   Simple-Ton: A ton of simple things to do.
#
#   This version will concentrate on grammar
#

import os

import simpStuff as ss
import simpSA as sa
import simpConfig as sc


from datetime import datetime

fConvo = 'convoHist.txt'
convo = []


def getInput():

    s = input("Enter a command <[C]hat, [S]peak, or [T]each>: ")

    if s == 'c' or s == 'C':
        if sc.verbose: print(s)
        print("Entering Chat mode...")
#    elif s == 's' or s == 'S':
#        if sc.verbose: print(s)
#        print("Entering random Speak mode, but not today...")
#    elif s == 't' or s == 'T':
#        if sc.verbose: print(s)
#        print("Entering Teach mode, but not today...")
#    else:
#        print("I do not understand: >>" + str(s) + "<<")

    return s

def showData(data):
    print('- showData -')
    for d in data: print(d)
    print('- End showData -')

def lowerCase(s, data): 
# Currently only lowers NNPs case
# The PRP 'I' is unchanged...

    slist = s.split(' ')
    ccs = []

    for w in slist:           
        for d in data:                       
            if d[0].lower() == w:
                if d[-1] == 'NNP':
                    w = w.capitalize()                            
        ccs.append(w)
    return ccs


def chkWords(s, inData):
# Returns sentence words not in lex
    words = []

    for d in inData:
        words.append(d[0])
                
    s1 = set(s)
    s2 = set(words)
    ret = s1.difference(s2)
    
    return ret


# May not be needed...~?
def getPOS(s, data):

    sPOS = []
    
    for w in s:
        for d in data:
            if w == d[0]:
                sPOS.append((w,d[1]))
    return(sPOS)


def simpChat(cmd):

    # Read all data (Nx, Vx, etc.)
    inData = ss.getData()
    inDataLen = len(inData)
    if sc.verbose:
        print("getData() returned {} lines of data.".format(inDataLen))
        showData(inData)

    # Build CFG file from data and cfg_rules
    ss.buildCFG(inData)

    # Develop rudimentary concept of self (I am Simp)
    simpName = 'Simp'
    for i in inData:
        if i[0] == simpName:
            #sc.simpData = i # What's with the sc. ?
            simpData = i
            break

    print("Hello I am: " + simpName)
    if sc.verbose: print("simpData  : {}: ".format(simpData))
    
    while cmd in ['c', 'C']:
        sPOS = ''
        s = input("Enter a short sentence: ")
        
        if len(s) > 0: # Now the fun begins
            if len(convo) > 0:
                print('---- Current conversation:') 
                for c in convo:
                    print(c)
                print('----')
                    
            lowerS = lowerCase(s, inData) 

            # Are all the words in the sentence in our Lex?
            ret = chkWords(lowerS, inData)

            if len(ret) > 0:
                # ss.addWord is under construction...
                print('chkWords returned: ' + str(ret))
                ans = input('Learn and add? <y/n>:')

                if ans in ['Y','y']:
                    if ss.addWord(ret):
                        inData = ss.getData() # Refresh input data with new word added
                        if sc.verbose: print('inData refreshed with: ', ret)
                    else:
                        print('!!{} was not added!!'.format(ret))
                else:
                    continue

            # Has this been said before?   Need to revamp...             
            hist = ss.chkHistory(lowerS)

            if len(hist) > 0:
                if sc.verbose: print('Something old...')    
                saidBefore = True
            else:
                if sc.verbose: print('Something new...')                    
                saidBefore = False
            
            # Parse corrected case sentence (input) per grammar
            # Draw out the grammar tree?
            draw = False
            grammarTree = ss.chkGrammar(lowerS, draw)

            if grammarTree == None:
                validCFG = False
                if sc.verbose: print('grammarTree == none')

                #sPOS = ss.getPOS(ccs, inData)
                #if sc.verbose: print('ccs tagged, sPOS: ', sPOS)

                #sA = sa.Sentence('', '', '', '', '', '', '', '', '', '', '')

                print('Do we really want to process invalid grammar?')
                print('--- A valid CFG was not returned. ---')
                print('--- Knowledge methods not ran.')

            else:
                validCFG = True

                tStr = grammarTree.pformat_latex_qtree()
                print("\n------------")
                print('tStr:')
                print(tStr)
                print("\n------------")
                
                sA = sa.sentAnalysis(tStr, lowerS)
                print("\n------------")
                print("sA.inSent: ")
                print(sA.inSent)
                print("\n------------")

                # Save sentence to list and conversation history file
                # 
                if sc.verbose: print('Retaining convo history...')

                if sA.inSent != '':
                    convo.append(sA.inSent)
                
                    f = open(fConvo, 'a')
                    f.write('\n' + str(sA.inSent))
                    f.close()

        else:
            if sc.verbose: print('Exiting chat...')
            cmd = ''

    # Archiving convo history
    now = datetime.now()
    timeStamp = now.strftime("%m%d%y-%H%M%S")

    if os.path.isfile('convoHist.txt'):
        os.rename('convoHist.txt', 'convoHist.txt' + '.' + timeStamp)
        
    return




if __name__ == "__main__":

    print("Simple-Ton, A ton of simple things to do.")

    loop = True

    # Main loop
    #
    while loop:
   
        # Get user command input
        #
        cmd = getInput()

        if cmd == 'c' or cmd == 'C': # Chat only; Others have been removed
            simpChat(cmd)
        else:
            loop = False
        
    print('End Simple-Ton.')
    # end simp.py
