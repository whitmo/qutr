from pyramid.view import view_config
from retools import global_connection as cxn
from . import io


@view_config(route_name='home', renderer='templates/mytemplate.html')
def hp(request):
    return {'project':'ltweb'}


@view_config(route_name='job_stream', renderer='jobview.html')
def index(request):
    """ Base view to load our template """
    return request.matchdict


@view_config(route_name='job_log', renderer='json')
def get_backlog(request, key=io.JobNamespace.job_key):
    """
    Grabs entire backlog from redis.
    """
    jobkey = key.format(**request.matchdict)
    return cxn.redis.lrange(jobkey, 0, -1)



