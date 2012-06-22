from pyramid.view import view_config
from retools import global_connection as cxn
from . import io


@view_config(route_name='home', renderer='index.html')
def hp(request):
    return dict()


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


@view_config(route_name='tasks', renderer='json')
def tasks_api(request):
    return request.tasks


@view_config(route_name='one23', renderer='json')
def one23(request):
    return dict(path='path',
                url='url',
                uid='1234') 


@view_config(route_name='jobs', renderer='json')
def jobs(request):
    if request.method == 'POST':
        path = request.POST['path']
        uid = request.enqueue(path)
        request.response.headers.add('Location', "%s/%s" %(request.application_url, uid))
        return dict(path=path, uid=uid)
    raise NotImplemented(request.method)


