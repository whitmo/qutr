from retools import queue
import inspect


class Task(dict):
    """
    Annotates a callable
    """
    attr = '_task_metadata'
    def __init__(self, **kwargs):
        self.update(kwargs)

    def __call__(self, func):
        self['desc'] = self.get('desc') or inspect.getdoc(func)
        self['name'] = self.get('name') or func.__name__
        setattr(func, self.attr, self)
        return func
    
    @classmethod
    def is_task(cls, func):
        if callable(func):
            meta = getattr(func, cls.attr, None)
            if meta:
                return meta
        return None


def task(*args, **kwargs):
    if len(args) == 1:
        return Task()(args[0])
    return Task(*args, **kwargs)


default_subscribers = dict(job_wrapper='ltweb.qsubs:teed_ioout')

def setup_queue_manager(config, subscribers=default_subscribers):
    config.registry.qm = queue.QueueManager(subscribers=subscribers)

def launch_worker(settings):
    q, interval, block = (settings['ltweb.q'], 
                          settings['ltweb.q_interval'], 
                          settings['ltweb.q_block'])
    worker = queue.Worker(queues=[q])
    block = False or block.lower() != 'false' 
    worker.work(interval=float(interval), blocking=bool(block))
    print "started worker: %s" %worker.worker_id






        

        


