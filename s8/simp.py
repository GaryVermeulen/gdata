#
# Simpleton -- simp.py
#   Simple-Ton: A ton of simple things to do.
#   
#

#import sys
import simpStuff as ss
import simpSA as sa
#import simpReply as sr
import simpConfig as sc
#import simpGuess as sg
#import simpReason as sr
import simpTree


print("Simple-Ton, A ton of simple things to do.")

# Read all data (Nx, Vx, etc.)
inData = ss.getData()
inDataLen = len(inData)
if sc.verbose: print("getData() returned {} lines of data.".format(inDataLen))

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

loop = True

# Main loop
#
while loop:
   
    # Get user command input
    #
    cmd = ss.getInput()

    if cmd == 'c' or cmd == 'C': # Chat
        while cmd in ['c', 'C']:
            sPOS = ''
            s = input("Enter a short sentence: ")
        
            if len(s) > 0: # Now the fun begins
                ccs = ss.correctCase(s, inData)

                # Are all the words in the sentence in our Lex?
                ret = ss.chkWords(ccs, inData)

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

                # Has this been said before?                
                hist = ss.chkHistory(ccs)

                if len(hist) > 0:
                    if sc.verbose:
                        print('Something old...')
                    
                    saidBefore = True
                else:
                    if sc.verbose: print('Something new...')
                    
                    saidBefore = False
            
                # Parse corrected case sentence (input) per grammar
                # Draw out the grammar tree?
                draw = False
                grammarTree = ss.chkGrammar(ccs, draw)

                if grammarTree == None:
                    validCFG = False
                    if sc.verbose: print('grammarTree == none')

                    sPOS = ss.getPOS(ccs, inData)
                    if sc.verbose: print('ccs tagged, sPOS: ', sPOS)

                    sA = sa.Sentence('', '', '', '', '', '', '', '', '', '') 

                else:
                    validCFG = True

                    tStr = grammarTree.pformat_latex_qtree()
                
                    sA = sa.sentAnalysis(tStr, ccs)

                    print("sA.inSent: ")
                    print(sA.inSent)
                    print("\n------------")

                # Original funky method to search for relationships (knowledge)
                #
                #if validCFG:
                #    can, cannot = sr.s4r(ccs, sA, sPOS, simpData, inData) # Search for relationships
#
#                    if sc.verbose:
#                        print('can   : ' + str(can))
#                        print('cannot: ' + str(cannot))#
#
#                else:
#                    print('No valid CFG returned, so not calling s4r')
#                    print('    we will deal with this later...')
#                    #rel = sr.s4r(ccs, sA, sPOS, simpData, inData)
                
                # Testing various methods to derive knowledge
                #
                if validCFG:
                    print('--- A valid CFG tree was returned, so let us attempt to find some knowledge')

                    w = simpTree.peruseData(sA)

                    print('peruseData returned:')
                    print(w)
                    print('---')
                    
                else:
                    print('--- A valid CFG was not returned. ---')
                    print('--- Knowledge methods not ran.')

# Later...
                print("--- Skipping guessing...")
#                sg.guess(s) # Make a SWAG with raw input

                print('--- No reply for now...')
#                s????.reply(sA, rel, sc.simpData) # Attempt some kind of coherent output (rule based)

          
                # Save sentence to conversation history file
                # 
#                if sc.verbose: print('Saving history...')
#                t = slt.replace(' ', '; ')
#                fh = open(fhistory, 'a')
#                fh.write('\n' + str(ccs) + '; ' + str(rel) + '; ' + t)
#                fh.close()
            
            else:
                cmd = 'EXIT'
                if sc.verbose: print('    cmd: ' + str(cmd)) 

    elif cmd == 's' or cmd == 'S': # Speak
        # Randomly generates a sentence from the exiting CFG
        # 
        rules = ss.getRules()
        relationFound = False
        
        while not relationFound:
            # Most likely returns gibberish
            s = ss.randomSpeak(rules)
            
            # This check also returns a list which is needed
            ccs = ss.correctCase(s, inData)
            sPOS = ss.getPOS(ccs, inData)
            relationFound = ss.s4r(ccs, inData, sPOS)
            if sc.verbose: print('relationFound: ' + str(relationFound))
        s = ''
            
    elif cmd == 't' or cmd == 'T': # Tech mode; Not yet
        # Train
        #
        if sc.verbose: print("TODO: Enter learningMode")
        s = ''
    #    sm.learningMode(retCode)
    else:
        if sc.verbose: print("    cmd = " + str(cmd) + " Exiting...")
        s = ''
        loop = False

print('End Simple-Ton.')

# end simp.py
