#
# counter1.py
#

from cell1DNA import isNumPrime1


if __name__ == "__main__":
    
    cnt = 0
    maxLoop = 120

    while cnt < maxLoop:

        print('---')
        print('cnt: ', cnt)

        isPrime = isNumPrime1(cnt)

        cnt += 1
