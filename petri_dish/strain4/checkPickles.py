#
# checkPickles.py
#

import pickle



if __name__ == "__main__":

    """  
    # logs.p
    #
    logs = pickle.load(open('logs.p', 'rb'))

    print('len logs: ', len(logs))
    print('type logs: ', type(logs))

    for log in logs:
        print('---')
        print(log[0])
        for line in log[1]:
            print(line)
    """
    
    # solutionBase.p
    #
    sb = pickle.load(open('solutionBase.p', 'rb'))

    print('len sb: ', len(sb))
    print('type sb: ', type(sb))

    for s in sb:
        print('---')
        print(s)
        


    
   
