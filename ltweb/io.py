from retools import global_connection as cxn
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
import json
from . import utils


class JobNamespace(BaseNamespace):
    job_key = "ltweb:job_out:{job_id}"
    def listener(self, job_id):
        import pdb;pdb.set_trace()
        r = cxn.redis.pubsub()
        r.subscribe('jobs:' + job_id)
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


def socketio_service(request):
    retval = socketio_manage(request.environ,
                             {'/jobs': JobNamespace}, 
                             request=request)

    return retval


def includeme(config):
    utils.simple_route(config, 'socket_io', 'socket.io/*remaining', socketio_service)

