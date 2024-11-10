#
# pickleChecker.py
#

import pickle
import os


if __name__ == "__main__":


    # Get the current working directory
    cwd = os.getcwd()

    # List all files and directories in the current working directory
    items = os.listdir(cwd)

    if len(items) > 0:
        for i in items:
            if i[-1] == "p":
                print(i)

        pFile = input('Enter pickle file to read: ')

        p = pickle.load(open(pFile, 'rb'))

        print('len p: ', len(p))
        print('type p: ', type(p))

        if type(p) is dict:
            for k, v in p.items():
                print("Key: {}; Value: {}".format(k, v))
        elif type(p) is list:
            for item in p:
                print(item)
        else:
            print(p)
    else:
        print("Current directory is empty (No pickles found).")

    
