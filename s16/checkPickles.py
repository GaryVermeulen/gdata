#
# pickleChecker.py
#

import pickle


if __name__ == "__main__":

    # starterKB.p
    #
    starterKB = pickle.load(open('pickleJar/starterKB.p', 'rb'))

    print('len starterKB: ', len(starterKB))
    print('type starterKB: ', type(starterKB))

    for k in starterKB:
        print(k)
