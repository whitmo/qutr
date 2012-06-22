from . import tee
from .io import JobIO
from contextlib import contextmanager


@contextmanager
def teed_ioout(func, job, **kw):
    """
    Tees output between stdout and stderr and redis. Serves as a
    **job_wrapper** subscriber for retools.queue.

    caveat: imagine it only will work with true forking queues
    """
    uid = func.uid = job.job_id

    print "Teeing output for %s" %uid
    out = tee.sysout(JobIO(uid))
    err = tee.syserr(JobIO(uid))
    try:
        yield
    except :
        import pdb;pdb.set_trace()
    finally:
        print "UnTeeing output for %s" %func.uid
        del out
        del err
