#
# Simpleton
#   Simple-Ton: A ton of simple things to do.
#   
#   Except to develop AGI (Artifical General Intelligence).
#

import sys
import simpStuff as ss
import simpSA as sa
#import simpReply as sr
import simpConfig as sc
import simpGuess as sg
import simpReason as sr

from datetime import datetime

flog = 'simpLog.txt'
fhistory = 'history.txt'
frslog = 'raw_sentence_log.txt'


f = open(flog, 'a')
startTime = datetime.now()

print("Simple-Ton, A ton of simple things to do.")

st = startTime.strftime("%m/%d/%Y %H:%M:%S")

f.write('\n*** START RUN AT: ' + str(st) + ' ***\n')
f.write('   Reading input data and building CFG file\n')

# Read lexicon & KB data file
inData = ss.getData()
inDataLen = len(inData)
f.write('   Read {} items\n'.format(inDataLen))

# Build CFG file from data and cfg_rules
f.write('   Building CFG file\n')
ss.buildCFG(inData)

endTime = datetime.now()
et = endTime.strftime("%m/%d/%Y %H:%M:%S")

elpTime = endTime - startTime

f.write("----------------------\n")
f.write("--- reading of data and building of CFG file completed:\n")
f.write("    end time: " + str(et) + "\n")
f.write("    elapsed time: " + str(elpTime) + "\n")
#f.close()

# Develop rudimentary concept of self (I am Simp)
simpName = 'Simp'
for i in inData:
    if i[0] == simpName:
        sc.simpData = i
        break

print("Hello I am: " + simpName)
if sc.verbose: print("simpData  : {}: ".format(sc.simpData))

loop = True

# Main loop
#
while loop:
   
    # Get user command input
    #
    cmd = ss.getInput()

    f.write('    cmd: ' + str(cmd) + '\n')

    sLoopTime = datetime.now()
    slt = sLoopTime.strftime("%m/%d/%Y %H:%M:%S")

    f.write('\n---    START LOOP AT: ' + str(slt) + ' ===\n')

    if cmd == 'c' or cmd == 'C': # Chat
        while cmd in ['c', 'C']:
            sPOS = ''
            s = input("Enter a short sentence: ")

            f.write('-------------\n')
            f.write('    s: ' + str(s) + '\n')
        
            if len(s) > 0: # Now the fun begins
                ccs = ss.correctCase(s, inData)
                f.write('    ccs: ' + str(ccs) + '\n')

                # Are all the words in the sentence in our Lex?
                ret = ss.chkWords(ccs, inData)
                f.write('    ret: ' + str(ret) + ' Is Unknown\n')

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
                print('ccs: ', ccs)
                print('ccs type: ', type(ccs))
                
                hist = ss.chkHistory(ccs)
                f.write('    aforementioned: ' + str(hist) + '\n')

                if len(hist) > 0:
                    if sc.verbose:
                        print('Something old...')
                        #for h in hist:
                        #    print(h)
                        #print('Said: ' + str(len(hist)) + ' times before')
                    
                    saidBefore = True
                else:
                    if sc.verbose: print('Something new...')
                    
                    saidBefore = False

                f.write('    hist mentioned: ' + str(len(hist)) + ' times before\n')
            
                # Parse corrected case sentence (input) per grammar
                # Draw out the grammar tree?
                draw = False
                tree = ss.chkGrammar(ccs, draw)

                if tree == None:
                    validCFG = False
                    if sc.verbose: print('tree == none')
                    f.write('    CFG parse returned NONE: ' + str(tree) + '\n')

                    sPOS = ss.getPOS(ccs, inData)
                    if sc.verbose: print('ccs tagged, sPOS: ', sPOS)
                    f.write('    sPOS: ' + str(sPOS) + '\n')

                    sA = sa.Sentence('', '', '', '', '', '', '', '', '', '') 

                else:
                    validCFG = True

                    fl = open(frslog, 'a')
                    fl.write(str(s) + '\n')
                    fl.write(str(tree) + '\n')
                    fl.close()
        
                    f.write('    CFG tree: ' + str(tree) + '\n')

#                    tList = ss.tree2List(tree)
                    tStr = tree.pformat_latex_qtree()

                    f.write('    tList: ' + str(tree) + '\n')
                
#                    sAnaly = sa.sentAnalysis(tList, f)
                    sA = sa.sentAnalysis(tStr, ccs, f)

#                    f.write('    sAnaly: ' + str(sAnaly) + '\n')
#                    print('sAnaly: ' + str(sAnaly))
                    
#
#                f.close()
#                sys.exit() # Under dev, so exit for now

                if validCFG:
                    rel = sr.s4r(ccs, sA, sPOS, sc.simpData, inData) # Search for relationships
                else:
                    rel = sr.s4r(ccs, sA, sPOS, sc.simpData, inData)


                    
                f.write('    rel: ' + str(rel) + '\n')

                if len(rel) == 0:
                    relationFound = False
                    if sc.verbose: print('rel = False: ' + str(rel))
                else:
                    relationFound = True
                    if sc.verbose: print('rel = True: ' + str(rel))

                    
                sg.guess(s) # Make a SWAG with raw input

                print('----- No reply for now...')
#                s????.reply(sA, rel, sc.simpData) # Attempt some kind of coherent output (rule based)

          
                # Save sentence to conversation history file
                # 
                if sc.verbose: print('Saving history...')
                t = slt.replace(' ', '; ')
                fh = open(fhistory, 'a')
                fh.write('\n' + str(ccs) + '; ' + str(rel) + '; ' + t)
                fh.close()
            
            else:
                cmd = 'EXIT'
                if sc.verbose: print('    cmd: ' + str(cmd)) 
                f.write(' -->> cmd: ' + str(cmd) + '\n')

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

    now = datetime.now()
    elt = now.strftime("%m/%d/%Y %H:%M:%S")
    elooptime = now - sLoopTime
    
    f.write('\n---    END LOOP AT: ' + str(elt) + ' ===\n')
    f.write('---    elapsed loop time: ' + str(elooptime) + ' ===\n')
        

now = datetime.now()
dt = now.strftime("%m/%d/%Y %H:%M:%S")
run_et = now - startTime

f.write('\n*** END RUN AT: ' + str(dt) + ' ***\n')
f.write('*** elapsed run time: ' + str(run_et) + '\n')
f.close()

print('End Simple-Ton.')

# end simp.py
