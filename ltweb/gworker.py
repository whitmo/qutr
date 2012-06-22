from gevent import monkey
monkey.patch_all(os=False)

from retools.queue import Worker


class GreenWorker(Worker):
    """
    A Green worker 
    """

run_worker = Worker.run

