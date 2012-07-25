from . import io
from pyramid.view import view_config
from retools import global_connection as cxn
import json
import logging

logger = logging.getLogger(__name__)

@view_config(route_name='home', renderer='index.html')
def hp(request):
    return dict()


@view_config(route_name='job_stream', renderer='jobview.html')
def index(request):
    """ Base view to load our template """
    return request.matchdict


@view_config(route_name='job', renderer='json', xhr=True)
def job(request, key=io.JobNamespace.job_key, xhr=True):
    """
    Grabs entire backlog from redis.
    """
    uid = request.matchdict['job_id']
    jobkey = key.format(**request.matchdict)
    logger.info(jobkey)
    lines = cxn.redis.lrange(jobkey, 0, -1) or []
    return dict(uid=uid, lines=lines)


@view_config(route_name='tasks', renderer='json', xhr=True)
def tasks_api(request):
    return request.tasks


@view_config(route_name='jobs', renderer='json', xhr=True)
def jobs(request):
    if request.method == 'POST':
        path = request.POST['path']
        uid = request.enqueue(path)
        skey = io.jns.sub_key.format(uid)
        cxn.redis.publish(skey, json.dumps(dict(state="queued")))
        url = "{0}/{1}".format(request.application_url, uid)
        request.response.headers.add('Location', url)
        return dict(uid=uid)
    raise NotImplemented(request.method)


