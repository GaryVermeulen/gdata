# Thread fun
#
import logging
##import threading
from threading import Thread
import time

def tcounter(tcount, name, thing):
    global count

    logging.info("Thread tcounter %s: starting", name)
    while count:
        tcount += 1
    thing.append(tcount)
    logging.info("Thread tcounter tcount %s: finishing", tcount)    
    logging.info("Thread tcounter %s: finishing", name)   
    

def thread_function1(name, pass_around):
    logging.info("Thread function1 %s: starting", name)
#    print("pass_around1: " + str(pass_around))
    logging.info("pass_around1 in t%s = %s", tx, pass_around)
    x = name + 1
    # print("x: " + str(x) + " name1 " + str(name) + " + 1")
    logging.info("Thread function1; sleep time x = %s...", x)
    time.sleep(x)
    logging.info("Thread1 sleep over...")
    pass_around.append('thread_function1')
    # print("pass_arround1: " + str(pass_around))
    logging.info("Thread function1; pass_around: %s...", pass_around)
    logging.info("Thread function1 %s: finishing", name)
    
    
def thread_function2(name, pass_around):
    logging.info("Thread function2 %s: starting", name)
    # print("pass_around2: " + str(pass_around))
    logging.info("pass_around2 in t%s = %s", tx, pass_around)
    x = name + 1
    # print("x: " + str(x) + " name2 " + str(name) + " + 1")
    logging.info("Thread function2; sleep time x = %s...", x)
    time.sleep(x)
    # print("fundtion2 sleep over, stop counting...")
    logging.info("Thread2 sleep over...")
    global count
    count = False
    pass_around.append('thread_function2')
    # print("count: " + str(count))   
    logging.info("Thread function2; count %s...", count)
    # print("pass_arround2: " + str(pass_around)) 
    logging.info("Thread function2; pass_around: %s...", pass_around)
    logging.info("Thread function2 %s: finishing.", name)    
    


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
 
# print("Starting main with t0...")


count = True
tx = 0
tcount = 0
thing = [0]
pass_around = ['start']

logging.info("Starting main t%s...", tx)
t0 = Thread(target=tcounter, args=[tcount, tx, thing])
t0.start()
 
 
# print("Starting main with t1...") 
tx = 1
logging.info("Starting main t%s...", tx)
t1 = Thread(target=thread_function1, args=[tx, pass_around])
t1.start()
 
# print("Starting t2 in main...")
tx = 2
logging.info("Starting main t%s...", tx) 
t2 = Thread(target=thread_function2, args=[tx, pass_around])
t2.start()


# print("tcount: " + str(tcount))  
# print("FINI...")

logging.info("Main before sleep: tcount: %s; thing: %s...", tcount, thing) 
logging.info("Main sleeping for 5s...") 
time.sleep(5)
logging.info("Main completed: tcount: %s; thing: %s...", tcount, thing) 
logging.info("Main FINI")



