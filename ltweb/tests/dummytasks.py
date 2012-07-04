from qutr.qutils import iotask


@iotask(name="2. Numbers Out")
def numbers():
    """
    Print out alot of numbers 
    """
    import sys
    for x, y in enumerate(range(100)):
        print "Out: %d %d" %(x, x*y)
        print >> sys.stderr, "Err: %s" %(x*y)
    raise ValueError('WHAHAHAHAH')


from itertools import count
from qutr.qutils import iotask, viztask
import json
import random
import requests
import time

@iotask(name="1. Numbers Out (short)")
def short_numbers():
    """
    Print out a few numbers 
    """
    import sys
    for x, y in enumerate(range(10)):
        print "Out: %d %d" %(x, x*y)
        print >> sys.stderr, "Err: %s" %(x*y)
    raise ValueError('WHAHAHAHAH')

def stream_o_twits(howmany):
    counter = count()
    r = requests.post('https://stream.twitter.com/1/statuses/sample.json',
                      data={'stall_warnings': False},
                      auth=('whitmo', 'pw'))
    for l in r.iter_lines():
        c = next(counter)
        data = {}
        if l:
            data = json.loads(l)
        yield c, data
        if c >= howmany:
            break


@iotask(name="Twits")
def twits():
    """
    A sample of the fire hose
    """
    print "STREAM THE TWITS"
    for count, twit in stream_o_twits(500):
        if 'text' in twit:
            print "%s -- %s" %(count, twit['text'])
    print "ENOUGH TWEETS"
    

@viztask(name="Scroller", type="viz")
def viz_test():
    """
    Scroll some random numbers
    """
    viz_test.publish("Load the viz");
    viz_test.publish(dict(type='viz',
                          event='load',
                          url="/static/scroll.js"))

    for x in range(100):
        viz_test.publish(dict(count=x*random.random()))
        time.sleep(0.5)
        
    viz_test.publish(dict(event='stop'))
    viz_test.publish("the viz ends");



@viztask(name="Twitter tweet length scroller", type="viz")
def twit_lengths():
    """
    Visualize tweets
    """
    twit_lengths.publish(dict(type='viz',
                              state='load',
                              url="/static/scroll.js"))
    
    for count, twit in stream_o_twits(500):
        if 'text' in twit:
            twit_lengths.publish(dict(count=len(twit['text']),
                                          state='update'))
    else:            
        twit_lengths.publish(dict(state='stop'))



