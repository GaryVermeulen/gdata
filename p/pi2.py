"""
Generating Pi via spigot algorithm...

"""
import time

def pi_digits(n):
    "Generate n digits of Pi."
    k, a, b, a1, b1 = 2, 4, 1, 12, 4
    while n > 0:
        p, q, k = k * k, 2 * k + 1, k + 1
        a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
        d, d1 = a / b, a1 / b1
        while d == d1 and n > 0:
            yield int(d)
            n -= 1
            a, a1 = 10 * (a % b), 10 * (a1 % b1)
            d, d1 = a / b, a1 / b1

# >>> list(pi_digits(20))
# [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4]

#seconds = time.time()

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

print(time_string)

n_digits = 100000


# print(list(pi_digits(n_digits)))

pi = pi_digits(n_digits)

# print(type(pi))

pl = list(pi)

# print(type(pl))

p1 = pl.pop(0)
# print(str(p1))

# print(pl)

pl2s = ''.join([str(elem) for elem in pl])
# print(pl2s)

print("pi to " + str(n_digits) + " digits")
print(str(p1) + '.' + pl2s)

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)

print(time_string)

