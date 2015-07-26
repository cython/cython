#Test file to check if call backs work
import mt_cheeses
import time

x = 0
def steal_all_cheeses():
    global x
    print("Python Found! Stealing Cheese from Python: %d" % (x))
    x += 1
    return 1

def steal_cheddar():
    print "Python - no cheddar!"
    return 0  #Boohoo! no cheddar

def steal_provolone():
    print "Python Found! Stealing provolone!"
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
   

