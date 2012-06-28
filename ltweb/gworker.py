#@@ blocks
#from gevent import monkey
#monkey.patch_all(os=False)
#monkey.patch_all()

from retools.queue import Worker


class GreenWorker(Worker):
    """
    A Green worker 
    """

run_worker = Worker.run

