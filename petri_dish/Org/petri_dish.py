# petri_dish.py
# A wacko idea of making small programs evolve into larger
# more complex programs--computer program evolution
#

from cell1 import cell1
from cell2 import cell2

import os
import subprocess

#
if __name__ == "__main__":

    print('Starting petri_dish.py')

    start = 1
    stop = 6

    print("Using import...")

    for i in range(start, stop):
        print(cell1(i), cell2(i+1))

    print('----------')
    # Shows output only from bash shell NOT python shell
    print("Using os.system...")

    result = os.system("python3 cell1.py")

    print("result: ", result)

    result = os.system("throwing shit")

    print('----------')

    try:
        ans = subprocess.check_output(["python3", "cell0.py"], text=True)
        print(ans)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")

    


    print('End petri_dish.py')
