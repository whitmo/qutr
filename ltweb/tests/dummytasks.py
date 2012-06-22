from ltweb.qutils import task
import gevent
import random


@task(name="Numbers Out")
def numbers_print_out():
    """
    Print out alot of numbers 
    """
    import sys
    for x, y in enumerate(100):
        print "Out: %d %d" %(x, x*y)
        gevent.sleep(random.random() * 5)
        print >> sys.stderr, "Err:%s" %y+1/x+1




