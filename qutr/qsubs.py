from . import tee
from .io import JobIO
from contextlib import contextmanager
from functools import partial
from qutr.io import jns
import json


@contextmanager
def teed_ioout(func, job, **kw):
    """
    Tees output between stdout and stderr and redis. Serves as a
    **job_wrapper** subscriber for retools.queue.

    caveat: imagine it only will work with true forking queues
    """
    with prep_job(func, job, **kw):
        uid = func.uid

        jobio = JobIO(uid, func.publish)
        tee.sysout(jobio).set()
        tee.syserr(jobio).set()

        try:
            yield
        finally:
            func.publish(dict(event='done'))
            import sys
            del sys.stdout
            del sys.stderr
 
@contextmanager
def prep_job(func, job, **kw):
    uid = func.uid = job.job_id
    func.publish = partial(publish, job.worker.redis, uid)
    try:
        yield
    finally:
        print "<<job:%s done>>" %job.job_id


@contextmanager
def visout(func, job, **kw):
    try:
        yield
    finally:
        print "VIZ Done"


def publish(redis, uid, data):
    if not isinstance(data, basestring):
        data = json.dumps(data)
    lkey = jns.job_key.format(job_id=uid)
    skey = jns.sub_key.format(uid)    
    redis.lpush(lkey, data)
    redis.publish(skey, data)
    return data, redis


