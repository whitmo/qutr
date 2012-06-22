from StringIO import StringIO
from retools import global_connection as cxn
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
import json


class JobNamespace(BaseNamespace):
    job_key = "ltweb:job_out:{job_id}"
    sub_key = 'jobs:{0}'

    def listener(self, job_id):
        r = cxn.redis.pubsub()
        r.subscribe(self.sub_key.format(job_id))
        for m in r.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                self.emit("jobOut", data)

    def on_subscribe(self, data):
        self.job_id = data['job_id']
        self.jobkey = self.job_key.format(job_id=self.job_id)
        self.spawn(self.listener, self.job_id)

    # def on_chat(self, job_id, msg):
    #     r = cxn.redis
    #     assert job_id
    #     r.lpush(self.jobkey, msg)

    #     # we got a new chat event from the client, send it out to
    #     # all the listeners
    #     r.publish('out', dumps(chat.serialize()))


class IndexNamespace(BaseNamespace):
    def on_subscribe(self, data):
        self.job_id = data['job_id']
        self.jobkey = self.job_key.format(job_id=self.job_id)
        self.spawn(self.listener, self.job_id)


def socketio_service(request):
    retval = socketio_manage(request.environ,
                             {'/jobs': JobNamespace,
                              '/index': IndexNamespace}, 
                             request=request)

    return retval


class JobIO(StringIO):
    """
    A stream-like object that write output to a redis pub channel and
    a list.
    """
    list_key = JobNamespace.job_key
    pub_key = JobNamespace.sub_key
    def __init__(self, uid, redis=None):
        if redis is None:
            redis = cxn.redis
        self.redis = redis
        self.lkey = self.list_key.format(job_id=uid)
        self.skey = self.pub_key.format(uid)

    def flush(self):
        pass
    
    def write(self, line):
        self.redis.lpush(self.lkey, line)
        self.redis.publish(self.pub_key, line)

    def close(self):
        pass


def includeme(config):
    from . import utils
    utils.simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)



