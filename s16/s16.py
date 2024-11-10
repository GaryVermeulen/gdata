#
# s16.py
#
# New: 11/10/24
#

import pandas as pd

from loadRawKB import loadRawKB
from loadRawCorpus import loadAndProcess
from processSVOs import processCorpus

debug = False


def findMainCharacter(pCorpus):

    corpusMC = []
    i_lst = []
    nnp_lst = []
    nn_lst = []
    nns_lst = []
    cnt = 0
    i_cnt = 0
    indices_cnt = 0

    for c in pCorpus:
        for s in c[1]:
            # I an Abe
            cnt += 1
            print('---- {} ----'.format(cnt))
            print(s.inputSent)
            #print(s.taggedSentShort)
            
            try: # try was needed of the .index -- doesn't seem needed for the indices method
                #index = s.inputSent.index('I') # Finds only the 1st
                #print('index: ', index, cnt, s.inputSent)
                indices = [index for index, value in enumerate(s.inputSent) if value == "I"]

                print("len indices: ", len(indices))

                if len(indices) > 0:
                    indices_cnt += 1
                    #print("Found 'I' at: ", cnt, indices)
                    for i in indices:
                        i_cnt += 1
                        print("   ", s.taggedSentShort[i])
                        print("   ", s.taggedSentShort[i + 1])
                        print("   ", s.taggedSentShort[i + 2])
                        print('...')
                        if s.taggedSentShort[i + 1]["word"] == "am":
                            print("   -", s.taggedSentShort[i + 1])
                            if s.taggedSentShort[i + 2]["tag"] == "NNP":
                                print("   --", s.taggedSentShort[i + 2])
                                corpusMC.append((s.taggedSentShort[i + 2], s))
                        print('---')
                    i_lst.append(s.taggedSentShort)
                else:
                    print('indices <= 0: ')

            except:
                print('index not found except: ', s.inputSent)
            
            #print("------ list NNPs")
            for i in s.taggedSentShort:
                if i["tag"] == "NNP":
                    #print(i)
                    nnp_lst.append(i)

            #print("------ list NNs")
            for i in s.taggedSentShort:
                if i["tag"] == "NN":
                    #print(i)
                    nn_lst.append(i)

            #print("------ list NNSs")
            for i in s.taggedSentShort:
                if i["tag"] == "NNS":
                    #print(i)
                    nns_lst.append(i)

        print("\nI count: ", i_cnt)
        print("indices cnt: ", indices_cnt)
        print('\ni_lst:')
        print(len(i_lst))
        print(type(i_lst))
        print('i_lst ------------------------')
        for i in i_lst:
            print("---")
            print(i)


        
        print('\ncorpusMC:')
        print(len(corpusMC))
        print(type(corpusMC))
        print('corpusMC ------------------------')
        for c in corpusMC:
            print(c)
            #print(c[0])
            #c[1].printAll()

        #df = pd.DataFrame(ds)

        print('\nnnp_lst:')
        print(len(nnp_lst))
        print(type(nnp_lst))
        print('nnp_lst ------------------------')
        for c in nnp_lst:
            print(c)

        df = pd.DataFrame(nnp_lst)

        print(df)
        print("---")
        #x = pd.concat(g for _, g in df.groupby("ID") if len(g) > 1) # Throws error

        ids = df["word"]
        x = df[ids.isin(ids[ids.duplicated()])].sort_values("word")

        print(x)

        print('\nnn_lst:')
        print(len(nn_lst))
        print(type(nn_lst))
        print('nn_lst ------------------------')
        for c in nn_lst:
            print(c)

        df = pd.DataFrame(nn_lst)

        print(df)
        print("---")
        #x = pd.concat(g for _, g in df.groupby("ID") if len(g) > 1) # Throws error

        ids = df["word"]
        x = df[ids.isin(ids[ids.duplicated()])].sort_values("word")

        print(x)

        print('\nnns_lst:')
        print(len(nns_lst))
        print(type(nns_lst))
        print('nns_lst ------------------------')
        for c in nns_lst:
            print(c)

        df = pd.DataFrame(nns_lst)

        print(df)
        print("---")
        #x = pd.concat(g for _, g in df.groupby("ID") if len(g) > 1) # Throws error

        ids = df["word"]
        x = df[ids.isin(ids[ids.duplicated()])].sort_values("word")

        print(x)


    return corpusMC

if __name__ == "__main__":


    print("START s16.py (main)...")

    startKB = loadRawKB()
    
    if debug:
        print('startKB:')
        print(len(startKB))
        print(type(startKB))
        print('startKB ------------------------')
        for k in startKB:
            print(k)

    corpus = loadAndProcess()
    
    if debug:
        print('corpus:')
        print(len(corpus))
        print(type(corpus))
        print('corpus ------------------------')
        for c in corpus:
            print(c[0])
            for s in c[1]:
                s.printAll()
        
    pCorpus = processCorpus(corpus)
    #debug = True
    if debug:
        print('pCorpus:')
        print(len(pCorpus))
        print(type(pCorpus))
        print('pCorpus ------------------------')
        for c in pCorpus:
            print(c[0])
            for s in c[1]:
                s.printAll()

    corpusMC = findMainCharacter(pCorpus)
    debug = True
    if debug:
        print('corpusMC:')
        print(len(corpusMC))
        print(type(corpusMC))
        print('corpusMC ------------------------')
        print(corpusMC)
        #for c in corpusMC:
        #    print(c)
            #print(c[0])
            #c[1].printAll()


            

    print("END s16.py (main)...")
