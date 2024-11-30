# randomNumber.py
#

import random

# Generate a random float between 0 and 1
random_float = random.random()
print("From float: ", random_float)

# Generate a random integer between 1 and 10 (inclusive)
random_int = random.randint(1, 10)
print("From int: ", random_int)

# Generate a random float between 5 and 10 (inclusive)
random_float_in_range = random.uniform(5, 10)
print("From float in range: ", random_float_in_range)

# Choose a random element from a list
my_list = [1, 2, 3, 4, 5]
random_element = random.choice(my_list)
print("From list: ", random_element)

random_int = random.randint(1, 240)
print("From int (1-240): ", random_int)

for i in range(1, 100):

    random_int = random.randint(0, 1)
    print("From int (0-1): ", random_int)
