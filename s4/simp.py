#
# Simpleton
#    Simple-Ton: A ton of simple things to do.
#
#

import sys
import simpStuff as ss

from datetime import datetime

flog = 'simpLog.txt'
fhistory = 'history.txt'


f = open(flog, 'a')
startTime = datetime.now()

print("Simple-Ton, A ton of simple things to do.")

st = startTime.strftime("%m/%d/%Y %H:%M:%S")

f.write('\n*** START RUN AT: ' + str(st) + ' ***\n')
f.write('   Reading input data\n')

# Read lexicon & KB data file
inData = ss.getData()

# Develop rudimentary concept of self (I am Simp)
simpName = 'Simp'
for i in inData:
    if i[0] == simpName:
        simpData = i
        break

print("Hello I am: " + simpName)
print(simpData)

# Build CFG file from data and cfg_rules
ss.buildCFG(inData)

endTime = datetime.now()
et = endTime.strftime("%m/%d/%Y %H:%M:%S")

elpTime = endTime - startTime

f.write("----------------------\n")
f.write("--- reading of data completed:\n")
f.write("    end time: " + str(et) + "\n")
f.write("    elapsed time: " + str(elpTime) + "\n")
#f.close()



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
                    # We'll do something with missing words later...
                    print('chkWords returned: ' + str(ret))
                    print('You will need to teach me the above')
                
                    continue

                # Has this been said before?
                aforementioned = ss.chkHistory(ccs)

                f.write('    aforementioned: ' + str(aforementioned) + '\n')

                if len(aforementioned) > 0:
                    print('Something old...')
                    print('Said: ' + str(len(aforementioned)) + ' times before')
                
                    #print(type(aforementioned))
#                   for a in aforementioned:
#                       print('a: ' + str(a))
#                       a2 = a.split(';')
#                       for a2a in a2:
#                           # a2a = a2a.replace(" ", "")
#                           print('a2a: ' + str(a2a))
                    
                    saidBefore = True
                else:
                    print('Something new...')
                    saidBefore = False

                f.write('    aforementioned mentioned: ' + str(len(aforementioned)) + ' times before\n')
            
                # Parse corrected case sentence (input) per grammar
                # Draw out the grammar tree?
                draw = False
                tree = ss.chkGrammar(ccs, draw)

                if tree == None:
                    validCFG = False

                    f.write('    CFG parse returned NONE: ' + str(tree) + '\n')
                
                else:
                    validCFG = True
        
                    f.write('    CFG tree: ' + str(tree) + '\n')

                    tList = ss.tree2List(tree)

                    f.write('    tList: ' + str(tree) + '\n')
                
                    sAnaly = ss.sentAnalysis(tList, f)

                    f.write('    sAnaly: ' + str(sAnaly) + '\n')

                sPOS = ss.getPOS(ccs, inData) # Is this needed any more?

                f.write('    sPOS: ' + str(sPOS) + '\n')
            
                rel = ss.s4r(ccs, inData, simpData) # Search for relationships

                f.write('    rel: ' + str(rel) + '\n')

                if len(rel) == 0:
                    relationFound = False
                    print('rel = False: ' + str(rel))
                else:
                    relationFound = True
                    print('rel = True: ' + str(rel))

                # Thus far we can have 8 situations:
                #   1) New sentence +CFG +rel
                #   2) New sentence +CFG -rel
                #   3) New sentence -CFG +rel
                #   4) New sentence -CFG -rel
                #   5) Old sentence +CFG +rel
                #   6) Old sentence +CFG -rel
                #   7) Old sentence -CFG +rel
                #   8) Old sentence -CFG -rel


            
                # For now just add the new sentence to the history file
                # 
                print('Saving history...')
                t = slt.replace(' ', '; ')
                fh = open(fhistory, 'a')
                fh.write('\n' + str(sPOS) + '; ' + str(rel) + '; ' + t)
                fh.close()
            
            
            else:
                cmd = 'EXIT'
                print('    cmd: ' + str(cmd)) 
                f.write(' -->> cmd: ' + str(cmd) + '\n')

    elif cmd == 's' or cmd == 'S': # Speak
        # Randomly generates a sentence from the exiting CFG
        # 
        rules = ss.getRules()
        relationFound = False
        
        while not relationFound:
            s = ss.randomSpeak(rules)
            # This check also returns a list which is needed
            ccs = ss.correctCase(s, inData)
            sPOS = ss.getPOS(ccs, inData)
            relationFound = ss.s4r(ccs, inData, sPOS)
            print('relationFound: ' + str(relationFound))
        s = ''
            
    elif cmd == 't' or cmd == 'T': # Tech mode; Not yet
        # Train
        #
        print("TODO: Enter learningMode")
        s = ''
    #    sm.learningMode(retCode)
    else:
        print("    cmd = " + str(cmd) + " Exiting...")
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
