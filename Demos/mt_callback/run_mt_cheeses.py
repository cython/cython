#Test file to check if call backs work
import mt_cheeses
import time
import threading

def steal_all_cheeses():
    global x
    print("%s. Python Found! Stealing Cheese from Python" % (threading.currentThread().getName()))
    return 1

def steal_cheddar():
    print ("%s Python - no cheddar!" %(threading.currentThread().getName()) )
    return 0  #Boohoo! no cheddar

def steal_provolone():
    print ("%s Python Found! Stealing provolone!" %(threading.currentThread().getName()))
    return 1 #Yahoo! provolone found


#register handler
mt_cheeses.reg( "all_cheeses", steal_all_cheeses )
mt_cheeses.reg( "cheddar", steal_cheddar )
mt_cheeses.reg( "provolone", steal_provolone )

#call callbacks
mt_cheeses.cheeses_init()

#keep the program alive
while True:
   time.sleep(5); 
   

